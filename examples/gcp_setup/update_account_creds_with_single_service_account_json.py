import sys
import csv
import time
import os
from sedai import account, credentials

if len(sys.argv) < 3:
    print("Usage: python update_account_creds_with_single_service_account_json.py <csv_file_path> <service_account_key.json>")
    sys.exit(1)

csv_file_path = sys.argv[1]
service_account_path = sys.argv[2]

if not os.path.exists(service_account_path):
    print(f"Service account file not found: {service_account_path}")
    sys.exit(1)

with open(service_account_path, 'r') as f:
    service_account_json = f.read()

credentials_obj = credentials.GCPServiceAccountJsonCredentials(service_account_json)

required_columns = {'Account ID'}

account_ids = []
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    missing_columns = required_columns - set(reader.fieldnames)
    if missing_columns:
        print(f"Missing required columns: {', '.join(missing_columns)}")
        sys.exit(1)

    for row in reader:
        account_id = row['Account ID'].strip()
        if account_id:
            account_ids.append((account_id, row.get('Account Name', '').strip()))

if not account_ids:
    print("No account IDs found in CSV.")
    sys.exit(0)

succeeded = []
failed = []

for i, (account_id, name) in enumerate(account_ids, start=1):
    print("-------------------------------------------------------------------------------")
    label = f"{account_id} ({name})" if name else account_id
    print(f"{i}/{len(account_ids)}. Updating credentials for account: {label}")

    try:
        result = account.update_account(id=account_id, credentials=credentials_obj)
        if result:
            print(f"Credentials updated successfully for account: {label}")
            succeeded.append(account_id)
        else:
            print(f"Failed to update credentials for account: {label}")
            failed.append(account_id)
    except Exception as e:
        print(f"Error updating credentials for account {label}: {e}")
        failed.append(account_id)

    if i < len(account_ids):
        time.sleep(5)

print("-------------------------------------------------------------------------------")
print(f"Done. {len(succeeded)} succeeded, {len(failed)} failed.")
if failed:
    print(f"Failed account IDs: {', '.join(failed)}")
