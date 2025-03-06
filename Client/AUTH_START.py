import json

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QMessageBox



import sys
import socketio
from auth import Ui_Dialog
import REG_START
import  AES
import  client
class AUTH_START(QtWidgets.QMainWindow):
    def __init__(self, sio):
        super(AUTH_START, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Authentication")
        self.ui.reg.clicked.connect(self.register)
        self.ui.window.clicked.connect(self.auth)
        self.setFixedSize(400, 300)
        self.sio = sio
        self.AES = AES.AES()
        self.key = self.sio.key
        self.result = None  # Здесь будет храниться результат диалога
        #print(self.sio.key+ "Fsd")
    def register(self):

        self.reg = REG_START.REG_UI(self.key,self.sio)
        self.animate_transition(self, self.reg)

    def auth(self):
        self.login = self.ui.login.text()
        self.password = self.ui.password.text()
        if (self.login=="")or(self.password==""):
            QtWidgets.QMessageBox.critical(self, "Error", "Введите данные")
            return
        try:

            auth_data = {
                "login": self.AES.encrypt(self.login, self.key.encode("ASCII")),
                "password": self.AES.encrypt(self.password, self.key.encode("ASCII")),
            }
            print("Шифрованные авторизационные данные")
            print(auth_data)
            self.sio.sio.emit('auth_data', auth_data)

        except Exception as e:
            print(e)


    def animate_transition(self, start_widget, end_widget):
        start_geometry = start_widget.geometry()
        end_geometry = end_widget.geometry()

        animation = QtCore.QPropertyAnimation(start_widget, b"geometry")
        animation.setDuration(5000)
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        animation.start()

        animation.finished.connect(end_widget.show)
        animation.finished.connect(start_widget.close)
        end_widget.show()
        start_widget.close()


if __name__ == "__main__":
    # Create a Socket.IO client instance
    sio = socketio.Client()

    # Connect the Flask-SocketIO server
    sio.connect('http://localhost:5001')  # Replace with your server URL

    app = QtWidgets.QApplication([])

    application = AUTH_START(sio)
    application.show()

    sys.exit(app.exec())
