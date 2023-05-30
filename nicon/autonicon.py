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
    __lists = [ i for i in __lists if os.path.isdir( __base +'\\'+ i )]
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
                # 10개씩 볼더 복사 
                if len(file_names) >= 10:
                    default_fold_nm = dirname+'\\'+default_fold_nm+'_10' 
                    prod_fold       = prod_fold+'_10' 
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

def fn_click( _xy , _sleep=2.0 ):
    pyautogui.click(  _xy['x'], _xy['y'])
    time.sleep( _sleep )

def fn_main():
    try:
        global base_xy , area_xy , sale_xy , search_xy , nobrand_xy , noitem_xy , additem_xy , exploer_xy , ok_xy
        dd = dbcon.DbConn()        
        base_sleep = 3        
        __lists    = dd.get_nicon_upload_list()
        pyautogui.click(100, 150)
        pyautogui.press('f5') 
        time.sleep(base_sleep-1.5)  

        for list in __lists:                
            print('시작.')
            print('list' , list )
            category_nm = list['category_nm']
            prod_nm = list['prod_nm']
            prod_fold_list = getfolelist( list['fold_nm'] )
            print('category_nm : ',category_nm,' , prod_nm : ',prod_nm,' , fold_nm : ' , prod_fold_list )
            
            for __i in prod_fold_list:
                pyautogui.click(100, 150)
                pyautogui.press('f5')
                time.sleep(base_sleep-1.7)

                #기프티콘 판매 클릭
                fn_click( sale_xy , base_sleep-2.4 )
                
                #대분류 클릭
                div_img = fn_find_xy( getImg(list['div_nm'] ) , base_xy )
                div_xy  = getXyinfo(div_img)
                fn_click( div_xy , base_sleep-2.4 )

                #검색창 클릭
                fn_click( search_xy , base_sleep-2.8 )

                #브랜드명 조회
                pyperclip.copy( category_nm )
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                time.sleep(base_sleep-2.8)

                #브랜드 클릭
                fn_click( nobrand_xy , base_sleep-2.5 )

                #검색창 클릭
                fn_click( search_xy , base_sleep-2.8 )

                #상품명 조회
                pyperclip.copy( prod_nm )
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                time.sleep(base_sleep-2.8)
               
                #상품 클릭
                fn_click( noitem_xy , base_sleep-2.5 )

                # 기프티콘 추가 윈도우 탐색기 호출
                fn_click(additem_xy , base_sleep-2.0 )
                
                # 탐색기 텍스트 부분
                fn_click(exploer_xy , base_sleep-2.8 )
                
                # 해당 폴더로 이동
                path_copy = __i
                pyperclip.copy( path_copy )
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                time.sleep(base_sleep-1.5)

                # 탐색기 텍스트 바로 위 클릭
                pyautogui.click(  exploer_xy['x'] , exploer_xy['y']-40)
                time.sleep(base_sleep-2.5)

                # 해당 폴더의 파일 전체 선택
                pyautogui.hotkey('ctrl', 'a')                
                time.sleep(base_sleep-2.0)
                pyautogui.hotkey('alt', 'o')
                time.sleep(base_sleep-2.7)
                fn_click( ok_xy , base_sleep-1.0)

                test = None #fn_find_xy('./nicon/except.png' )
                if test != None:
                    '''예외 발생'''
                    telegram_str = '오류\n'
                    telegram_str += list['fold_nm']+' : '+str(list['amount'])+'\n'
                    telegram_str += '원본 : '+path_copy+'\n\n'
                    send_telegram_message(telegram_str)
                    pyautogui.press('enter')
                else : 
                    telegram_str = '정상\n'
                    telegram_str += list['fold_nm']+' : '+str(list['amount'])+'\n'
                    telegram_str += '원본 : '+path_copy+'\n\n'
                    telegram_str += '완료 : '+complete_fold(path_copy)
                    send_telegram_message(telegram_str)
                    pyautogui.press('enter')
                    time.sleep(base_sleep-2.8)
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

    #test = fn_find_xy('./nicon/except.png' )
    #test_xy  = getXyinfo(test)
    #print(test,test_xy)

    print('time : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )


if __name__ == "__main__":   
    base_xy     = ()
    area_xy     = {}
    sale_xy     = {}
    search_xy   = {}
    nobrand_xy  = {}
    noitem_xy   = {}
    additem_xy  = {}
    exploer_xy  = {}
    ok_xy       = {}   

    
    # 기본폴더 생성
    print('기본폴더 생성','-'*10)
    base_fold_create()

    print('이미지 정리','-'*10)
    init_fold('c:\\ncnc')    
    
    # 기본 좌표 생성
    getting_xy()

    time.sleep(5)
    while(True):
        print('시작',datetime.today().strftime('%Y-%m-%d %H:%M:%S'),'-'*10)
        check = getCheck()
        try:
            if check >= 1:
                print('판매시작','-'*10)
                fn_main()            
            time.sleep(10)
        except Exception as e:
            print('while error',e)
