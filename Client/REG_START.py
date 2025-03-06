from PyQt5 import QtWidgets

from REG_UI import Ui_Dialog  # импорт нашего сгенерированного файла
import sys
import AUTH_START
import re
import AES
class REG_UI(QtWidgets.QMainWindow):
    def __init__(self,key,sio):
        super(REG_UI, self).__init__()
        self.setFixedSize(400, 300)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Authentication")
        self.ui.pushButton.clicked.connect(self.back)
        self.ui.pushButton_2.clicked.connect(self.reg)
        self.key=key
        self.sio=sio
        self.AES=AES.AES()
    def back(self):
        self.auth = AUTH_START.AUTH_START(self.sio)
        self.auth.show()
        self.close()
    def reg(self):
        self.name=self.ui.name.text()
        self.firstname=self.ui.First_name.text()
        self.login=self.ui.login.text()
        self.password=self.ui.password_1.text()
        self.password_2=self.ui.password_2.text()

        if not (self.validate_login(self.login) and self.validate_password(self.password)):
            QtWidgets.QMessageBox.critical(self, "Error", "Неправильный формат ввода пароля или логина , не менее 6 символов , должны быть и цифры и буквы")
            return

        if self.password != self.password_2:
            QtWidgets.QMessageBox.critical(self, "Error", "Пароли должны совпадать")
            return
        try:

            reg_data={
                "name":self.AES.encrypt(self.name,self.key.encode("ASCII")),
                "firstname":self.AES.encrypt(self.firstname,self.key.encode("ASCII")),
                "login":self.AES.encrypt(self.login,self.key.encode("ASCII")),
                "password":self.AES.encrypt(self.password,self.key.encode("ASCII")),
            }
            print(reg_data)
            self.sio.sio.emit("reg_data", reg_data)
        except Exception as e:
            print(e)


    def validate_password(self,password):
        if len(password) < 6:
            return False
        if not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password):
            return False
        return True

    def validate_login(self,login):
        if len(login) < 6:
            return False
        return True