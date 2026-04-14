import sys
from sedai import account, credentials
import time, csv, json

if len(sys.argv) < 3:
    print("Usage: python update_accounts_with_single_service_principal_creds.py <csv_file_path> <credentials_file_path>")
    print("CSV columns: Account ID, Account Name (optional)")
    print("Credentials file (JSON): { \"client_id\": \"...\", \"client_secret\": \"...\" }")
    sys.exit(1)

csv_file_path = sys.argv[1]
credentials_file_path = sys.argv[2]

with open(credentials_file_path, encoding='utf-8') as creds_file:
    creds_data = json.load(creds_file)

client_id = creds_data.get('client_id')
client_secret = creds_data.get('client_secret')

if not client_id or not client_secret:
    print("Credentials file must contain 'client_id' and 'client_secret' fields.")
    sys.exit(1)

required_columns = {'Account ID'}

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    missing_columns = required_columns - set(reader.fieldnames)
    if missing_columns:
        print(f"Missing required columns: {', '.join(missing_columns)}")
        sys.exit(1)

    rows = list(reader)

if not rows:
    print("No rows found in CSV.")
    sys.exit(0)

succeeded = []
failed = []

for i, row in enumerate(rows, start=1):
    print("-------------------------------------------------------------------------------")
    account_id = row['Account ID'].strip()
    account_name = row.get('Account Name', '').strip()

    label = f"{account_id} ({account_name})" if account_name else account_id
    print(f"{i}/{len(rows)}. Updating credentials for Azure account: {label}")

    try:
        credentials_obj = credentials.AzureClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )

        result = account.update_account(
            id=account_id,
            credentials=credentials_obj
        )

        if result:
            print(f"Credentials updated successfully for account: {label}")
            succeeded.append(account_id)
        else:
            print(f"Failed to update credentials for account: {label}")
            failed.append(account_id)

    except Exception as e:
        print(f"Error updating credentials for account {label}: {e}")
        failed.append(account_id)

    if i < len(rows):
        print(f"Waiting 30 seconds before processing the next account...")
        time.sleep(30)

print("-------------------------------------------------------------------------------")
print(f"Done. {len(succeeded)} succeeded, {len(failed)} failed.")
if failed:
    print(f"Failed account IDs: {', '.join(failed)}")
