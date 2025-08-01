from datetime import datetime
from PIL import ImageGrab , Image # pip install pillow
import os
import shutil
import numpy as np
import pyzbar.pyzbar as pyzbar  # pip install pyzbar
import cv2                      # pip install opencv-python
import requests
import time
from pytz import timezone
#from pytz import timezone




def mk_image():
    '''캡쳐 만들기'''
    try:
        base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d_%H%M%S')
        img = ImageGrab.grab()
        imgCrop = img.crop()
        file_name = 'c:\\ncnc\\{}{}'.format(base_dttm,'.png')
        imgCrop.save(file_name)
    except Exception as e:
        print('mk_image : ',e)

def getNow():
    '''현재시간 '''
    return datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')

def getNowDate():
    '''현재 시간 datetime type 으로 리턴'''
    return datetime.now() 

def get1HourOver( _v_datetime : datetime ):
    '''1시간 이상 초과 확인'''
    _rt = False
    time_difference = getNowDate() - _v_datetime
    if ( ( time_difference.seconds // 3600 ) >= 1): # 마지막 메세지 발송후 1시간 이상 True를 리턴한다.
        _rt = True

    return _rt


def decode(im):
    '''Find barcodes and QR codes
    바코드 탐지하는 엔진 (바코드 및 QR코드 탐지)
    ''' 
    _str = None
    try:
        decodedObjects = pyzbar.decode(im)        
        for obj in decodedObjects:
            _str = obj.data.decode('utf-8') 
            print(_str)       
    except Exception as e:
        print(e)
        return None
    return _str

def base_fold_create( _dbconn ):
    '''기본폴더 생성'''
    base_root = 'c:\\ncnc'    
    list = _dbconn.get_nicon_fold_list()
    for i in list:
        try :
            os.mkdir(base_root+'\\'+i['fold_nm'])
        except Exception as e:
            '''이미 만들어 져있으면 오류가 발생'''
            #print( 'base_fold_create' , e ) 

def into_rename_barcode():
    '''파일명 바코드로 변환'''
    try:
        ''''''
        str = 'c:\\ncnc'  
        rootlist = os.listdir(str)
        rootdirs = [X for X in rootlist if os.path.isdir(str+'\\'+X)]
        for i in rootdirs:        
            dirname = str+'\\'+i            
            listdir = os.listdir(dirname)
            path_files =  [ os.path.join(dirname, x)  for x in listdir ]        
            file_names =  [ X for X in path_files if os.path.isfile(X)]
            file_nm    =  [ x for x in listdir ]                
            uniq = 1
            for ii in file_names:               
                __sp = os.path.splitext(ii)
                __exc = __sp[1] # 확장자

                __n = np.fromfile(ii, np.uint8)
                __img = cv2.imdecode(__n, cv2.IMREAD_COLOR)
                __barcode = decode(__img)      
                __rename_file_nm=dirname+'\\'+'{0}_{1}{2}'.format(__barcode,uniq,__exc)
                os.rename( ii , __rename_file_nm )
                uniq +=1

    except Exception as e :
        print('into_rename_barcode : ',e)

def init_fold( _dbconn ):
    '''폴더 정리.'''
    try:
        str = 'c:\\ncnc'        
        dd = _dbconn
        rootlist = os.listdir(str)
        rootdirs = [X for X in rootlist if os.path.isdir(str+'\\'+X)]
        for i in rootdirs:        
            dirname = str+'\\'+i
            base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d_%H%M_')        
            listdir = os.listdir(dirname)

            path_files =  [ os.path.join(dirname, x)  for x in listdir ]        
            file_names =  [ X for X in path_files if os.path.isfile(X)]
            file_nm    =  [ x for x in listdir ]
                
            cnt = 1 # 폴더 카운트        
            while( len(file_names) > 0):
                default_fold_nm = base_dttm+(repr(cnt).zfill(2))
                prod_fold       = base_dttm+(repr(cnt).zfill(2))
                v_range = 0
                # 5개씩 볼더 복사 
                if len(file_names) >= 5:
                    default_fold_nm = dirname+'\\'+default_fold_nm+'_5' 
                    prod_fold       = prod_fold+'_5' 
                    v_range = 5       
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

def getfolelist(str):    
    base = 'c:\\ncnc'
    path_str = base+'\\'+str
    __list = os.listdir( path_str )
    temp_list = [ X for X in __list if os.path.isdir(path_str+'\\'+X)]
    list = [ path_str+'\\'+X for X in temp_list if X[-4:-1] != '(완료']
    return list            

def getFileList( _path ):    
    __list = os.listdir( _path )    
    list = [ _path+'\\'+X for X in __list ]
    return list

def send_telegram_message( message , div='' ):
    '''텔러그램 판매 발송
    '''
    token = '6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc' 
    '''
    -1001813504824 : 니콘방 우정이 개인방 SEND_TYPE V , VE 일경우 이쪽으로 보낸다.
    -1002336115183 : 매크로 봇방
    '''
    try: 
        base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
        data = {'chat_id' : '-1001813504824' , 'text' : base_dttm+'\n'+message}
        response = requests.post(url, data=data)
        time.sleep(0.5)
        #print( 'send_telegram_message : ' , response.json() )               
    except Exception as e:
        print( 'telegram_send', e )
    finally:
        pass

def sendTelegramMsg( message ):
    '''텔러그램 매크로 봇방
    '''
    token = '6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc' 
    '''
    -1001813504824 : 니콘방 우정이 개인방 SEND_TYPE V , VE 일경우 이쪽으로 보낸다.
    -1002336115183 : 매크로 봇방
    '''
    try: 
        base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
        data = {'chat_id' : '-1002336115183' , 'text' : base_dttm+'\n'+message}
        response = requests.post(url, data=data)
        time.sleep(0.1)
        #print( 'sendTelegramMsg : ' , response.json() )               
    except Exception as e:
        print( 'sendTelegramMsg', e )
    finally:
        pass        

def complete_fold(path , state = True):
    '''해당 path 의 이름 변경'''
    base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S')
    __path = path
    if state:
        __path += '_'+base_dttm+'(완료)'
    else :
        __path += '_이상이상이상(완료)'

    os.rename( path , __path)
    return __path


def getFileCnt( _dbconn ):
    '''잔여파일 개수 확인.'''
    rt = []
    path1 = 'c:\\ncnc'    
    __list = os.listdir( path1 )
    _dbconn.update_nicon_job_list_qty() # 초기화
    
    # 1차 하위 폴더 리스트
    subFolds = [ X for X in __list if os.path.isdir(path1+'\\'+X)] 
    for fold in subFolds:
        cnt = 0
        # 2차 폴더 패스
        path2 = os.path.join(path1 , fold)
        __list2 = os.listdir( path2 )
        subFolds2 = [ X for X in __list2 if X[-4:-1] != '(완료']   
        for ff in subFolds2:
            path3 = os.path.join(path2, ff)
            __list3 = os.listdir( path3 )
            cnt += len(__list3)        

        if cnt >0:
            rt.append( [fold , cnt] )
            param = {'qty': cnt , 'path':fold }
            _dbconn.update_nicon_job_list( param )
    
    txt = ''
    for i in rt:
        txt += f'{i[0]} \n=== 잔여 갯수[ {i[1]}개 ] ===\n--------------------\n\n'
    
    send_telegram_message( txt )



def setJobLog( job_nm , flag):
    '''작업 로그 생성 URL 호출'''
    try:
        url = "https://themoreschool.cafe24.com/job_log.php"
        payload = {"job_nm": job_nm, "flag": flag}
        response = requests.post(url, data=payload)  # ← json= → data= 로 변경
    except Exception as e:
        print('='*20)
        print( 'setJobLog error', e )
        print('='*20)
