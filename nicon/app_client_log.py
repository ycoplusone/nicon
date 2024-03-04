import requests
import json

import time
from pytz import timezone
from datetime import datetime

import lib.dbcon as dbcon 
import lib.util as w2ji


def send_telegram_message( message ):
    '''
    -1001813504824 : 우정이 개인방 SEND_TYPE V , VE 일경우 이쪽으로 보낸다.
    '''    
    token = '6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc' 

    base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')        
    try: 
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
        data = {'chat_id': '-1001813504824' , 'text': base_dttm+'\n'+message , 'parse_mode':'HTML' ,'disable_web_page_preview': True }
        response = requests.post(url, data=data)
        time.sleep(1)
    except Exception as e:
        print( 'telegram_send', e )
    finally:
        pass
    

    

def main():
    '''client 활성화 체크'''
    dd = dbcon.DbConn()
    _sql = dd.get_nicon_client_log()
    
    _seq       = _sql[0]['seq']
    _reg_date  = _sql[0]['reg_date']
    _send_yn   = _sql[0]['send_yn']   #메세지 발소 여부
    _diff_time = _sql[0]['diff_time'] #로그 생성 시간
    _send_time = _sql[0]['send_time'] #메세지 재발송 여부

    if   (_diff_time == 'Y') & (_send_yn=='N') :
        print('발송')
        send_telegram_message('nicon client 5minutes off during')
        dd.update_nicon_client_log({'seq':_seq})
    elif (_diff_time == 'Y') & (_send_yn=='Y') & (_send_time=='Y') :
        print('재발송')
        send_telegram_message('nicon client 1hour off during')
        dd.update_nicon_client_log({'seq':_seq})
    else:
        print('문제 없음')
    


if __name__ == "__main__":    
    main()