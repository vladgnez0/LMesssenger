import time

import requests
from PyQt6 import QtWidgets,QtCore
import sys
import clientui
import datetime


class Messenger(clientui.Ui_LMessenger):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        try :
            self.pushButton.pressed.connect(self.send_message)
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.get_messages)
            self.timer.start(1000)
        except  Exception as e:
            # TODO server killer
            print("Error server killer __init__ ",e)
            return
    def send_message(self):
        name = self.lineEdit.text()
        sms = self.textEdit.toPlainText()
        try:
            print(name,sms)
            response=requests.post(
                'http://127.0.0.1:5000/send',
                json={
                    'name':name,
                    'text':sms
                }

            )
        except  Exception as e:
            # TODO server killer
            print("Error server killer send_message ",e)
            return
        if response.status_code!=200:
            # TODO server killer
            print("Error")
            return
        self.textEdit.setText('')
    def print_message(self,sms):
        self.textBrowser.append(sms['name']+" "+ sms['text'])
    def get_messages(self):
        after =time.time()
        try:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after':after}

            )
            messages= response.json()['messages']
            for sms in messages:
                self.print_message(sms)
                after=sms['time']
        except  Exception as e:
            # TODO server killer
            print("Error server killer get_sms ",e)
            return


app = QtWidgets.QApplication(sys.argv)
window = Messenger()
window.show()
print(type(window))
app.exec()
