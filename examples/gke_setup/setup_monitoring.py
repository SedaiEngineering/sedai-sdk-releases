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
    print("Usage: python setup_monitoring.py <service_account_json_file_path> <project_id> <sedai_account_name>")
    sys.exit(1)


service_account_json_file_path = args[0]
project_id = args[1]
account_name = args[2]


# First check if the service_account_json_file_path exists
if not os.path.exists(service_account_json_file_path):
    print("The service account file does not exist")
    sys.exit(1)

# Check if the service_account_json_file_path is a valid json
try:
    with open(service_account_json_file_path, 'r') as f:
        json.load(f)
except Exception as e:
    print("The service account file is not a valid json")
    sys.exit(1)

# Check if the account_name exists
accounts = account.search_accounts_by_name(account_name)
if len(accounts) == 0:
    print(f"The account with name {account_name} does not exist")
    sys.exit(1)

# Read the service account json file
with open(service_account_json_file_path, 'r') as f:
    service_account_json = json.load(f)
    # Convert the json to a json string
    service_account_json = json.dumps(service_account_json)

# Create the monitoring provider
tc = credentials.GKEMonitoringCredentials(
    service_account_json=service_account_json
)
accounts = account.search_accounts_by_name(account_name)
account_id = accounts[0].id

gke_mp = monitoring_provider.add_GKE_monitoring(
    account_id=account_id,
    project_id=project_id,
    credentials=tc,
    lb_dimensions=['test_val1', 'test_val_2'],
    region_dimensions=['region_val1', 'region_val_2']
)