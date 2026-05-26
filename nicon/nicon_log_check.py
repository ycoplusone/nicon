import os
import time
from datetime import datetime, timedelta
import urllib.request
import urllib.parse
import json
import lib.util as w2ji

# 파일을 미래 시간으로 변경하는 powershell 스크립트 비상 상황에 쓰도록 한다.
# $(Get-Item "c:\ncnc\nicon.log").LastWriteTime = "2026-12-31 15:00:00"

# ================= 설 정 구 간 =================
LOG_FILE_PATH = r"c:\ncnc\nicon.log"
# ===============================================


def check_log_file():
    # 1. 파일 존재 여부 확인
    if not os.path.exists(LOG_FILE_PATH):
        msg = f"🚨 *[경고]* 로그 파일(`{LOG_FILE_PATH}`)을 찾을 수 없습니다."
        # 필요 시 아래 주석을 해제하면 파일이 없을 때도 알림을 보냅니다.
        return

    # 2. 파일의 마지막 수정 시간 확인
    last_modified_timestamp = os.path.getmtime(LOG_FILE_PATH)
    last_modified_time = datetime.fromtimestamp(last_modified_timestamp)
    
    # 3. 현재 시간과의 차이 계산
    current_time = datetime.now()
    time_difference = current_time - last_modified_time
    
    print(f"현재 시간: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"최종 기록: {last_modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"경과 시간: {int(time_difference.total_seconds() / 60)}분")

    # 4. 1시간(3600초) 이상 기록이 없는 경우 알림 발송
    if time_difference > timedelta(hours=1):
        formatted_time = last_modified_time.strftime("%Y-%m-%d %H:%M:%S")
        message = (
            f"🚨 *[로그 중단 경고]*\n"
            f"`{LOG_FILE_PATH}` 파일에 최근 1시간 동안 새로운 기록이 없습니다.\n"
            f"(마지막 기록 시간: {formatted_time})"
        )
        #send_telegram_message(message)        
        w2ji.send_telegram_message(  f'니콘 이상' )      

if __name__ == "__main__":
    while(True):         
        check_log_file()
        time.sleep(60)