import sys

from sedai import account, credentials

# Collect the following command line arges:
# -
# Account Name

# Read the args from the command line
args = sys.argv[1:]

if len(args) != 1:
    print("Usage: python setup_cluster.py <sedai_account_name>")
    sys.exit(1)

account_name = args[0]

sedai_account_id = account.create_account(
    name=account_name,
    cloud_provider='KUBERNETES',
    integration_type='AGENT_BASED',
    credentials=credentials.SedaiCredentials(),
    cluster_provider='GCP',
)

if not sedai_account_id:
    print(f"Failed to create account {account_name}")
    sys.exit(1)

print(f"Account {account_name} created successfully")

# Get the agent installation command
install_command = account.get_agent_installation_command_by_id(sedai_account_id)
if install_command is None:
    print(f"Failed to get agent installation command for account {sedai_account_id}")
    sys.exit(1)

kubectl_cmd = install_command.kubeInstallCmd

print(f"Agent installation command\n\n: {kubectl_cmd}")
