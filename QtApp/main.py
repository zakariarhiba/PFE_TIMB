from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QMessageBox,
    QFileDialog,
    QTableWidgetItem,
)
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QPixmap
import sys
import pandas as pd
from IPython.display import display
from PIL import Image


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()

    def set_ui(self):
        self.setWindowTitle("Track Health Application")
        self.setGeometry(300, 400, 823, 563)
        self.setFixedSize(823, 563)
        uic.loadUi("./ui/main.ui", self)
        # self.langage.activated[str].connect(self.set_langage)

    def trigged_buttons(self):
        self.button_login.clicked.connect(
            lambda: interfaces.setCurrentWidget(login_window)
        )


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()

    def set_ui(self):
        self.setWindowTitle("Track Health Application")
        self.setGeometry(300, 400, 823, 563)
        self.setFixedSize(823, 563)
        uic.loadUi("./ui/login.ui", self)
        # self.langage.activated[str].connect(self.set_langage)

    def trigged_buttons(self):
        self.button_retour.clicked.connect(
            lambda: interfaces.setCurrentWidget(main_window)
        )
        self.button_connecter.clicked.connect(lambda: self.connecter())

    def connecter(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()

        if (username == "") or (password == ""):
            QMessageBox.warning(
                self,
                "Manque d'informations",
                "S'il te plait remplir les champs obligatoires",
            )
        elif " " in username:
            QMessageBox.warning(
                self, "Nom d'utilisateur erroné", "il ne doit pas contient des espaces"
            )
        elif " " in password:
            QMessageBox.warning(
                self, "Mot de passe erroné", "il ne doit pas contient des espaces"
            )
        else:
            self.verifyDb(username, password)

    def verifyDb(self, lineEdit_username, lineEdit_password):
        try:
            df = pd.read_csv("./db/login_accounts.csv")
            df2 = df.loc[
                (df["usernames"] == lineEdit_username)
                & (df["passwords"] == lineEdit_password)
            ]
            if df2.empty:
                QMessageBox.warning(
                    self, "connection interrompue", "Utilisateur n'existe pas !"
                )
                self.lineEdit_password.setText("")
            else:
                QMessageBox.warning(
                    self, "connection verfier", "Bonne santé à vos patients"
                )
                interfaces.setCurrentWidget(patients_window)
                self.lineEdit_username.setText("")
                self.lineEdit_password.setText("")

        except:
            QMessageBox.warning(
                self,
                "connection interrompue",
                "échec de la connexion à la base de données",
            )


class Patient(QMainWindow):
    patient_name = ""
    patient_prenom = ""

    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()

    def loadPatientInfo(self):
        df = pd.read_csv(".\db\patients.csv")
        df = df[
            (df["nom"] == self.patient_name) & (df["prenom"] == self.patient_prenom)
        ]
        patient_info = df.values.tolist()
        patient_info = patient_info[0]
        self.le_id.setText(patient_info[0])
        if patient_info[0] == "NAN":
            self.le_id.setText("-")
        self.le_cin.setText(patient_info[1])
        self.le_nom.setText(patient_info[2])
        self.le_prenom.setText(patient_info[3])
        self.cb_sexe.setCurrentText(patient_info[4])
        self.cb_nationalite.setCurrentText(patient_info[5])
        self.patient_descrption.setText(patient_info[6])
        self.tb_maladie.setText(patient_info[7])
        if patient_info[7] == "NAN":
            self.tb_maladie.setText("pas de descrpition")
        try:
            if patient_info[8] != "":
                img_link = f"./patients_images/{patient_info[8]}.jpg"
                print(img_link)
                self.iamge_label.setPixmap(QPixmap(img_link))
            self.iamge_label.repaint()
        except:
            pass

    def set_ui(self):
        self.setWindowTitle("Track Health Application")
        self.setGeometry(300, 400, 823, 563)
        self.setFixedSize(823, 563)
        uic.loadUi("./ui/patient.ui", self)
        # self.langage.activated[str].connect(self.set_langage)

    def trigged_buttons(self):
        self.button_deconnecter.clicked.connect(
            lambda: interfaces.setCurrentWidget(main_window)
        )
        self.button_retour.clicked.connect(
            lambda: interfaces.setCurrentWidget(patients_window)
        )


class AjoutPatient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()
        self.file_name = ""

    def set_ui(self):
        self.setWindowTitle("Track Health Application")
        self.setGeometry(300, 400, 823, 563)
        self.setFixedSize(823, 563)
        uic.loadUi("./ui/ajoute_patient.ui", self)
        # self.langage.activated[str].connect(self.set_langage)

    def trigged_buttons(self):
        self.button_deconnecter.clicked.connect(
            lambda: interfaces.setCurrentWidget(main_window)
        )
        self.button_retour.clicked.connect(
            lambda: interfaces.setCurrentWidget(patients_window)
        )
        self.button_image.clicked.connect(self.getImage)
        self.button_ajoute_patient.clicked.connect(self.ajoutePatient)

    def getImage(self):
        try:
            self.file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Open Image File",
                r"<Default dir>",
                "Image files (*.jpg *.jpeg *.png)",
            )
            if self.file_name != "":
                self.iamge_label.setPixmap(QPixmap(self.file_name))
            self.iamge_label.repaint()
        except:
            pass
        QApplication.processEvents()

    def ajoutePatient(self):
        if self.checkPatientData() == True:
            self.patient_id = self.le_id.text()
            self.patient_cin = self.le_cin.text()
            self.patient_nom = self.le_nom.text()
            self.patient_prenom = self.le_prenom.text()
            self.patient_desc = self.patient_descrption.text()
            self.patient_maladie = self.te_descrption_maladie.toPlainText()
            self.patient_sexe = self.cb_sexe.currentText()
            self.patient_nationalite = self.cb_nationalite.currentText()
            self.patient_img = f"{self.patient_id}{self.patient_cin}"
            if self.patient_id == "":
                self.patient_id = "NAN"
            if self.patient_maladie == "":
                self.patient_maladie = "NAN"
            if self.file_name == "":
                self.patient_img = "NAN"
            try:
                img_PIL = Image.open(self.file_name)
                display(img_PIL)
                img_PIL.save(f"./patients_images/{self.patient_img}.jpg")
            except:
                print("doesn't save image")
            QApplication.processEvents()
            try:
                self.sendDataToDb()
            except:
                QMessageBox.warning(
                    self,
                    "connection interrompue",
                    "échec de la connexion à la base de données, réssayer plus tard",
                )
            else:
                QMessageBox.information(
                    self,
                    "Patient Ajouter",
                    "Votre Patient a été bien ajouter à la base de données, Bon retablissement",
                )
                self.le_id.setText("")
                self.le_cin.setText("")
                self.le_nom.setText("")
                self.le_prenom.setText("")
                self.patient_descrption.setText("")
                self.te_descrption_maladie.clear()
                self.iamge_label.setPixmap(QPixmap("./images/patient.png"))
                QApplication.processEvents()
                interfaces.setCurrentWidget(main_window)
        else:
            QMessageBox.warning(
                self,
                "Manque d'informations",
                "S'il te plait remplir les champs obligatoires",
            )

    def checkPatientData(self):
        if (
            self.le_cin.text() == ""
            or self.le_nom.text() == ""
            or self.le_prenom.text() == ""
            or self.patient_descrption.text() == ""
        ):
            return False
        return True

    def sendDataToDb(self):
        new_patient = {
            "id": self.patient_id,
            "cin": self.patient_cin,
            "nom": self.patient_nom,
            "prenom": self.patient_prenom,
            "sexe": self.patient_sexe,
            "nationalite": self.patient_nationalite,
            "desc_court": self.patient_desc,
            "desc_maladie": self.patient_maladie,
            "img_name": self.patient_img,
        }
        df = pd.read_csv(".\db\patients.csv")
        df = pd.concat([df, pd.DataFrame([new_patient])], ignore_index=True)
        df.to_csv(".\db\patients.csv", encoding="utf-8", index=False)


