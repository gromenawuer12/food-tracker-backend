import requests

def url(uri):
    return f'http://127.0.0.1:3000/{uri}'

def login():
    response = requests.post(url('users/login'), headers = {
        'Authorization': 'Bearer dGVzdDp0ZXN0'
    })
    return {'Authorization': f"Bearer {response.json()['token']}"}
