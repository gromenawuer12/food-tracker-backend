import requests,base64, json, sys

def test_get_user_none_authorization():
    response = requests.get("http://python:5000/users/John")
    assert response.status_code == 200
    assert json.loads(response.content).keys() == {"username"}

def test_get_different_user_authorizated():
    credentials = base64.b64encode(b"test:test").decode('utf-8')
    token = json.loads(requests.post("http://python:5000/users/login",headers={"Authorization": f"Basic {credentials}"}).content.decode("utf-8"))['token']
    response = requests.get("http://python:5000/users/John",headers={'Authorization': 'access_token '+token})

    assert response.status_code == 200
    assert json.loads(response.content).keys() == {"username","role"}

def test_get_same_user_authorizated():
    credentials = base64.b64encode(b"test:test").decode('utf-8')
    token = json.loads(requests.post("http://python:5000/users/login",headers={"Authorization": f"Basic {credentials}"}).content.decode("utf-8"))['token']
    response = requests.get("http://python:5000/users/test",headers={'Authorization': 'access_token '+token})

    assert response.status_code == 200
    assert json.loads(response.content).keys() == {"username","password","role"}

def test_add_user():
    response = requests.post("http://python:5000/users/",json={"username":"test111112312____2123username","password":"aaa","role":"test_role"})
    assert response.status_code == 200

def test_add_user_400_scace():
    response = requests.post("http://python:5000/users/",json={"username":"test nick_name12","password":"aaa","role":"test-role"})
    assert response.status_code == 400

def test_add_user_400_dash():
    response = requests.post("http://python:5000/users/",json={"username":"test-nickn32ame","password":"aaa","role":"test-role"})
    assert response.status_code == 400

def test_add_user_already_exists():
    response = requests.post("http://python:5000/users/",json={"username":"John","password":"aaa","role":"test-role"})
    assert response.status_code == 409

def test_login():
    credentials = base64.b64encode(b"test:test").decode('utf-8')
    response = requests.post("http://python:5000/users/login",headers={"Authorization": f"Basic {credentials}"})
    assert response.status_code == 200

def test_update():
    credentials = base64.b64encode(b"test:test").decode('utf-8')
    token = json.loads(requests.post("http://python:5000/users/login",headers={"Authorization": f"Basic {credentials}"}).content.decode("utf-8"))['token']
    
    response = requests.put("http://python:5000/users/test",headers={'Authorization': 'access_token '+token},json={"new_password":"aaa"})

    assert response.status_code == 200