import subprocess
import time
from pytz import timezone
from datetime import datetime

import requests
import json


import lib.dbcon as dbcon

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
    _dbconn = dbcon.DbConn() #db연결    
    python_script = "c://Users//DLIVE//eclipse-workspace//nicon//autonicon2.py"

    # Python 인터프리터의 경로
    python_executable = "python"
    # subprocess를 사용하여 Python 스크립트 실행
    subprocess.run([python_executable, python_script] , capture_output=True)

    _tmp = _dbconn.get_nicon_client_log()
    

    
    while(True):
        _seq       = _tmp[0]['seq']
        _reg_date  = _tmp[0]['reg_date']
        _send_yn   = _tmp[0]['send_yn']   #메세지 발소 여부
        _diff_time = _tmp[0]['diff_time'] #로그 생성 시간
        _send_time = _tmp[0]['send_time'] #메세지 재발송 여부

        if( _diff_time == 'Y' ):
            print(datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S') , 'Nicon client ReStart')
            send_telegram_message('Nicon client ReStart')
            subprocess.run([python_executable, python_script] , capture_output=True)
        
        time.sleep(60)
    

    



if __name__ == "__main__":
    main()