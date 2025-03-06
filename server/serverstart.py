import secrets
import b92
import self as self
from flask import Flask, request
from flask_socketio import SocketIO
import time
from threading import Timer
import AES
import sql
class MyFlaskApp:
    def __init__(self):
        self.connected_sockets = {}
        self.connected_AES={}
        self.connected_Auth={}
        self.connected_name={}
        self.bob_basis={}
        self.bob_res={}
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app,engineio_logger=False)
        self.ip_lst=set()
        self.app.add_url_rule('/status', 'status', self.status, methods=['GET'])
        self.app.add_url_rule('/send', 'send_sms', self.send_sms, methods=['POST'])
        self.socketio.on_event('connect', self.handle_connect)
        self.socketio.on_event('disconnect', self.handle_disconnect)
        self.socketio.on_event('status',self.status)
        self.socketio.on_event('key_AES',self.key_AES)
        self.socketio.on_event('reg_data',self.reg_data)
        self.socketio.on_event("auth_data",self.auth)
        self.socketio.on_event("push",self.push)
        self.socketio.on_event("key_bb",self.push_push)
        self.block_size = 16
        self.AES=AES.AES()
        self.sql=sql.SQL()
        #self.socketio.on_event('status',self.status)
        Timer(60, self.check_socket_activity).start()
    def handle_connect(self):
        self.client_ip = request.remote_addr
        sid = request.sid
        print(f'Client connected: {sid}' + " " + self.client_ip)
        self.connected_sockets[sid] = True
        AES_Key= self.AES.generate_random_key()
        self.connected_AES[sid]=AES_Key
    def handle_disconnect(self):
        sid = request.sid
        print(f'Client disconnected: {sid}')
        self.connected_sockets.pop(sid, None)
        self.connected_AES.pop(sid,None)
        self.connected_Auth.pop(sid,None)
    def handle_connect_list(self):
        connected_clients = list(self.socketio.server.manager.connected)
        print(f'Connected clients: {connected_clients}')
    def key_AES(self):
        sid = request.sid
        self.socketio.emit("key_AES",self.connected_AES[sid],room=sid)
    def status(self):

        sid = request.sid
        print("Отправил статус клиенту "+ str(sid))
        self.socketio.emit('status', {
            'status': True,
            'name': 'Lmes',
            'time': time.time(),
            'version': '0.01'
        },room=sid)
    def reg_data(self, data):
        sid=request.sid
        print("Принял  регистрационные данные шифрованные данные и записал в базу")

        name=data["name"]
        firstname=data["firstname"]
        login=data["login"]
        password=data["password"]
        #print(self.connected_AES[sid])
        name=(self.AES.decrypt(name,self.connected_AES[sid].encode("ASCII")))
        firstname=(self.AES.decrypt(firstname,self.connected_AES[sid].encode("ASCII")))
        login=(self.AES.decrypt(login,self.connected_AES[sid].encode("ASCII")))
        password=(self.AES.decrypt(password,self.connected_AES[sid].encode("ASCII")))
        #print(name)
        self.sql.reg_auth(name,firstname,login,password)
    def auth(self,data):
        sid = request.sid
        login = (self.AES.decrypt(data["login"],self.connected_AES[sid].encode("ASCII")))
        password = (self.AES.decrypt(data["password"], self.connected_AES[sid].encode("ASCII")))
        print(login+password)
        a,b,c=self.sql.auth_start(login, password)

        if a ==True:
            print("Отправил запрос на авторизацию" )
            self.socketio.emit("auth_yes",{"status":True,"name":str(b)+ " "+ str(c)},room=sid)
            self.connected_Auth[sid]=True
            self.connected_name[sid]=str(b)+" "+  str(c)
        else:
            self.socketio.emit("auth_yes",{'status': False}, room=sid)

    def push(self,data):
        sid=request.sid
        if sid not in self.connected_Auth:
            return
        bob_results=b92.bob_measure_qubits(data['alice_qubits'])
        bob_b=b92.bob_announce_basis(bob_results)
        self.bob_res[sid]=bob_results
        self.bob_basis[sid]=bob_b
        self.socketio.emit('rush_2',bob_results,room=sid)
    def xor_cipher(self,str, key):
        encript_str = ""
        i=0
        for letter in str:
            encript_str += chr(ord(letter) ^ int(key[i]))
            i+=1
        return encript_str
    def push_push(self,data):
        sid = request.sid
        a=data["key"]
        b=data["text"]
        a=(self.AES.decrypt(a,self.connected_AES[sid].encode("ASCII")))
        b=self.xor_cipher(b,a)
        for key in self.connected_Auth.keys():
            print(1)
            self.socketio.emit("sms",{"sms": self.AES.encrypt(b,self.connected_AES[key].encode("ASCII")),"name":self.connected_name[key]},room=sid)

        # Функция, которая проверяет активность сокетов и удаляет неактивные
    def check_socket_activity(self):
        for sid, active in list(self.connected_sockets.items()):
            if not active:
                print(f"Removing inactive client with SID: {sid}")
                self.connected_sockets.pop(sid, None)
        for sid, active in list(self.connected_AES.items()):
            if not active:
                self.connected_AES.pop(sid, None)
        # Запускаем таймер снова
        print("Чистка пустых sid ")
        Timer(60, self.check_socket_activity).start()
    def send_sms(self):
        try:
            data = request.json
            name = data['name']
            text = data['text']

            if not isinstance(name, str) or not isinstance(text, str):
                return self.app.abort(400)

            if name == "" or text == "":
                return self.app.abort(400)

            if set(data.keys()) != {'name', 'text'}:
                return self.app.abort(400)

            return {'ok': True}
        except:
            return {'ok': False, 'code': self.app.abort(400)}

    def run(self):
        self.socketio.run(self.app, host='127.0.0.1'
                                         , port=5001, debug=True)

if __name__ == '__main__':
    my_app = MyFlaskApp()
    my_app.run()
