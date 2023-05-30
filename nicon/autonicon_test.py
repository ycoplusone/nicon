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

# 바코드
import pyzbar.pyzbar as pyzbar  # pip install pyzbar
import numpy as np              # pip install numpy
import cv2                      # pip install opencv-python


# 현재 사용하는 모니터의 해상도 출력
#print(pyautogui.size())

# 현재 마우스 커서의 위치 출력
#print(pyautogui.position())

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




#send_telegram_message('문자테스트 입니다.')
def fn_history():
    datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    data = {  
              'authority' : 'api2.ncnc.app'
            , 'accept' : 'application/json, text/plain, */*'
            , 'accept-language' : 'ko,en;q=0.9'
            , 'authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjI1MzMwLCJ0eXBlcyI6Imtha2FvLHBob25lIiwiYmFua0lkIjo0LCJpYXQiOjE2ODE4NjQyNTEsImV4cCI6MTc0NDkzNjI1MX0.7FR1Taz1ukOZntopSAD3A3wp8YRDiokXkQWt1wyJ4E4'
            , 'origin': 'https://ncnc.app'
            , 'referer': 'https://ncnc.app/'
        }

    r_url = 'https://api2.ncnc.app/cons/confirmed?page={}'
    for i in range(1,11):
        url = r_url.format(i)
        print(url)
        response = requests.get(url , headers=data )
        if response.status_code == 200:
            _json = response.json()
            _json_cons = _json['cons']
            dd = dbcon.DbConn()
            for _i in _json_cons:
                _confirmExpireAt =  _i['confirmExpireAt'] if _i['confirmExpireAt'] != None else '1999-12-31T01:01:01.000Z'
                _expireAt        =  _i['expireAt'] if _i['expireAt'] != None else '1999-12-31T01:01:01.000Z'
                _createdAt       =  _i['createdAt'] if _i['createdAt'] != None else '1999-12-31T01:01:01.000Z'
                
                
                param = {
                    'seq':_i['id']
                    , 'askingPrice' : _i['askingPrice']
                    , 'confirmExpireAt' : datetime.strptime( _confirmExpireAt , datetime_format)    
                    , 'expireAt'        : datetime.strptime( _expireAt        , datetime_format)
                    , 'createdAt'       : datetime.strptime( _createdAt       , datetime_format)
                    , 'rejectedReason' : _i['rejectedReason']
                    , 'lastCodeNumber' : _i['lastCodeNumber']
                    , 'currentStatus' : _i['currentStatus']
                }
                _conitem = _i['conItem']
                
                param['prod_id']  = _conitem['id']
                param['prod_nm']  = _conitem['name']
                _conCategory2 = _conitem['conCategory2']
                param['div_id']  = _conCategory2['conCategory1Id']
                param['category_id']  = _conCategory2['id']
                param['category_nm']  = _conCategory2['name']            
                dd.upsert_nicon_sale_info(param)

def send_telegram_message( message ):
    '''텔러그램 판매 발송    '''
    token = '6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc'     
    #-1001813504824 : 우정이 개인방 SEND_TYPE V , VE 일경우 이쪽으로 보낸다.    
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

def fn_find_xy( _str , _region=None):
    __xy = None
    if _region == None :
        __xy = pyautogui.locateOnScreen( _str )
    else :
        __xy = pyautogui.locateOnScreen( _str , region = _region )
    return __xy

def fn_click( _xy , _sleep=2.0 ):
    pyautogui.click(  _xy['x'], _xy['y'])
    time.sleep( _sleep )


            
