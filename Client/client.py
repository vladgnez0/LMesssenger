
from PyQt5 import QtWidgets,QtCore
from messenger import Ui_LMessenger
import sys
import  AES
import b92
class mes(QtWidgets.QMainWindow):
    update_signal = QtCore.pyqtSignal(str)
    update_signal_1 = QtCore.pyqtSignal(str)
    def __init__(self,sio):
        super(mes, self).__init__()
        self.ui = Ui_LMessenger()
        self.ui.setupUi(self)
        self.ui.name.setVisible(False)
        self.ui.textBrowser.setText("Вы не авторизованы")
        self.setWindowTitle("Message")
        self.sio = sio
        self.sio.sio.on("auth_yes", self.mes)
        self.sio.sio.on("rush_2", self.rush_2)
        self.sio.sio.on("sms",self.sms)
        self.auth=False
        self.update_signal.connect(self.es)
        self.update_signal_1.connect(self.sms_pushsms)
        self.key = self.sio.key
        self.ui.pushButton.clicked.connect(self.push)
        self.AES= AES.AES()
    def mes(self,data):
        if data['status']==True:
            self.ui.name.setVisible(True)
            self.ui.name.setText(data['name'])
            self.update_signal.emit("Вы авторизованы")
            self.key = self.sio.key
    def es(self, text):
        # Обновляем интерфейс в потоке GUI
        self.ui.textBrowser.setText(text)
    def push(self):
        self.a= self.ui.textEdit.text()
        print('Я на этапе отправки смс '  + self.a)
        self.alice_key, self.alice_qubits =b92.alice_send_qubits(len(self.a)*5)
        self.sio.sio.emit('push',{ 'alice_qubits':self.alice_qubits})

    def xor_cipher(self,str, key):
        encript_str = ""
        i=0
        for letter in str:
            encript_str += chr(ord(letter) ^ int(key[i]))
            i+=1
        return encript_str
    def rush_2(self,data):
        print("2 фаза")
        a= b92.alice_announce_basis(self.alice_qubits,data)
        self.bbkeys=b92.key_exchange(a,self.alice_key)
        print(self.bbkeys)
        #print(self.AES.encrypt(self.bbkeys,self.key.encode('ASCII')))
        #print(type(self.bbkeys))
        print(self.key)
        key=self.AES.encrypt(self.bbkeys,self.key.encode('ASCII'))
        text= self.xor_cipher(self.a,self.bbkeys)
        self.sio.sio.emit("key_bb",{"key":key,"text":text})
    def sms(self,data):
        text=self.AES.decrypt(data["sms"],self.key.encode("ASCII"))
        name =data["name"]
        sms= name + ":"+text
        self.update_signal_1.emit(sms)
    def sms_pushsms(self,str):
        self.ui.textBrowser.append(str)





