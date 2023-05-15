import requests
import json

url = 'https://kauth.kakao.com/oauth/token'
client_id = '1570f95c9be37f282cfaafd09261554c'
redirect_uri = 'https://localhost:3000'
code = 'LwV1lpI9RG_y_mbx12IZloEf9AQq9VjkLOh7D_lKs9WAkFU-MBCDTuTe9bbD_CO1sVQYggo9c5oAAAGHl9qSvg'

data = {
    'grant_type':'authorization_code',
    'client_id':client_id,
    'redirect_uri':redirect_uri,
    'code': code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print( tokens )
with open("kakao_friend.json", "w") as fp:
    json.dump(tokens, fp)
