import pandas as pd


# create login accounts database
# Accounts = ({
#     'usernames':["Zak"],
#     'passwords' :["123456789"]
#                })
# df = pd.DataFrame(Accounts)



# create patients accounts database
# Patients = ({
#     'id':[],
#     'cin':[],
#     'nom' :[],
#     'prenom':[],
#     'sexe':[],
#     'nationalite':[],
#     'desc_court':[],
#     'desc_maladie':[],
#     'img_name':[]
#     })
# df = pd.DataFrame(Patients)

# df.to_csv("patients.csv",encoding='utf-8', index=False)
# Modify db

# add new account

# new_acc ={
#     'usernames':'admin',
#     'passwords' :'123'
#     }

# df = pd.concat([df, pd.DataFrame([new_acc])], ignore_index=True)

dl_patient_nom = "SAAD"
dl_patient_prenom = "EDDHAMANI"
df = pd.read_csv(".\patients.csv")
df = df[(df['nom'] == dl_patient_nom) & (df['prenom'] == dl_patient_prenom)  ] 
patient_info = df.values.tolist()
patient_info = patient_info[0]
print(patient_info)


# df = df.loc[(df["nom"] != dl_patient_nom) & (df["prenom"]!= dl_patient_prenom)]
# df = df.loc[df["cin"] != 'BJ891222']


# patient_id = "NAN"
# patient_cin = "BJ467011"
# patient_nom = "rhiba"
# patinet_prenom = "zakaria"
# patient_desc = "churirgie poumon"
# patient_maladie = "churirgie poumon cause de fumer"
# patient_sexe = "Homme"
# patient_nationalite = "Marocaine"
# patient_img = f"{patient_id}{patient_cin}"

# new_patient ={
#     'id':patient_id,
#     'cin':patient_cin,
#     'nom' :patient_nom,
#     'prenom':patinet_prenom,
#     'sexe':patient_desc,
#     'nationalite':patient_maladie,
#     'desc_court':patient_sexe,
#     'desc_maladie':patient_nationalite,
#     'img_name':patient_img
#     }

# df = pd.concat([df, pd.DataFrame([new_patient])], ignore_index=True)


# df.to_csv("patients.csv",encoding='utf-8', index=False)



# patients_liste = df.values.tolist()

# for patient in patients_liste:
#     print(patient)


# verify account exists

# lineEdit_username = "admin"
# lineEdit_password = "Zikddo0384"

# print(lineEdit_username in set(df['usernames']))

# df2 = df.loc[
#     (df["usernames"] == lineEdit_username) & (df["passwords"] == lineEdit_password)
# ]
# if df2.empty:
#     print("Account doesn't exist")
# else:
#     print("Account Found")
