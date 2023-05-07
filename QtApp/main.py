from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox, QFileDialog
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
        self.file_name = ''

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
        self.file_name , _ = QFileDialog.getOpenFileName(self, 'Open Image File',\
        r"<Default dir>", "Image files (*.jpg *.jpeg *.png)")
        if self.file_name != "": 
            self.iamge_label.setPixmap(QPixmap(self.file_name))
        self.iamge_label.repaint()
        QApplication.processEvents()
        
        
    def aj
        outePatient(self):
        patient_id = self.le_id.text()
        patient_cin = self.le_cin.text()
        patient_nom = self.le_nom.text()
        patinet_prenom = self.le_prenom.text()
        patient_desc = self.patient_desc.text()
        patient_maladie = self.te_descrption_maladie.toPlainText()
        patient_sexe = self.cb_sexe.currentText()
        patient_nationalite = self.cb_nationalite.currentText()
        patient_img = f"{patient_id}{patient_cin}"
        img = plt.imread(self.file_name)
        plt.savefig(f"./patients_images/{patient_img}.jpg")
        QApplication.processEvents()
            
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
