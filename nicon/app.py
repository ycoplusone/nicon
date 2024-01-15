import requests
#from bs4 import BeautifulSoup
import json
import lib.dbcon as dbcon 
import schedule
import time
from datetime import datetime
#import requests
import json
import random
from pytz import timezone
from operator import itemgetter    

import math    

'''
"id":1114,"name":"싱글레귤러 아이스크림","askingPrice":2950,"isRefuse":1,"isBlock":0
askingPrice :매입가격 
isRefuse : 0 매입중 , 1 매입대기
isBlock : 0 매입가능 , 1 매입불가

bot 접속 현황 
https://api.telegram.org/bot6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc/getUpdates
METHOD_NAME

메세지 테스트
https://api.telegram.org/bot6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc/sendMessage?chat_id=-1001813504824&text=forgetme1

'''
def send_telegram_message( message ,send_type ):
    token = '6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc' 
    chats = ['-1001932446119','-1001839221120','-1001906908142']    
    '''
    -1001932446119 : 니콘내콘 알림
    -1001839221120 : 더모아방
    -1001906908142 : themore
    
    -1001813504824 : 우정이 개인방 SEND_TYPE V , VE 일경우 이쪽으로 보낸다.
    '''
    base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        
    try: 
        if 'V' in send_type: #우정이 전용방
            url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
            data = {'chat_id': '-1001813504824', 'text': base_dttm+'\n'+message}
            response = requests.post(url, data=data)
            time.sleep(1)
            print( 'with V : ' , response.json() )
        
        if 'E' in send_type:       
            for chat in chats:
                url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
                data = {'chat_id': chat , 'text': base_dttm+'\n'+message}
                response = requests.post(url, data=data)
                time.sleep(1)
                print( 'without V : ',response.json() )
    except Exception as e:
        print( 'telegram_send', e )
    finally:
        pass
    
        
    

def getNicon():
    try:
        s_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')        
        dd = dbcon.DbConn()    
        __lists = dd.get_job_list()
                           
        for ii in __lists:
            category_id = ii[0] #카테고리 id
            category_nm = ii[2] #카테리고리명
            __details = dd.get_nicon_job_detail( {'category_id':category_id } )         # 검증 세부 레스트
            url = 'https://api2.ncnc.app/con-items?forSeller=1&conCategory2Id='+category_id
           
            response = requests.get(url)
            
            if response.status_code == 200:
                txt = response.json()
                lists = txt['conItems']
                
                
                for ll in lists:    
                    for detail in __details: # 상품명 리스트      
                        if ( detail[2] == ll['name'].strip() ):                                  
                            id      = ll['id']
                            name    = ll['name'].strip()
                            amount  = ll['askingPrice']
                            refuse  = ll['isRefuse']
                            block   = ll['isBlock']
                            param = {'category_id':category_id ,'category_nm' : category_nm ,'id': id , 'name':name , 'amount': amount , 'refuse' : refuse , 'block': block }
                            
                            res = dd.get_prod_chg(param)
                            sent_text = ''
                            sent_text += category_nm+' / '+name+'\n'
                            sent_text += "가격 : {}".format(amount)+'\n'
                            sent_text += '매입 : '+( '매입중' if refuse == 0 else '매입보류')
                            #print(sent_text)
                            if len(res) == 0: # 신규일경우
                                dd.insert_nicon(param)
                                print('신규 : ',param)
                                #asyncio.run( telegram_send(sent_text , detail[3] ) )
                                send_telegram_message(sent_text , detail[3] )
    
                            else : #기존 상품일경우
                                result = dd.get_nicon( param )   
                                #print( param ) 
                                #print( '','값',result[0][0]  )
                                #print( '','조건',result[0][0] == 'F' )
                                if result[0][0] == 'F':
                                    dd.update_nicon(param)
                                    print('변경 : ',param)                                    
                                    #asyncio.run( telegram_send(sent_text, detail[3] ) )
                                    send_telegram_message(sent_text , detail[3] )
                            
                                    
            else : 
                print(response.status_code)
            
        e_time = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        print('start / end time : {} ~ {}'.format(s_time , e_time) )    
        dd.update_nicon_state();
    
    except Exception as e:
        print( 'function getNicon() exception => ', e )
    finally:
        pass
    
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
    for i in range(1,15):
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


def fn_test(str):
    print('fn_test' , str  )

def fn_test1():    
    global _rewind_sec , scheduler1
    _rewind_sec = random.randint(1,10)
    print('fn_test1',_rewind_sec)
    schedule.clear()
    schedule.every( _rewind_sec ).seconds.do( lambda: fn_test('scheduler zzz')  )
    schedule.every(30).seconds.do( fn_test1 )      


def fnRewindSec():
    global _rewind_sec , _db_conn
    _rewind_sec = _db_conn.getNiconStateRewindSec()
    print(_rewind_sec)
    schedule.clear()
    schedule.every( _rewind_sec ).seconds.do( getNicon )  
    schedule.every().day.at('00:10').do(fn_history)
    schedule.every(30).minutes.do( fnRewindSec )


if __name__ == "__main__":    
    #_rewind_sec = 5
    #schedule.every( _rewind_sec ).seconds.do( lambda: fn_test('scheduler1') )
    #schedule.every(15).seconds.do( fn_test1 )

    _db_conn = dbcon.DbConn()
    
    getNicon()

    _rewind_sec = _db_conn.getNiconStateRewindSec()    
    
    # 상품정보 수집
    schedule.every( _rewind_sec ).seconds.do( getNicon )    
    
    # 판매정보 수집
    #schedule.every().days.do( fn_history )
    schedule.every().day.at('00:10').do(fn_history)
    # 반복 초 변경
    schedule.every(30).minutes.do( fnRewindSec )    

    
    while True:
        schedule.run_pending()
        time.sleep(1)
    




    
        
        