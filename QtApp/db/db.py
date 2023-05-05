import pandas as pd


# create login accounts database
# Accounts = ({
#     'usernames':["Zak"],
#     'passwords' :["123456789"]
#                })
# df = pd.DataFrame(Accounts)


# Modify db
df = pd.read_csv(".\login_accounts.csv")
# add new account

new_acc ={
    'usernames':'admin',
    'passwords' :'123'
    }

df = pd.concat([df, pd.DataFrame([new_acc])], ignore_index=True)


df.to_csv("login_accounts.csv",encoding='utf-8', index=False)


# verify account exists

lineEdit_username = "admin"
lineEdit_password = "Zikddo0384"

# print(lineEdit_username in set(df['usernames']))

df2 = df.loc[
    (df["usernames"] == lineEdit_username) & (df["passwords"] == lineEdit_password)
]
if df2.empty:
    print("Account doesn't exist")
else:
    print("Account Found")
