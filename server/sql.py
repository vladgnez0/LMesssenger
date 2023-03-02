from flask import Flask
from flaskext.mysql import MySQL

class sql():
    def __init__(self):
        super().__init__()
        try:
            self.app_=app = Flask(__name__)
            self.mysql = MySQL(app)
            self.app_.config['MYSQL_DATABASE_USER'] = 'pma'
            self.app_.config['MYSQL_DATABASE_PASSWORD'] = 'lol228'
            self.app_.config['MYSQL_DATABASE_HOST'] = '195.43.142.160'
            self.app_.config['MYSQL_DATABASE_DB'] = 'sms_user'
            self.mysql.init_app(app)
            self.conn = self.mysql.connect()
            self.cursor = self.conn.cursor()
        except :
            print("Error sql init ")
    def mysql_(self):
        return

class sql_get(sql):
    def __init__(self):
        super().__init__()
        try:

            self.cursor = self.conn.cursor()
        except :
            print("Error sql_get init ")
    def sms_get(self):
        try:
            self.cursor.execute("SELECT *\
                                    FROM sms_test \
                                    ORDER BY Time DESC\
                                    LIMIT 5")
            data = self.cursor.fetchall()
            return data
        except :
            print("Error sql_get init ")
            return None
class sql_send(sql):
    def __init__(self):
        super().__init__()
    def sms_send(self,sms):
        print("Новый запрос на добавление в базу данных ")
        try:
            self.cursor.execute(f"INSERT INTO sms_test "
                                f"VALUES ('{sms['name']}', '{sms['text']}', {sms['time']});")
            self.conn.commit()
        except Exception as e:
            print(e)