def fn_main():
    try:
        global base_xy , area_xy , sale_xy , search_xy , nobrand_xy , noitem_xy , additem_xy , exploer_xy , ok_xy
        dd = dbcon.DbConn()        
        base_sleep = 3        
        __lists     = dd.get_nicon_upload_list()

        for list in __lists:
            if len(base_xy) == 0:
                __xy = fn_find_xy('./nicon/basexy.png' )
                base_xy = ( __xy.left-50 , __xy.top , 550 , 1050 )            
                
            print('시작.')
            print(list)
            prod_fold_list = getfolelist( list['fold_nm'] )
            
            for __i in prod_fold_list:
                pyautogui.click(100, 150)
                pyautogui.press('f5')
                time.sleep(base_sleep-1)

                if len(sale_xy) == 0:
                    print('sale_xy 설정')
                    sale_img = fn_find_xy('./nicon/sale.png' , base_xy ) #pyautogui.locateOnScreen('./nicon/sale.png') 
                    sale_xy  = getXyinfo(sale_img)
                    print('sale_xy : ',sale_xy)
                
                fn_click( sale_xy )

                div_img = fn_find_xy( getImg(list['div_nm'] ) , base_xy ) #pyautogui.locateOnScreen( getImg(list['div_nm'] )  )
                div_xy  = getXyinfo(div_img)
                fn_click( div_xy )

                if len(search_xy) == 0:
                    print('search_xy 설정')
                    search_img = fn_find_xy('./nicon/search.png' , base_xy ) #pyautogui.locateOnScreen('./nicon/search.png')
                    search_xy  = getXyinfo(search_img)
                    print('search_xy : ',search_xy)  
                fn_click( search_xy )

                pyperclip.copy(list['category_nm'])
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                time.sleep(base_sleep-1)

                if len(nobrand_xy) == 0:
                    print('nobrand_xy 설정')
                    nobrand_img = fn_find_xy('./nicon/nobrand.png' , base_xy ) #pyautogui.locateOnScreen('./nicon/nobrand.png')
                    nobrand_xy  = getXyinfo(nobrand_img)
                    print('nobrand_xy : ',nobrand_xy)  
                pyautogui.click(  nobrand_xy['x']+140, nobrand_xy['y'])
                time.sleep(base_sleep-1)

                fn_click( search_xy )                       
                pyperclip.copy(list['prod_nm'])
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                time.sleep(base_sleep-2)

                _xy = fn_find_xy('./nicon/reject.png' , base_xy ) #pyautogui.locateOnScreen('./nicon/reject.png')             
                if _xy != None:
                    break
                else:
                    if len(noitem_xy) == 0:
                        noitem_img = fn_find_xy('./nicon/noitem.png' , base_xy ) #pyautogui.locateOnScreen('./nicon/noitem.png')
                        noitem_xy  = getXyinfo(noitem_img)
                        print('noitem_xy : ',noitem_xy)  
                    pyautogui.click(  noitem_xy['x'], noitem_xy['y']+120)
                    time.sleep(base_sleep-1)

                    if len(additem_xy) == 0:
                        additem_img = fn_find_xy('./nicon/additem.png' , base_xy ) #pyautogui.locateOnScreen('./nicon/additem.png')             
                        additem_xy  = getXyinfo(additem_img)
                        print('additem_xy : ',additem_xy)  
                    fn_click(additem_xy)
                    
                    if len(exploer_xy) == 0:
                        exploer_img = fn_find_xy('./nicon/exploer.png') #pyautogui.locateOnScreen('./nicon/exploer.png')             
                        exploer_xy  = getXyinfo(exploer_img)
                        print('exploer_xy : ',exploer_xy)  
                    pyautogui.click(  exploer_xy['x']+60 , exploer_xy['y'] )
                    time.sleep(base_sleep-1)       
                    path_copy = __i
                    pyperclip.copy( path_copy )
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.press('enter')
                    time.sleep(base_sleep-1)

                    pyautogui.click(  exploer_xy['x']+60 , exploer_xy['y']-40)
                    time.sleep(base_sleep-2)

                    pyautogui.hotkey('ctrl', 'a')
                    time.sleep(base_sleep-2)
                    pyautogui.hotkey('alt', 'o')
                    time.sleep(base_sleep-2)
                    if len(ok_xy) == 0:
                        ok_img = fn_find_xy('./nicon/ok.png'  ) #pyautogui.locateOnScreen('./nicon/ok.png')             
                        ok_xy  = getXyinfo(ok_img)
                        print('ok_xy : ',ok_xy) 
                    fn_click( ok_xy )
                    pyautogui.press('enter')
                    time.sleep(base_sleep-2)                
                    telegram_str = ''
                    telegram_str += list['fold_nm']+' : '+str(list['amount'])+'\n'
                    telegram_str += '원본 : '+path_copy+'\n\n'                
                    telegram_str += '완료 : '+complete_fold(path_copy)
                    send_telegram_message(telegram_str)
                    pyautogui.press('enter')
                    time.sleep(base_sleep-2)
    except Exception as e:
        print('fn_main',e)            

