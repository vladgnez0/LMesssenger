# Form implementation generated from reading ui file 'StartBAR.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import sys


class Ui_LMessenger(QtWidgets.QMainWindow):
    def setupUi(self, LMessenger):
        LMessenger.setObjectName("LMessenger")
        LMessenger.resize(481, 490)
        self.centralwidget = QtWidgets.QWidget(parent=LMessenger)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 10, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 420, 311, 41))
        self.textEdit.setObjectName("textEdit")
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 90, 451, 311))
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(360, 60, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 60, 101, 20))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(370, 420, 81, 41))
        self.pushButton.setObjectName("pushButton")
        LMessenger.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=LMessenger)
        self.statusbar.setObjectName("statusbar")
        LMessenger.setStatusBar(self.statusbar)

        self.retranslateUi(LMessenger)
        QtCore.QMetaObject.connectSlotsByName(LMessenger)

    def retranslateUi(self, LMessenger):
        _translate = QtCore.QCoreApplication.translate
        LMessenger.setWindowTitle(_translate("LMessenger", "LMessenger"))
        self.label.setText(_translate("LMessenger", "LMessenger"))
        self.label_2.setText(_translate("LMessenger", "Имя пользователя:="))
        self.pushButton.setText(_translate("LMessenger", "Отправить"))



