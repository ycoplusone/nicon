import requests
import json

#발행한 토큰 불러오기
with open("kakao_friend.json","r") as kakao:
    tokens = json.load(kakao)
    print(tokens)

friend_id = 'ESIXIxojEiASPgY0BDwMNAE0GCAZLxgrGVs'

url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
header = {"Authorization": 'Bearer ' + tokens["access_token"]}
data={
    'receiver_uuids': '["{}"]'.format(friend_id),
    "template_object": json.dumps({
        "object_type":"text",
        "text":"딥러닝 뉴스232",
        "link":{
            "web_url" : "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws",
            "mobile_web_url" : "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws"
        },
        "button_title": "뉴스 보기"
    })
}
response = requests.post(url, headers=header, data=data)
response.status_code