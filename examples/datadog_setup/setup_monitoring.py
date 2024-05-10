from sedai import monitoring_provider
from sedai import credentials
from sedai import account
import os
import json

import sys

# Collect the following command line arges:
# - service_account_json file path
# Project ID
# Account Name

# Read the args from the command line
args = sys.argv[1:]

if len(args) != 3:
    print("Usage: python setup_monitoring.py <sedai_account_name> <api_key> <application_key>")
    sys.exit(1)


account_name = args[0]
api_key = args[1]
application_key = args[2]



# Check if the account_name exists
accounts = account.search_accounts_by_name(account_name)
if len(accounts) == 0:
    print(f"The account with name {account_name} does not exist")
    sys.exit(1)

# Create the monitoring provider
tc = credentials.DatadogCredentials(
    api_key=api_key,
    application_key=application_key,

)

account_id = accounts[0].id


dd_mp = monitoring_provider.add_datadog_monitoring(
    account_id=account_id,
    credentials=tc,
    app_dimensions=[
        "destination_workload",
        "service",
        "kube_app_name"
    ],
    region_dimensions=[],
    az_dimensions=[],
    namespace_dimensions=[
        "destination_service_namespace",
        "namespace",
        "kube_namespace"
    ],
    cluster_dimensions=[
        "cluster_name",
        "kube_cluster_name"
    ],
    env_dimensions=[],
    instance_id_pattern=None,


)
print(f"Datadog monitoring provider added successfully to account {account_name}")
