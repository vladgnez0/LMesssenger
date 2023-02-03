import time
import requests
from PyQt6 import QtWidgets,QtCore
import login
class Login(QtWidgets.QMainWindow,login.Ui_login,):
    def __init__(self):
        print(3)
        super().__init__()
        self.setupUi(self)

