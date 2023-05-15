import requests
import json

#발행한 토큰 불러오기
with open("kakao_code.json","r") as kakao:
    tokens = json.load(kakao)
    print(tokens)

url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

headers={
    "Authorization" : "Bearer " + tokens["access_token"]
}

data = {
       'object_type': 'text',
       'text': '니콘내콘fkfkfkfk',
       'link': {
           'web_url': 'https://ncnc.app/sell',
           'mobile_web_url': 'https://ncnc.app/sell'
       },
       'button_title': '키워드'
   }

data = {'template_object': json.dumps(data)}
print(data)
response = requests.post(url, headers=headers, data=data)
response.status_code