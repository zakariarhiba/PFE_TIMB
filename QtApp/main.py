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
import paho.mqtt.client as paho
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from time import sleep

import smtplib, ssl

smtp_server = "smtp.gmail.com"
port = 465    # For SMTP
sender_email = "zakariarhiba21@gmail.com"
password = "Ziko0384Qqhi"

context = ssl.create_default_context()


class MqttApp(QThread):
    spio2 = pyqtSignal(str)
    temp = pyqtSignal(str)
    pulse_rate = pyqtSignal(str)

    def run(self):
        self.client = paho.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe("moniteurCHU/temp")
        self.client.subscribe("moniteurCHU/spio2")
        self.client.subscribe("mntrCHU/plsRate")

    def on_message(self, client, userdata, msg):
        topic, message = msg.topic, msg.payload.decode("utf-8")
        print(topic + " -> " + str(message))
        if topic == "moniteurCHU/temp":
            self.temp.emit(str(message))
        elif topic == "moniteurCHU/spio2":
            self.spio2.emit(message)
        elif topic == "mntrCHU/plsRate":
            self.pulse_rate.emit(message)

    def on_publish(self, client, userdata, result):
        print("data published")

    def publish_msg(self, topic, message):
        ret = self.client.publish(topic, message)


# still need image deleted from patient images folder


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
                QMessageBox.information(
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
            self.patient_id = str(self.le_id.text())
            self.patient_cin = str(self.le_cin.text())
            self.patient_nom = str(self.le_nom.text())
            self.patient_prenom = str(self.le_prenom.text())
            self.patient_desc = str(self.patient_descrption.text())
            self.patient_maladie = str(self.te_descrption_maladie.toPlainText())
            self.patient_sexe = str(self.cb_sexe.currentText())
            self.patient_nationalite = str(self.cb_nationalite.currentText())
            self.moniteur_statut = str(self.cb_moniteur.currentText())
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
                interfaces.setCurrentWidget(patients_window)
                patients_window.loadData()
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
            "moniteur_statut": self.moniteur_statut,
            "sexe": self.patient_sexe,
            "nationalite": self.patient_nationalite,
            "desc_court": self.patient_desc,
            "desc_maladie": self.patient_maladie,
            "img_name": self.patient_img,
        }
        df = pd.read_csv(".\db\patients.csv")
        df = pd.concat([df, pd.DataFrame([new_patient])], ignore_index=True)
        df.to_csv(".\db\patients.csv", encoding="utf-8", index=False)


