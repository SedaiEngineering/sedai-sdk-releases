import sys
from sedai import account, credentials, monitoring_provider
import time, csv

if len(sys.argv) < 2:
    print("Usage: python setup_multiple_accounts.py <csv_file_path>")
    sys.exit(1)

# Collect the following command line arges:
csv_file_path = sys.argv[1]

required_columns = {'Account Name', 'IAM Role', 'External ID'}

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    # Check for missing columns
    missing_columns = required_columns - set(reader.fieldnames)
    if missing_columns:
        print(f"Missing required columns: {', '.join(missing_columns)}")
        sys.exit(1)
    else:
        i = 0
        for row in reader:
            account_name = row['Account Name']
            role_arn = row['IAM Role']
            external_id = row['External ID'] if row['External ID'] else None  # Handle empty values

            print("-------------------------------------------------------------------------------")
            i = i + 1
            print(f" {i}. Waiting 30 seconds before processing the next account...")
            time.sleep(30)

            try:
                credentials_obj = credentials.AwsRoleCredentials(
                    role_arn=role_arn,
                    external_id=external_id
                )
                sedai_account_id = account.create_account(
                    name=account_name,
                    cloud_provider='AWS',
                    integration_type='AGENTLESS',
                    credentials=credentials_obj
                )
            except Exception as e:
                print(f"Error processing account create {account_name} with IAM Role {role_arn} and External ID {external_id}: {e}")

            try:
                if sedai_account_id:
                    print(f"Account {account_name} created successfully with id {sedai_account_id}")

                    # Create the monitoring provider
                    monitoring_provider.add_cloudwatch_monitoring(
                        account_id=sedai_account_id,
                        use_account_credentials=True
                    )

            except Exception as e:
                print(f"Error creating monitoring provider for {account_name}: {e}")

print("All accounts processed successfully.")