import json
import os
import sys

from sedai import account, credentials, monitoring_provider

# Collect the following command line arges:
# - service_account_json file path
# Project ID
# Account Name

# Read the args from the command line
args = sys.argv[1:]

if len(args) != 3:
    print(
        "Usage: python setup_monitoring.py <service_account_json_file_path> <project_id> <sedai_account_name>"
    )
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
except Exception:  # noqa: BLE001 - intentional catch-all boundary; logs/wraps and degrades gracefully
    print("The service account file is not a valid json")
    sys.exit(1)

# Check that exactly one account exists with this name. Account names are not unique in Sedai.
accounts = account.search_accounts_by_name(account_name)
if len(accounts) == 0:
    print(f"The account with name {account_name} does not exist")
    sys.exit(1)
if len(accounts) > 1:
    print(
        f"More than one account found with name {account_name}. Matching ids: "
        + ", ".join(a.id for a in accounts)
    )
    print("Re-run with an unambiguous account name, or delete the duplicates.")
    sys.exit(1)

account_id = accounts[0].id

# Read the service account json file
with open(service_account_json_file_path, 'r') as f:
    service_account_json = json.load(f)
    # Convert the json to a json string
    service_account_json = json.dumps(service_account_json)

# Create the monitoring provider
tc = credentials.GKEMonitoringCredentials(service_account_json=service_account_json)

gke_mp = monitoring_provider.add_GKE_monitoring(
    account_id=account_id,
    project_id=project_id,
    credentials=tc,
    lb_dimensions=['test_val1', 'test_val_2'],
    region_dimensions=['region_val1', 'region_val_2'],
)
