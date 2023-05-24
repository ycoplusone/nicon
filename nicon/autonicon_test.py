'''
RPA 작업
pip install pyautogui
pip install opencv-python
'''
import pyautogui
import pyperclip
import os
import shutil
from datetime import datetime
import time

import dbcon
import logging
import requests

# 현재 사용하는 모니터의 해상도 출력
print(pyautogui.size())

# 현재 마우스 커서의 위치 출력
print(pyautogui.position())

# 
#pyautogui.mouseInfo()


# 절대 좌표로 이동
#pyautogui.moveTo(100, 100)                 # 100, 100 위치로 즉시 이동
#pyautogui.moveTo(500, 500, duration=0.5)   # 200, 200 위치로 0.5초간 이동

# 상대 좌표로 이동
#pyautogui.move(100, 100, duration=1)    # 현재 위치 기준으로 100, 100만큼 1초간 이동
#pyautogui.moveTo(100, 100, duration=0.5)   # 200, 200 위치로 0.5초간 이동


#pyautogui.click(200, 200)

#pyautogui.click(x=200,y=200 , clicks=2 , interval=0.5 , button='left')

#pyautogui.click(500, 500)
#pyautogui.write('Hello world!', interval=0.2)
#pyautogui.write(['H', 'e', 'l', 'l', 'o'], interval=0.2)

# 캐쳐이미지로 좌표 찾기

def getXyinfo( obj ):
    ''' Box(left=802, top=139, width=80, height=82) 값 받아서 x , y 좌표 리턴 '''
    x = obj.left + (obj.width / 2 )
    y = obj.top + (obj.height /2)
    return {'x' : x , 'y' : y}

def getImg( str ):
    if str == '카':
        return './nicon/1.png'
    elif str == '편':
        return './nicon/2.png'
    elif str == '빵':
        return './nicon/3.png'
    elif str == '피':
        return './nicon/4.png'
    elif str == '문':
        return './nicon/5.png'
    elif str == '외':
        return './nicon/6.png'    
    elif str == '백':
        return './nicon/7.png'    

def getfolelist(str):
    base = 'c:\\ncnc'
    path_str = base+'\\'+str
    __list = os.listdir( path_str )
    temp_list = [ X for X in __list if os.path.isdir(path_str+'\\'+X)]
    list = [ path_str+'\\'+X for X in temp_list if X[-4:-1] != '(완료']
    return list

def complete_fold(path):
    '''해당 path 의 이름 변경'''
    os.rename( path , path+'(완료)')

#test_img = pyautogui.locateOnScreen('./nicon/1.png') 
#print( getXyinfo(test_img)['x'] )

#_xy = pyautogui.locateOnScreen('./nicon/reject.png')             
#print(_xy != None)
def base_fold_create():
    base_root = 'c:\\ncnc'
    dd = dbcon.DbConn()
    list = dd.get_nicon_fold_list()
    for i in list:
        try :
            os.mkdir(base_root+'\\'+i['fold_nm'])
        except Exception as e:
            print( 'base_fold_create' , e ) 


def send_telegram_message( message ):
    token = '6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc' 
    '''
    -1001813504824 : 우정이 개인방 SEND_TYPE V , VE 일경우 이쪽으로 보낸다.
    '''
    base_dttm = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    try: 
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
        data = {'chat_id': '-1001813504824', 'text': base_dttm+'\n'+message}
        response = requests.post(url, data=data)
        time.sleep(0.5)
        print( 'send_telegram_message : ' , response.json() )               
    except Exception as e:
        print( 'telegram_send', e )
    finally:
        pass

send_telegram_message('문자테스트 입니다.')