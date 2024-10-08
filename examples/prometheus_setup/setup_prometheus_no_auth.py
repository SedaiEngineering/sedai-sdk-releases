from sedai import monitoring_provider
from sedai import credentials
from sedai import account

import sys

"""
Collects
- the account name to add monitoring provider to
- the prometheus endpoint
as command line arguments.
"""


# Read the args from the command line
args = sys.argv[1:]

if len(args) != 2:
    print("Usage: python setup_prometheus_no_auth.py <sedai_account_name> <prometheus_endpoint>")
    sys.exit(1)


account_name = args[0]
prometheus_endpoint = args[1]

# Check if the account_name exists
accounts = account.search_accounts_by_name(account_name)
if len(accounts) == 0:
    print(f"The account with name {account_name} does not exist")
    sys.exit(1)

# Create the monitoring provider
fp_creds = credentials.FederatedPrometheusNoAuth()
accounts = account.search_accounts_by_name(account_name)
account_id = accounts[0].id

gke_mp = monitoring_provider.add_federated_prometheus_monitoring(
    account_id=account_id,
    credentials=fp_creds,
    endpoint=prometheus_endpoint,
)
