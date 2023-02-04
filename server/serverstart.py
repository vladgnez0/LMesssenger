
import flask
from flask import Flask,request
import time
import sql

app= Flask(__name__)

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
        sql_=sql.sql_send()
        sql_.sms_send(message)


        return {'ok': True}
    except:
        return {'ok': False,'code':flask.abort(400)}
after=0
@app.route("/messages")
def get_sms():
    global after
    try:
        result=[]
    except:
      return flask.abort(400)
    a=sql.sql_get()
    b=a.sms_get()
    if b is None:
        return #надо что то придумать
    for sms in b:
        result.append(sms)
    return {'messages':result[:10]}
app.run()
