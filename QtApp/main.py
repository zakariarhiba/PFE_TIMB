from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QMessageBox,
    QFileDialog,
)
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QPixmap
import sys
import pandas as pd
import matplotlib.pyplot as plt


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
                interfaces.setCurrentWidget(home_window)
                self.lineEdit_username.setText("")
                self.lineEdit_password.setText("")

        except:
            QMessageBox.warning(
                self,
                "connection interrompue",
                "échec de la connexion à la base de données",
            )


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()

    def set_ui(self):
        self.setWindowTitle("Track Health Application")
        self.setGeometry(300, 400, 823, 563)
        self.setFixedSize(823, 563)
        uic.loadUi("./ui/home.ui", self)
        # self.langage.activated[str].connect(self.set_langage)

    def trigged_buttons(self):
        self.button_deconnecter.clicked.connect(
            lambda: interfaces.setCurrentWidget(main_window)
        )
        self.button_consultation.clicked.connect(
            lambda: interfaces.setCurrentWidget(patients_window)
        )
        self.button_ajoute_patient.clicked.connect(
            lambda: interfaces.setCurrentWidget(ajoute_patient)
        )
        self.button_modifier_patient.clicked.connect(
            lambda: interfaces.setCurrentWidget(patient_window)
        )
        self.button_suprimer_patient.clicked.connect(
            lambda: interfaces.setCurrentWidget(patient_window)
        )
        self.button_recherche.clicked.connect(
            lambda: interfaces.setCurrentWidget(patient_window)
        )


class Patient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()

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
            lambda: interfaces.setCurrentWidget(home_window)
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
            lambda: interfaces.setCurrentWidget(home_window)
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
            self.patinet_prenom = self.le_prenom.text()
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
                self.patient_img = ".\images\patient.png"
            try:
                img = plt.imread(self.file_name)
                plt.savefig(f"./patients_images/{self.patient_img}.jpg")
            except:
                pass
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
                interfaces.setCurrentWidget(home_window)
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
            "prenom": self.patinet_prenom,
            "sexe": self.patient_desc,
            "nationalite": self.patient_maladie,
            "desc_court": self.patient_sexe,
            "desc_maladie": self.patient_nationalite,
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
        # self.langage.activated[str].connect(self.set_langage)

    def trigged_buttons(self):
        self.button_deconnecter.clicked.connect(
            lambda: interfaces.setCurrentWidget(main_window)
        )
        self.button_retour.clicked.connect(
            lambda: interfaces.setCurrentWidget(home_window)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    interfaces = QStackedWidget()
    interfaces.setWindowIcon(QtGui.QIcon("./images/icon.png"))
    main_window = Main()
    login_window = Login()
    home_window = Home()
    patient_window = Patient()
    patients_window = Patients()
    ajoute_patient = AjoutPatient()
    interfaces.addWidget(main_window)
    interfaces.addWidget(login_window)
    interfaces.addWidget(home_window)
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
