import requests
import json
import lib.dbcon as dbcon 
import schedule
import time
from datetime import datetime
import random
from pytz import timezone
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
    -1001813504824 : 우정이 개인방 SEND_TYPE V , VE 일경우 이쪽으로 보낸다.

    -1001932446119  : 니콘내콘 알림
    -1001839221120  : 더모아방
    -1001906908142  : themore
    -1002078550724  : 주땡 - e내콘
    -1002107720688  : 유치원 - e내콘    
    
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
                _seq = 0
                for ll in lists:    
                    _seq += 1   
                    for detail in __details: # 상품명 리스트                           
                        if ( detail[2] == ll['name'].strip() ):                                  
                            id      = ll['id']
                            name    = ll['name'].strip()
                            amount  = ll['askingPrice']
                            refuse  = ll['isRefuse']
                            block   = ll['isBlock']
                            param = {'category_id':category_id ,'category_nm' : category_nm ,'id': id , 'name':name , 'amount': amount , 'refuse' : refuse , 'block': block , 'seq':_seq }
                            
                            
                            res = dd.get_prod_chg(param)
                            sent_text = ''
                            sent_text += category_nm+' / '+name+'\n'
                            sent_text += "가격 : {}".format(amount)+'\n'
                            sent_text += '매입 : '+( '매입중' if refuse == 0 else '매입보류')
                            #print(sent_text)
                            if len(res) == 0: # 신규일경우
                                dd.insert_nicon(param)
                                print('신규 : ',param)
                                send_telegram_message(sent_text , detail[3] )
    
                            else : #기존 상품일경우
                                result = dd.get_nicon( param )   

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
    


def fnRewindSec():
    global _rewind_sec , _db_conn
    _rewind_sec = _db_conn.getNiconStateRewindSec()
    print(_rewind_sec)
    schedule.clear()
    schedule.every( _rewind_sec ).seconds.do( getNicon )  
    schedule.every(30).minutes.do( fnRewindSec )


if __name__ == "__main__":    
    getNicon() # 데이터 수집


    




    
        
        