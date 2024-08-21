import sys
import pandas as pd
from sedai import account, credentials, monitoring_provider

# Collect the following command line arges:
# -- excel_file_path

excel_file_path = sys.argv[1]

if len(sys.argv) < 2:
    print("Usage: python setup_multiple_accounts.py <excel_file_path>")
    sys.exit(1)

# Read the Excel file
try:
    df = pd.read_excel(excel_file_path)
except Exception as e:
    print(f"Error reading Excel file: {e}")
    sys.exit(1)

# Ensure the required columns are present
required_columns = ['Account Name', 'IAM Role', 'External ID']
for column in required_columns:
    if column not in df.columns:
        print(f"Missing required column: {column}")
        sys.exit(1)

# Creating each account in Sedai
for index, row in df.iterrows():
    account_name = row['Account Name']
    role_arn = row['IAM Role']
    external_id = row['External ID'] if not pd.isna(row['External ID']) else None

    try:
        credentials_obj = credentials.AwsRoleCredentials(
            role_arn=role_arn,
            external_id=external_id
        )

        account_status = account.create_account(
            name=account_name,
            cloud_provider='AWS',
            integration_type='AGENTLESS',
            credentials=credentials_obj
        )

        accounts = account.search_accounts_by_name(account_name)
        aws_account = accounts[0]
        account_id = aws_account.id

        if account_status:
            print(f"Account {account_name} created successfully with id {account_id}")

            # Create the monitoring provider
            monitoring_provider.add_cloudwatch_monitoring(
                account_id=account_id,
                credentials=credentials_obj
            )

    except Exception as e:
        print(f"Error processing account {account_name} with IAM Role {role_arn} and External ID {external_id}: {e}")

print("All accounts processed successfully.")