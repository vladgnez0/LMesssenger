from PyQt5 import QtWidgets
import sys
import socketio
import tkinter.messagebox as mb
import AUTH_START
from PyQt6.QtCore import pyqtSignal, QObject
import  client
class SocketIOClient(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.sio = socketio.Client()
        self.init_socketio()


    def init_socketio(self):
        try:
            self.sio.connect('http://localhost:5001')  # Replace with your server URL
            self.sio.emit('register_event', {'data': 'some_data'})
            self.sio.emit('status')
            self.sio.on('status', self.handle_status)

            self.key=""
            #self.emit("key_AES")

        except Exception as e:
            msg = "Нет связи с сервером"
            mb.showerror("ОШИБКА", msg)
            exit(0)
        self.sio.emit('key_AES')
        self.sio.on("key_AES", self.key_AES)
    def handle_status(self, data):
        print(data )  # Handle the status event
    def key_AES(self,data):
        self.key=data
        print(self.key)
    def mes(self,data):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    socketio_client = SocketIOClient()
    auth_start = AUTH_START.AUTH_START(socketio_client)
    client_start = client.mes(socketio_client)
    auth_start.show()
    client_start.show()
    sys.exit(app.exec())