class ModifierPatient(QMainWindow):
    patient_named = ""
    patient_prenomd = ""
    file_name = ""

    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()
        self.file_name = ""

    def set_ui(self):
        self.setWindowTitle("Track Health Application")
        self.setGeometry(300, 400, 823, 563)
        self.setFixedSize(823, 563)
        uic.loadUi("./ui/modifier_patient.ui", self)
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

    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()

    def loadPatientInfo(self):
        self.labelEror.setText("")
        df = pd.read_csv(".\db\patients.csv")
        df = df[
            (df["nom"] == self.patient_named) & (df["prenom"] == self.patient_prenomd)
        ]
        patient_info = df.values.tolist()
        patient_info = patient_info[0]
        self.le_id.setText(str(patient_info[0]))
        if patient_info[0] == "NAN":
            self.le_id.setText("-")
        self.le_cin.setText(str(patient_info[1]))
        self.le_nom.setText(str(patient_info[2]))
        self.le_prenom.setText(str(patient_info[3]))
        self.cb_moniteur.setCurrentText(str(patient_info[4]))
        self.cb_sexe.setCurrentText(str(patient_info[5]))
        self.cb_nationalite.setCurrentText(str(patient_info[6]))
        self.patient_descrption.setText(str(patient_info[7]))
        self.tb_maladie.setText(str(patient_info[8]))

        if str(patient_info[4]) == "Deactive":
            self.statutM = "N"
        else:
            self.statutM = "Y"
        if patient_info[8] == "NAN":
            self.tb_maladie.setText("pas de descrpition")
        try:
            if patient_info[9] != "" and patient_info[9] != "NAN":
                img_link = f"./patients_images/{patient_info[9]}.jpg"
                print(img_link)
                self.iamge_label.setPixmap(QPixmap(img_link))
            elif patient_info[9] == "NAN":
                self.iamge_label.setPixmap(QPixmap("./images/patient.png"))
            self.iamge_label.repaint()
        except:
            pass

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
            self.patient_id = str(self.le_id.text())
            self.patient_cin = str(self.le_cin.text())
            self.patient_nom = str(self.le_nom.text())
            self.patient_prenom = str(self.le_prenom.text())
            self.patient_desc = str(self.patient_descrption.text())
            self.patient_maladie = str(self.tb_maladie.toPlainText())
            self.moniteur_statut = str(self.cb_moniteur.currentText())
            self.patient_sexe = str(self.cb_sexe.currentText())
            self.patient_nationalite = str(self.cb_nationalite.currentText())
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
                    "Patient Data Modifier",
                    "Votre Patient a été bien corriger ses données, Bon retablissement",
                )
                self.le_id.setText("")
                self.le_cin.setText("")
                self.le_nom.setText("")
                self.le_prenom.setText("")
                self.patient_descrption.setText("")
                self.tb_maladie.clear()
                self.iamge_label.setPixmap(QPixmap("./images/patient.png"))
                self.deletePatient(self.patient_named, self.patient_prenomd)
                QApplication.processEvents()
                interfaces.setCurrentWidget(patients_window)
                patients_window.loadData()
        else:
            QMessageBox.warning(
                self,
                "Manque d'informations",
                "S'il te plait remplir les champs obligatoires",
            )

    def deletePatient(self, dl_patient_nom, dl_patient_prenom):
        try:
            df = pd.read_csv(".\db\patients.csv")
            df = df.loc[
                (df["nom"] != dl_patient_nom) & (df["prenom"] != dl_patient_prenom)
            ]
            df.to_csv(".\db\patients.csv", encoding="utf-8", index=False)
        except:
            QMessageBox.information(
                self,
                "Operation Echoué",
                "Veuillerz réssayer plus tard",
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
            "moniteur_statut": self.moniteur_statut,
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
        self.tableColumns = ["CIN", "Nom", "Prénom", "Moniteur", "Description"]
        self.table_patients.setHorizontalHeaderLabels(self.tableColumns)

    def trigged_buttons(self):
        self.button_deconnecter.clicked.connect(
            lambda: interfaces.setCurrentWidget(main_window)
        )
        self.button_modifier_patient.clicked.connect(lambda: self.goToModifierPatient())
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
                    self.table_patients.setItem(row, 0, QTableWidgetItem(patient[1]))
                    self.table_patients.setItem(row, 1, QTableWidgetItem(patient[2]))
                    self.table_patients.setItem(row, 2, QTableWidgetItem(patient[3]))
                    self.table_patients.setItem(row, 3, QTableWidgetItem(patient[4]))
                    self.table_patients.setItem(row, 4, QTableWidgetItem(patient[7]))
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

    def goToModifierPatient(self):
        try:
            indexRow = self.table_patients.selectedIndexes()[0].row()
            dl_patient_nom = self.patients_liste[indexRow][2]
            dl_patient_prenom = self.patients_liste[indexRow][3]
            modifier_patient.patient_named = dl_patient_nom
            modifier_patient.patient_prenomd = dl_patient_prenom
            print("ok")
            modifier_patient.loadPatientInfo()
        except:
            self.labelEror.setText("Erreur Connection à BD I don't know why")
        else:
            self.labelEror.setText("")
            interfaces.setCurrentWidget(modifier_patient)

    def loadData(self):
        try:
            df = pd.read_csv(".\db\patients.csv")
            self.patients_liste = df.values.tolist()
            rowPosition = self.table_patients.rowCount()
            self.table_patients.insertRow(rowPosition)
            self.table_patients.setRowCount(len(self.patients_liste))
            row = 0
            self.patients_liste.reverse()
            for patient in self.patients_liste:
                self.table_patients.setItem(row, 0, QTableWidgetItem(f"{patient[1]}"))
                self.table_patients.setItem(row, 1, QTableWidgetItem(f"{patient[2]}"))
                self.table_patients.setItem(row, 2, QTableWidgetItem(f"{patient[3]}"))
                self.table_patients.setItem(row, 3, QTableWidgetItem(f"{patient[4]}"))
                self.table_patients.setItem(row, 4, QTableWidgetItem(f"{patient[7]}"))
                row = row + 1
            if len(self.patients_liste) == 0:
                self.labelEror.setText("Not found !")
            else:
                self.labelEror.setText("")
        except:
            self.labelEror.setText("Erreur Connection à BD")


class Patient(QMainWindow):
    patient_name = ""
    patient_prenom = ""
    statutM = ""

    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()

    def loadPatientInfo(self):
        self.labelEror.setText("")
        df = pd.read_csv(".\db\patients.csv")
        df = df[
            (df["nom"] == self.patient_name) & (df["prenom"] == self.patient_prenom)
        ]
        patient_info = df.values.tolist()
        patient_info = patient_info[0]
        self.le_id.setText(str(patient_info[0]))
        if patient_info[0] == "NAN":
            self.le_id.setText("-")
        self.le_cin.setText(str(patient_info[1]))
        self.le_nom.setText(str(patient_info[2]))
        self.le_prenom.setText(str(patient_info[3]))
        self.cb_moniteur.setCurrentText(str(patient_info[4]))
        self.cb_sexe.setCurrentText(str(patient_info[5]))
        self.cb_nationalite.setCurrentText(str(patient_info[6]))
        self.patient_descrption.setText(str(patient_info[7]))
        self.tb_maladie.setText(str(patient_info[8]))

        if str(patient_info[4]) == "Deactive":
            self.statutM = "N"
        else:
            self.statutM = "Y"
        if patient_info[8] == "NAN":
            self.tb_maladie.setText("pas de descrpition")
        try:
            if patient_info[9] != "" and patient_info[9] != "NAN":
                img_link = f"./patients_images/{patient_info[9]}.jpg"
                print(img_link)
                self.iamge_label.setPixmap(QPixmap(img_link))
            elif patient_info[9] == "NAN":
                self.iamge_label.setPixmap(QPixmap("./images/patient.png"))
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
        self.button_moniteur.clicked.connect(lambda: self.goToMoniteur())

    def goToMoniteur(self):
        try:
            moniteur_patient.patient_name = self.patient_name
            moniteur_patient.patient_prenom = self.patient_prenom
            if self.statutM == "N":
                self.labelEror.setText("Patient Don't Have Moniteur")
            elif self.statutM == "Y":
                moniteur_patient.loadPatientInfo()
                self.labelEror.setText("")
                interfaces.setCurrentWidget(moniteur_patient)
        except:
            self.labelEror.setText("Erreur Connection à Moniteur")


class Moniteur(QMainWindow):
    patient_name = ""
    patient_prenom = ""

    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()
        self.start_subscribing()

    def set_temp(self, temp):
        self.temperature_value.display(temp)
        print(f"temp : {temp}")

    def set_spio2(self, spio2):
        self.progressBar_spo2.setValue(int(spio2))
        print(f"Spio2 : {spio2}")

    def set_pulse_rate(self, puls_rate):
        self.puls_rate.display(puls_rate)
        print(f"puls_rate : {puls_rate}")

    def loadPatientInfo(self):
        df = pd.read_csv(".\db\patients.csv")
        df = df[
            (df["nom"] == self.patient_name) & (df["prenom"] == self.patient_prenom)
        ]
        patient_info = df.values.tolist()
        patient_info = patient_info[0]
        self.le_id.setText(str(patient_info[0]))
        if patient_info[0] == "NAN":
            self.le_id.setText("-")
        self.le_cin.setText(str(patient_info[1]))
        self.le_nom.setText(str(patient_info[2]))
        self.le_prenom.setText(str(patient_info[3]))
        self.cb_sexe.setCurrentText(str(patient_info[5]))
        self.cb_nationalite.setCurrentText(str(patient_info[6]))
        try:
            if patient_info[9] != "" and patient_info[9] != "NAN":
                img_link = f"./patients_images/{patient_info[9]}.jpg"
                print(img_link)
                self.iamge_label.setPixmap(QPixmap(img_link))
            elif patient_info[9] == "NAN":
                self.iamge_label.setPixmap(QPixmap("./images/patient.png"))
            self.iamge_label.repaint()
        except:
            pass

    def set_ui(self):
        self.setWindowTitle("Track Health Application")
        self.setGeometry(300, 400, 823, 563)
        self.setFixedSize(823, 563)
        uic.loadUi("./ui/moniteur.ui", self)
        # self.langage.activated[str].connect(self.set_langage)

    def trigged_buttons(self):
        self.button_deconnecter.clicked.connect(
            lambda: interfaces.setCurrentWidget(main_window)
        )
        self.button_retour.clicked.connect(lambda: self.goToPatient())

    def goToPatient(self):
        try:
            dl_patient_nom = self.patient_name
            dl_patient_prenom = self.patient_prenom
            patient_window.patient_name = dl_patient_nom
            patient_window.patient_prenom = dl_patient_prenom
            patient_window.loadPatientInfo()
        except:
            self.labelEror.setText("Erreur Connection à BD")
        else:
            self.labelEror.setText("")
            interfaces.setCurrentWidget(patient_window)

    def start_subscribing(self):
        self.thread = MqttApp()
        self.thread.temp.connect(self.set_temp)
        self.thread.spio2.connect(self.set_spio2)
        self.thread.pulse_rate.connect(self.set_pulse_rate)
        self.thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    interfaces = QStackedWidget()
    interfaces.setWindowIcon(QtGui.QIcon("./images/icon.png"))
    main_window = Main()
    login_window = Login()
    patient_window = Patient()
    patients_window = Patients()
    ajoute_patient = AjoutPatient()
    modifier_patient = ModifierPatient()
    moniteur_patient = Moniteur()
    interfaces.addWidget(main_window)
    interfaces.addWidget(login_window)
    interfaces.addWidget(patient_window)
    interfaces.addWidget(patients_window)
    interfaces.addWidget(ajoute_patient)
    interfaces.addWidget(modifier_patient)
    interfaces.addWidget(moniteur_patient)
    interfaces.show()
    interfaces.setWindowTitle("Track Health Application")
    interfaces.setFixedSize(823, 563)
    interfaces.setGeometry(180, 120, 823, 563)

    try:
        app.exec_()
    except:
        print("closing...")
