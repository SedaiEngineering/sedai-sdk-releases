from sedai import account

test_connection_failed_accounts = []
accounts = account.get_all_accounts()
for acc in accounts:
    print(f"TestConnection starting for {acc.id}")
    if not account.test_connection(acc.id):
        test_connection_failed_accounts.append((acc.name, acc.providerAccountId))
print("TestConnection completed successfully for all accounts")

#write the failed accounts to a file
with open('test_connection_failed_accounts.csv', 'w+') as file:
    for account in test_connection_failed_accounts:
        file.write(f"{account[0]},{account[1]}\n")
print("Accounts which failed test_connection are successfully written to test_connection_failed_accounts.csv")