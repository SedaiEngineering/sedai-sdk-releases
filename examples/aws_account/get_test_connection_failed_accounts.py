from sedai import account

testConnectionFailedAccounts = []
accounts = account.get_all_accounts()
for acc in accounts:
    if not account.testConnection(acc.id):
        testConnectionFailedAccounts.append((acc.name, acc.providerAccountId))

#write the failed accounts to a file
with open('test_connection_failed_accounts.txt', 'w+') as file:
    for account in testConnectionFailedAccounts:
        file.write(f"{account[0]}: {account[1]}\n")