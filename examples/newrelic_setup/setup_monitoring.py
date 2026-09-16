import sys

from sedai import account, credentials, monitoring_provider

# Collect the following command lines args
# Account name
# API Key
# New relic account id
# New relic api server

# Read the args from the command line
args = sys.argv[1:]

if len(args) != 4:
    print(
        "Usage: python setup_monitoring.py <sedai_account_name> <api_key> <new_relic_acount_id> <new_relic_api_server>"
    )
    sys.exit(1)


account_name = args[0]
api_key = args[1]
new_relic_account_id = args[2]
new_relic_api_server = args[3]


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

# Create the monitoring provider
new_relic_credentials = credentials.NewrelicCredentials(api_key=api_key)

nr_mp = monitoring_provider.add_new_relic_monitoring(
    account_id=account_id,
    credentials=new_relic_credentials,
    new_relic_account_id=new_relic_account_id,
    api_server=new_relic_api_server,
)
print("New relic monitoring provider added successfully")
