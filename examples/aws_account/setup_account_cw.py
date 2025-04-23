import sys

from sedai import account, credentials, monitoring_provider

args = sys.argv[1:]

# Collect the following command line arges:
# - account_name
# - role_arn
# - external_id (optional)

if len(args) < 2:
    print("Usage: python setup_account_cw.py <account_name> <role_arn> <external_id>")
    sys.exit(1)

account_name = args[0]
role_arn = args[1]
external_id = args[2] if len(args) == 3 else None

# Create the account in Sedai

credentials = credentials.AwsRoleCredentials(
    role_arn=role_arn,
    external_id=external_id
)

sedai_account_id = account.create_account(
    name=account_name,
    cloud_provider='AWS',
    integration_type='AGENTLESS',
    credentials=credentials)

print(f"Account {account_name} created successfully with id {sedai_account_id}")

# Create the monitoring provider
monitoring_provider.add_cloudwatch_monitoring(
    account_id=sedai_account_id,
    use_account_credentials=True
)

