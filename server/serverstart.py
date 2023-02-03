
import flask
from flask import Flask,request
import time

app= Flask(__name__)
db=[
       {'time': time.time(),
        'name':'Jack',
        'text':'Привет всем!',

        }

]

@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Lmes',
        'time':time.time(),
        'version':'0.01'

    }

@app.route("/send",methods=['POST'])
def send_sms():
    #POST
    #request.json
    #name ,text
    #validate
    try:
        data = request.json
        name = data['name']
        text=data['text']
        if not isinstance(name,str):
            return flask.abort(400)
        if not isinstance(text,str):
            return flask.abort(400)
        if name =="":
            return flask.abort(400)
        if text == "":
            return flask.abort(400)

        if set(data.keys())!={'name','text'}:
            return flask.abort(400)
        message={
            'time':time.time(),
            'name': name,
             'text':text,

        }
        #print(type(message["time"]))
        db.append(message)
        print(db)
        return {'ok': True}
    except:
        return {'ok': False,'code':flask.abort(400)}
after=0
@app.route("/messages")
def get_sms():
    global after
    try:
        result=[]
        if len(db) > 5:
            db.clear()
    except:
      return flask.abort(400)
    for sms in db:
        if sms in db:
            if sms['time']>after:
                result.append(sms)
                after=sms['time']
    return {'messages':result[:10]}
@app.route("/last")
def last_sms():
    result = []
    for sms in db:
        if sms in db:
                result.append(sms)
    return {'messages':result[-1:-5:-1]}
app.run(host='195.43.142.160')