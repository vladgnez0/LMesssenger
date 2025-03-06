import  requests

data={

    'name':'Nick',
    'text':'Привет',

}

respons=requests.get("http://127.0.0.1:5000/status")
print(respons.status_code)
print(respons.json()['status'])