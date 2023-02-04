from flask import Flask
from flaskext.mysql import MySQL

class sql():
    def __init__(self):
        super().__init__()
        self.app_=app = Flask(__name__)
        self.mysql = MySQL(app)
        self.app_.config['MYSQL_DATABASE_USER'] = 'pma'
        self.app_.config['MYSQL_DATABASE_PASSWORD'] = 'lol228'
        self.app_.config['MYSQL_DATABASE_HOST'] = '195.43.142.160'

        self.mysql.init_app(app)
    def mysql_(self):
        return

class sql_get(sql):
    def __init__(self):
        super().__init__()
        self.app_.config['MYSQL_DATABASE_DB'] = 'sms_user'
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sms_test VALUES('vity2', '1','2')")
        conn.commit()
a=sql_get()