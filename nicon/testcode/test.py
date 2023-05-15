import requests
import json

with open("kakao_friend.json","r") as kakao:
    tokens = json.load(kakao)
    print(tokens)

# uuid : ESIXIxojEiASPgY0BDwMNAE0GCAZLxgrGVs
url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 목록 가져오기
header = {"Authorization": 'Bearer ' + tokens["access_token"]}
result = json.loads(requests.get(url, headers=header).text)
friends_list = result.get("elements")
print(friends_list)