class Patients(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()

    def set_ui(self):
        self.setWindowTitle("Track Health Application")
        self.setGeometry(300, 400, 823, 563)
        self.setFixedSize(823, 563)
        uic.loadUi("./ui/patients.ui", self)
        self.loadData()
        # self.langage.activated[str].connect(self.set_langage)
        self.tableColumns = ["ID", "CIN", "NOM", "PRENOM", "Description"]
        self.table_patients.setHorizontalHeaderLabels(self.tableColumns)

    def trigged_buttons(self):
        self.button_deconnecter.clicked.connect(
            lambda: interfaces.setCurrentWidget(main_window)
        )
        self.button_retour.clicked.connect(
            lambda: interfaces.setCurrentWidget(main_window)
        )
        self.button_ajoute_patient.clicked.connect(
            lambda: interfaces.setCurrentWidget(ajoute_patient)
        )
        self.button_fiche_patient.clicked.connect(self.goToPatient)
        self.button_rech.clicked.connect(self.recherche)
        self.button_delete_patient.clicked.connect(lambda: self.deletePatient())

    def deletePatient(self):
        try:
            indexRow = self.table_patients.selectedIndexes()[0].row()
            dl_patient_nom = self.patients_liste[indexRow][2]
            dl_patient_prenom = self.patients_liste[indexRow][3]
            print(f"{dl_patient_nom} {dl_patient_prenom}")
            df = pd.read_csv(".\db\patients.csv")
            df = df.loc[
                (df["nom"] != dl_patient_nom) & (df["prenom"] != dl_patient_prenom)
            ]
            df.to_csv(".\db\patients.csv", encoding="utf-8", index=False)
            self.loadData()
        except:
            self.labelEror.setText("Erreur Connection à BD")
        else:
            QMessageBox.information(
                self,
                "Patient Supprimer",
                "Votre Patient a été bien supprimer",
            )
            self.labelEror.setText("")

    def recherche(self):
        key_cin = self.le_cin_rech.text()
        if key_cin != "":
            try:
                self.table_patients.clear()
                self.table_patients.setHorizontalHeaderLabels(self.tableColumns)
                df = pd.read_csv(".\db\patients.csv")
                df = df[df["cin"] == key_cin]
                self.patients_liste = df.values.tolist()
                rowPosition = self.table_patients.rowCount()
                self.table_patients.insertRow(rowPosition)
                self.table_patients.setRowCount(len(self.patients_liste))
                row = 0
                for patient in self.patients_liste:
                    self.table_patients.setItem(row, 0, QTableWidgetItem(patient[0]))
                    self.table_patients.setItem(row, 1, QTableWidgetItem(patient[1]))
                    self.table_patients.setItem(row, 2, QTableWidgetItem(patient[2]))
                    self.table_patients.setItem(row, 3, QTableWidgetItem(patient[3]))
                    self.table_patients.setItem(row, 4, QTableWidgetItem(patient[6]))
                    row = row + 1
                if len(self.patients_liste) == 0:
                    self.labelEror.setText("Not found !")
                else:
                    self.labelEror.setText("")
            except:
                self.labelEror.setText("Erreur Connection à BD")
        else:
            self.loadData()

    def goToPatient(self):
        try:
            indexRow = self.table_patients.selectedIndexes()[0].row()
            dl_patient_nom = self.patients_liste[indexRow][2]
            dl_patient_prenom = self.patients_liste[indexRow][3]
            patient_window.patient_name = dl_patient_nom
            patient_window.patient_prenom = dl_patient_prenom
            patient_window.loadPatientInfo()
        except:
            self.labelEror.setText("Erreur Connection à BD")
        else:
            self.labelEror.setText("")
            interfaces.setCurrentWidget(patient_window)

    def loadData(self):
        try:
            df = pd.read_csv(".\db\patients.csv")
            self.patients_liste = df.values.tolist()
            rowPosition = self.table_patients.rowCount()
            self.table_patients.insertRow(rowPosition)
            self.table_patients.setRowCount(len(self.patients_liste))
            row = 0
            for patient in self.patients_liste:
                self.table_patients.setItem(row, 0, QTableWidgetItem(f"{patient[0]}"))
                if patient[0] == "NAN":
                    self.table_patients.setItem(row, 0, QTableWidgetItem(""))
                self.table_patients.setItem(row, 1, QTableWidgetItem(f"{patient[1]}"))
                self.table_patients.setItem(row, 2, QTableWidgetItem(f"{patient[2]}"))
                self.table_patients.setItem(row, 3, QTableWidgetItem(f"{patient[3]}"))
                self.table_patients.setItem(row, 4, QTableWidgetItem(f"{patient[6]}"))
                row = row + 1
            if len(self.patients_liste) == 0:
                self.labelEror.setText("Not found !")
            else:
                self.labelEror.setText("")
        except:
            self.labelEror.setText("Erreur Connection à BD")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    interfaces = QStackedWidget()
    interfaces.setWindowIcon(QtGui.QIcon("./images/icon.png"))
    main_window = Main()
    login_window = Login()
    patient_window = Patient()
    patients_window = Patients()
    ajoute_patient = AjoutPatient()
    interfaces.addWidget(main_window)
    interfaces.addWidget(login_window)
    interfaces.addWidget(patient_window)
    interfaces.addWidget(patients_window)
    interfaces.addWidget(ajoute_patient)
    interfaces.show()
    interfaces.setWindowTitle("Track Health Application")
    interfaces.setFixedSize(823, 563)
    interfaces.setGeometry(180, 120, 823, 563)

    try:
        app.exec_()
    except:
        print("closing...")
