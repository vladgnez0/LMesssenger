import time

import requests
import clientui
from PyQt6 import QtWidgets,QtCore
import sql
import ip

after = time.time()
class Messenger(clientui.Ui_LMessenger,QtWidgets.QMainWindow):
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

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.send_message()
    def sms_last(self):
        try:
            response = requests.get(
                'http://'+ip.ip+':5000/last',


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
                'http://'+ip.ip+':5000/send',
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
            print("Error not status 200")
            return
        self.textEdit.setText('')

    def print_message(self,sms):
        # print(1)
        struct = time.localtime(sms[2])#date
        self.textBrowser.append(time.strftime('%d.%m.%Y %H:%M', struct)+" " +
                                sms[0]+"\n"+#name
                                sms[1])#sms


    def get_messages(self):
        global after
        try:
            response = requests.get(
                'http://'+ip.ip+':5000/messages',
                params={'after':after})
            messages= response.json()['messages']
            print(messages)
            for sms in messages:
                if after<sms[2]:
                    self.print_message(sms)
                    after=sms[2]#time
        except  Exception as e:
            # TODO server killer
            print("Error server killer get_sms ",e)
            return
    def sms_last(self):
        try:
            response = requests.get(
                'http://' + ip.ip + ':5000/messages')
            messages = response.json()['messages']
            print(messages)
            for sms in messages:
                self.print_message(sms)
        except  Exception as e:
            # TODO server killer
            print("Error server killer get_sms ", e)
            return

