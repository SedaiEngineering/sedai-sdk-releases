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

kubernetes_account = account.create_account(
    name=account_name,
    cloud_provider='KUBERNETES',
    integration_type='AGENT_BASED',
    credentials=credentials.FederatedPrometheusJWT(
        bearer_token='bearer_token'
    ),
    cluster_provider='GCP'
)

print(f"Account {account_name} created successfully")

# Get the agent installation command
install_command = account.get_agent_installation_command(account_name)
kubectl_cmd = install_command.kubeInstallCmd

print(f"Agent installation command\n\n: {kubectl_cmd}")
