from sedai import monitoring_provider
from sedai import credentials
from sedai import account

import sys

# Collect the following command line arges:
# Account Name
# Monitoring Provider Id
# Api Key
# Application key

# Read the args from the command line
args = sys.argv[1:]

if len(args) != 4:
    print("Usage: python setup_monitoring.py <sedai_account_name> <monitoring_provider_id> <api_key> <application_key>")
    print("Note: To add new monitoring provider set the <monitoring_provider_id> as None")
    sys.exit(1)


account_name = args[0]
monitoring_provider_id = args[1]
api_key = args[2]
application_key = args[3]

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

dd_mp = monitoring_provider.add_or_update_datadog_monitoring(
    account_id=account_id,
    credentials=tc,
    monitoring_provider_id= monitoring_provider_id,
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

print(f"Datadog monitoring provider added or updated successfully to account {account_name}")
