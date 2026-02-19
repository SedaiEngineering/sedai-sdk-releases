import sys
from sedai import account, credentials, monitoring_provider
import time, csv, json, os

if len(sys.argv) < 3:
    print("Usage: python setup_multiple_accounts.py <csv_file_path> <json key file path>")
    sys.exit(1)

csv_file_path = sys.argv[1]
service_account_path=sys.argv[2]

required_columns = {'Project Name', 'Project ID'}

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    # Check for missing columns
    missing_columns = required_columns - set(reader.fieldnames)
    if missing_columns:
        print(f"Missing required columns: {', '.join(missing_columns)}")
        sys.exit(1)

    i = 0
    for row in reader:
        account_name = row['Project Name']
        project_id = row['Project ID']

        print("-------------------------------------------------------------------------------")
        i += 1
        print(f"{i}. Waiting 30 seconds before processing the next account...")
        time.sleep(30)

        if not os.path.exists(service_account_path):
            print(f"Service account file not found: {service_account_path}")
            continue

        try:
            with open(service_account_path, 'r') as f:
                service_account_json = f.read()

            credentials_obj = credentials.GCPServiceAccountJsonCredentials(
                service_account_json
            )

            sedai_account_id = account.create_account(
                name=account_name,
                cloud_provider='GCP',
                integration_type='AGENTLESS',
                credentials=credentials_obj,
                project_id=project_id,
            )

        except Exception as e:
            print(f"Error creating GCP account {account_name}: {e}")
            continue

        try:
            if sedai_account_id:
                print(f"Account {account_name} created successfully with id {sedai_account_id}")

                # Add GCP Monitoring (Cloud Monitoring)
                monitoring_provider.add_GKE_monitoring(
                    account_id=sedai_account_id,
                    project_id=row['Project ID'],
                    credentials=credentials.GKEMonitoringCredentials(
                        service_account_json=service_account_json
                    )
                )

        except Exception as e:
            print(f"Error creating monitoring provider for {account_name}: {e}")

print("All GCP accounts processed.")
