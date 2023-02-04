
from PyQt6 import QtWidgets,QtCore
import sys
import loginstart
import messenger
app = QtWidgets.QApplication(sys.argv)
window = messenger.Messenger()
print(type(window))
window.show()
window.sms_last()
app.exec()
