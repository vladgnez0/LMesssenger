import  sqlite3

class SQL():
    def __init__(self):
        self.connection = sqlite3.connect('auth.db')
        self.cursor = self.connection.cursor()
    def reg_auth(self,name_,firstname_,login_,password_):
        try:
            self.cursor.execute(f'INSERT INTO Users (name, firstname , login, password) VALUES ("{name_}", "{firstname_}", "{login_}", "{password_}")' )
            self.connection.commit()
            return True
        except:
            return False
    def auth_start(self,login_,  password):
        #print(login_+ password)
        self.cursor.execute(f'SELECT name, firstname, login, password FROM Users WHERE login = "{login_}"')
        res= self.cursor.fetchone()
        #print(res[3])
        if res:
            if password==res[3]:
                print("Password"
                      "")
                return True,res[0],res[1]
            else:
                return False,None,None
        else:
            return False,None,None