def getting_xy():
    global base_xy , area_xy , sale_xy , search_xy , nobrand_xy , noitem_xy , additem_xy , exploer_xy , ok_xy
    __sleep = 3.0

    print('time : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )
    pyautogui.click(100, 150)
    pyautogui.press('f5')
    time.sleep(__sleep-1.7)     

    print('bati : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )    
    __xy = fn_find_xy('./nicon/basexy.png' )
    base_xy = ( __xy.left-50 , __xy.top , 550 , 1050 )       
 
    print('sati : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )    
    sale_img = fn_find_xy('./nicon/sale.png' , base_xy )
    sale_xy  = getXyinfo(sale_img)
    fn_click( sale_xy , __sleep-2.4 )

    print('diti : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )    
    div_img = fn_find_xy( './nicon/1.png' , base_xy )
    div_xy  = getXyinfo(div_img)
    fn_click( div_xy , __sleep-2.4 )

    print('seti : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )        
    search_img = fn_find_xy('./nicon/search.png' , base_xy )
    search_xy  = getXyinfo(search_img)
    fn_click( search_xy , __sleep-2.8 )

    print('bati : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )    
    pyperclip.copy( '스타벅스' )
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep( __sleep-2.8 )    

    print('nbti : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )    
    nobrand_img = fn_find_xy('./nicon/nobrand.png' , base_xy )
    nobrand_xy  = getXyinfo(nobrand_img)
    nobrand_xy['x'] = nobrand_xy['x']+140
    fn_click( nobrand_xy , __sleep-2.5 )

    print('seti : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )    
    fn_click( search_xy , __sleep-2.5 ) 
    pyperclip.copy('오늘의 커피 T')
    #pyperclip.copy('부드러운 디저트 세트 (부드러운 생크림 카스텔라 + 아메리카노 T 2)')    
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(__sleep-2.7)


    print('niti : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )    
    noitem_img = fn_find_xy('./nicon/noitem.png' , base_xy )
    noitem_xy  = getXyinfo(noitem_img)
    noitem_xy['y'] = noitem_xy['y']+120
    fn_click( noitem_xy , __sleep-2.5 )

    
    print('adti : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )    
    additem_img = fn_find_xy('./nicon/additem.png' , base_xy )
    additem_xy  = getXyinfo(additem_img)    
    fn_click(additem_xy , __sleep-2.0 )

    print('exti : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )    
    exploer_img = fn_find_xy('./nicon/exploer.png') #pyautogui.locateOnScreen('./nicon/exploer.png')             
    exploer_xy  = getXyinfo(exploer_img)
    exploer_xy['x'] = exploer_xy['x']+60
    fn_click(exploer_xy , __sleep-2.5 )

    print('pcti : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )    
    path_copy = 'C:\\ncnc\\test.png'
    pyperclip.copy( path_copy )
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(__sleep-1)    

    print('okti : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )    
    ok_img = fn_find_xy('./nicon/ok.png'  )
    ok_xy  = getXyinfo(ok_img)

    
    

    print('time : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )


if __name__ == "__main__":    
        base_xy     = () # 500 , 900
        area_xy     = {}
        sale_xy     = {}
        search_xy   = {}
        nobrand_xy  = {}
        noitem_xy   = {}
        additem_xy  = {}
        exploer_xy  = {}
        ok_xy       = {}    
        
        
        getting_xy()
        print( base_xy , area_xy , sale_xy , search_xy , nobrand_xy , noitem_xy , additem_xy , exploer_xy , ok_xy )



    
    
    