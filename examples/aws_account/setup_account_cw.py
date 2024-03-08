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

account_status = account.create_account(
    name=account_name,
    cloud_provider='AWS',
    integration_type='AGENTLESS',
    credentials=credentials)


accounts = account.search_accounts_by_name(account_name)
aws_account = accounts[0]
account_id = aws_account.id

print(f"Account {account_name} created successfully with id {account_id}")

# Create the monitoring provider
monitoring_provider.add_cloudwatch_monitoring(
    account_id=account_id,
    credentials=credentials
)

