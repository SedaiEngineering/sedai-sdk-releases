import sys

from sedai import account, credentials, monitoring_provider

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
tc = credentials.DatadogCredentials(
    api_key=api_key,
    application_key=application_key,
)


dd_mp = monitoring_provider.add_datadog_monitoring(
    account_id=account_id,
    credentials=tc,
    app_dimensions=["destination_workload", "service", "kube_app_name"],
    region_dimensions=[],
    az_dimensions=[],
    namespace_dimensions=["destination_service_namespace", "namespace", "kube_namespace"],
    cluster_dimensions=["cluster_name", "kube_cluster_name"],
    env_dimensions=[],
    instance_id_pattern=None,
)
print(f"Datadog monitoring provider added successfully to account {account_name}")
