from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt5 import uic, QtGui
import sys
import pandas as pd


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.trigged_buttons()

    def set_ui(self):
        self.setWindowTitle("Track Health Application")
        self.setGeometry(39, 30, 716, 544)
        self.setFixedSize(716, 544)
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
        self.setGeometry(39, 30, 716, 544)
        self.setFixedSize(716, 544)
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
            else:
                QMessageBox.warning(
                    self, "connection verfier", "Bonne santé à vos patients"
                )
        except:
            QMessageBox.warning(
                self,
                "connection interrompue",
                "échec de la connexion à la base de données",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    interfaces = QStackedWidget()
    interfaces.setWindowIcon(QtGui.QIcon("./images/icon.png"))
    main_window = Main()
    login_window = Login()
    interfaces.addWidget(main_window)
    interfaces.addWidget(login_window)
    interfaces.show()
    interfaces.setWindowTitle("Track Health Application")
    interfaces.setGeometry(39, 30, 716, 544)
    interfaces.setFixedSize(716, 544)

    try:
        app.exec_()
    except:
        print("closing...")
