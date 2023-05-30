import pyautogui
import pyperclip
import os
import shutil
from datetime import datetime
import time

import pyzbar.pyzbar as pyzbar  # pip install pyzbar
import cv2                      # pip install opencv-python
import numpy as np

import dbcon
import requests

def getXyinfo( obj ):
    ''' Box(left=802, top=139, width=80, height=82) 값 받아서 x , y 좌표 리턴 '''
    x = obj.left + (obj.width / 2 )
    y = obj.top + (obj.height /2)
    return {'x' : x , 'y' : y}

def send_telegram_message( message ):
    '''텔러그램 판매 발송
    '''
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

def complete_fold(path):
    '''해당 path 의 이름 변경'''
    #base_dttm = datetime.today().strftime('%Y%m%d%H%M') 
    base_dttm = datetime.today().strftime('%Y%m%d%H%M%S')
    __path = path+'_'+base_dttm+'(완료)'
    os.rename( path , __path)
    return __path

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
    
def base_fold_create():
    base_root = 'c:\\ncnc'
    dd = dbcon.DbConn()
    list = dd.get_nicon_fold_list()
    for i in list:
        try :
            os.mkdir(base_root+'\\'+i['fold_nm'])
        except Exception as e:
            print( 'base_fold_create' , e ) 

def getfolelist(str):
    base = 'c:\\ncnc'
    path_str = base+'\\'+str
    __list = os.listdir( path_str )
    temp_list = [ X for X in __list if os.path.isdir(path_str+'\\'+X)]
    list = [ path_str+'\\'+X for X in temp_list if X[-4:-1] != '(완료']
    return list    

def getCheck():
    '''판매가능한 바코드들이 있는지 확인한다'''
    _return_val = 0
    __base = 'c:\\ncnc'    
    __lists = os.listdir( __base )
    for i in __lists:        
        _dirs = os.listdir( __base+'\\'+i )        
        _temp_list = [ X for X in _dirs if os.path.isdir( __base +'\\'+ i +'\\'+ X )]
        _target_list = [ X for X in _temp_list if X[-4:-1] != '(완료']
        #print(  '처리폴더개수(', len(_target_list) , ') : ' , i )
        _return_val += len(_target_list)        
    return _return_val 

def decode(im):
    '''Find barcodes and QR codes
    바코드 탐지하는 엔진 (바코드 및 QR코드 탐지)
    ''' 
    _str = None
    try:
        decodedObjects = pyzbar.decode(im)        
        for obj in decodedObjects:
            _str = obj.data.decode('utf-8')        
    except Exception as e:
        print(e)
        return None
    return _str

def init_fold(str):
    try:
        '''폴더 정리.'''
        dd = dbcon.DbConn()
        rootlist = os.listdir(str)
        rootdirs = [X for X in rootlist if os.path.isdir(str+'\\'+X)]
        for i in rootdirs:        
            dirname = str+'\\'+i
            base_dttm = datetime.today().strftime('%Y%m%d_%H%M_')        
            listdir = os.listdir(dirname)

            path_files =  [ os.path.join(dirname, x)  for x in listdir ]        
            file_names =  [ X for X in path_files if os.path.isfile(X)]
            file_nm    =  [ x for x in listdir ]
                
            cnt = 1 # 폴더 카운트        
            while( len(file_names) > 0):
                default_fold_nm = base_dttm+(repr(cnt).zfill(2))
                prod_fold       = base_dttm+(repr(cnt).zfill(2))
                v_range = 0
                # 30개씩 볼더 복사 
                if len(file_names) >= 30:
                    default_fold_nm = dirname+'\\'+default_fold_nm+'_30' 
                    prod_fold       = prod_fold+'_30' 
                    v_range = 30       
                else :
                    default_fold_nm = dirname+'\\'+default_fold_nm+'_'+repr( len(file_names) ).zfill(2)
                    prod_fold       = prod_fold+'_'+repr( len(file_names) ).zfill(2)
                    v_range = len(file_names)
                    
                os.mkdir(default_fold_nm)
                
                for j in range(v_range):                
                    __full_path = file_names[0]
                    __file_nm = os.path.basename(__full_path) 
                    __n = np.fromfile(__full_path, np.uint8)
                    __img = cv2.imdecode(__n, cv2.IMREAD_COLOR)
                    __barcode = decode(__img)               
                    param = {'base_fold':i , 'prod_fold':prod_fold ,'file_nm':__file_nm,'barcode': __barcode }
                    dd.insert_nicon_barcode(param)
                    shutil.move(file_names[0] , default_fold_nm )
                    del file_names[0]
                    del file_nm[0]        
                cnt = cnt+ 1
    except Exception as e:
        print('init_fold : ',e)
            

def fn_find_xy( _str , _region=None):
    __xy = None
    if _region == None :
        __xy = pyautogui.locateOnScreen( _str )
    else :
        __xy = pyautogui.locateOnScreen( _str , region = _region )
    return __xy

def fn_click( _xy ):
    pyautogui.click(  _xy['x'], _xy['y'])
    time.sleep( 2 )

def fn_main():
    try:
        dd = dbcon.DbConn()        
        base_sleep = 3
        base_xy     = () # 500 , 900
        area_xy     = {}
        sale_xy     = {}
        search_xy   = {}
        nobrand_xy  = {}
        noitem_xy   = {}
        additem_xy  = {}
        exploer_xy  = {}
        ok_xy       = {}
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


if __name__ == "__main__":   
    # 기본폴더 생성
    print('기본폴더 생성','-'*10)
    base_fold_create()
    time.sleep(5)
    while(True):
        print('시작',datetime.today().strftime('%Y-%m-%d %H:%M:%S'),'-'*10)
        check = getCheck()
        try:
            if check >= 1:
                print('\t판매시작','-'*10)
                fn_main()            
            else:
                # 기본폴더 내 이미지 정리
                print('\t이미지 정리','-'*10)
                init_fold('c:\\ncnc')
            time.sleep(15)
        except Exception as e:
            print('while error',e)
