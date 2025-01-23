from sedai import monitoring_provider
from sedai import credentials
from sedai import account

import sys

# Collect the following command lines args
# Account name
# API Key
# New relic account id
# New relic api server

# Read the args from the command line
args = sys.argv[1:]

if len(args) != 4:
    print("Usage: python setup_monitoring.py <sedai_account_name> <api_key> <new_relic_acount_id> <new_relic_api_server>")
    sys.exit(1)


account_name = args[0]
api_key = args[1]
new_relic_account_id = args[2]
new_relic_api_server = args[3]


# Check if the account_name exists
accounts = account.search_accounts_by_name(account_name)
if len(accounts) == 0:
    print(f"The account with name {account_name} does not exist")
    sys.exit(1)

# Create the monitoring provider
new_relic_credentials = credentials.NewrelicCredentials(api_key=api_key)

account_id = accounts[0].id

nr_mp = monitoring_provider.add_new_relic_monitoring(
        account_id=account_id,
        credentials=new_relic_credentials,
        new_relic_account_id=new_relic_account_id,
        api_server=new_relic_api_server,
)
print("New relic monitoring provider added successfully")
