import time

import requests
import clientui
from PyQt6 import QtWidgets,QtCore
from PyQt5.QtCore import Qt
import sys


class Messenger(clientui.Ui_LMessenger,QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        try :
            self.pushButton.pressed.connect(self.send_message)
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.get_messages)
            self.timer.start(3000)

        except  Exception as e:
            # TODO server killer
            print("Error server killer __init__ ",e)

    def keyPressEvent(self, event):

        print('press')
        if event.key() == Qt.Key_Return:
            print('success')
            self.send_message()
    def sms_last(self):
        try:
            response = requests.get(
                'http://195.43.142.160:5000/last',


            )
            messages = response.json()['messages']
            for sms in messages:
                self.print_message(sms)
                after = sms['time']
        except  Exception as e:
            # TODO server killer
            print("Error server killer last sms ", e)
            return

    def send_message(self):
        name = self.lineEdit.text()
        sms = self.textEdit.text()
        try:
            print(name,sms)
            response=requests.post(
                'http://195.43.142.160:5000/send',
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
        struct = time.localtime(sms['time'])
        self.textBrowser.append(time.strftime('%d.%m.%Y %H:%M', struct)+" " +
                                sms['name']+"\n"+
                                sms['text'])

    def get_messages(self):
        after =time.time()
        try:
            response = requests.get(
                'http://195.43.142.160:5000/messages',
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
