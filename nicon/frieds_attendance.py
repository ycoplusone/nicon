from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from datetime import datetime
from pytz import timezone
import time
import os
import pandas as pd
import random

__g_wait = 5

def fnClick(driver , str):    
    time.sleep(0.5)
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, str ))).click()
        return True
    except Exception as e:
        print('error : fnClick')
        return False



def fnScript(driver , txt):
    '''콘솔 스크립트로 '''
    time.sleep(0.5)
    try:
        driver.execute_script(txt)
        return True
    except Exception as e:
        print('error : fnScript')
        return False



def readfile( path ):
    '''파일 읽기'''
    _rt = []
    df = pd.read_excel(path ,   engine='openpyxl' , dtype=object )
    arr =  df.to_numpy()
    for i in arr :
        aa = []
        for j in i:
            aa.append( str(j) )
        _rt.append( aa )    
    return _rt   

def fnDriver():
    '''
    크룸 초기화
    https://googlechromelabs.github.io/chrome-for-testing/#stable
    '''
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument('window-size=900x768')   
    options.add_argument('--incognito')
    _rt = webdriver.Chrome('chromedriver.exe' , options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
    #_rt.get('https://friends001.com/?fbclid=PAZXh0bgNhZW0BMAABpjtt8PFV4Z-qo0fbbTCQfcSblUECKe0sghHasBnz18cjQcwh9v_MQJoq5Q_aem_LjkNBXjTNTleWqoHEcb8yg')
    _rt.get('https://friends001.com/bbs/login.php?url=%2F')    
    _rt.implicitly_wait(15)  
    time.sleep(1)  
    return _rt

def fnCapture(driver , str):
    try:
        base_dttm   = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d_%H%M%S')
        os.mkdir('c:\\ncnc_class\\friends')
    except Exception as e:
        ''''''
        

    file_name   = r"c:\\ncnc_class\\friends\\{}_{}{}".format( base_dttm , str ,'.png') 
    try:
        driver.save_screenshot(file_name)
        #print("### capture complete \t", file_name)
    except Exception as e:
        print('### error msg :: ', e)    


def fnLogin(driver , list ):
    '''로그인'''    
    try:
        rt = True        
        print('')
        id_txt = f"$('#login_id').val('{list[0]}');"
        ps_txt = f"$('#login_pw').val('{list[1]}');"    
        
        _bool = fnScript(driver, id_txt )
        if _bool == False:
            rt = False        

        _bool = fnScript(driver, ps_txt )
        if _bool == False:
            rt = False                
        
        _bool = fnClick( driver , '/html/body/div[1]/div[1]/div/div/div/div/div[1]/div[2]/form/div[3]/div[2]/button')
        time.sleep(1)    
        if _bool == False:
            rt = False    

        driver.implicitly_wait(15)
        time.sleep(0.5)        
        return rt
    except Exception as e:
        return False
    

def fnAttendance(driver , list):
    '''출석 체크 페이지'''    
    try :        
        rt = True
        url = 'https://friends001.com/plugin/attendance/attendance.php'
        driver.get( url )
        driver.implicitly_wait(15)
        time.sleep( __g_wait )
        txt = f"$('#subject').val('{list[2]}');"
        
        _bool = fnScript(driver, txt )
        if _bool == False:
            rt = False           
        
        _bool = fnClick( driver , '/html/body/div[1]/div[1]/div/div/div[3]/div[3]/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td/form/div/li[3]/input')
        time.sleep( __g_wait )
        if _bool == False:
            rt = False        
        
        Alert(driver).accept()
        if _bool:
            fnCapture( driver , list[0]+'_출석' ) #캡쳐
        time.sleep(0.5)
        return rt
    except Exception as e:
        ''''''
        return False
        

def fnReply(driver, list , rep_txt , seq):
    '''댓글쓰기'''    
    try:
        rt = True
        url = 'https://friends001.com/bbs/board.php?bo_table=free'
        driver.get( url )     
        driver.implicitly_wait(15)
        time.sleep( __g_wait )
        tag = f"/html/body/div[1]/div[1]/div/div/div[3]/section/div/form/div[1]/ul/li[{seq}]/div[2]/a"

        _bool = fnClick( driver , tag )
        time.sleep( __g_wait )
        if _bool == False:
            rt = False        
        
        txt = f"$('#wr_content').val('{rep_txt}');"                
        _bool = fnScript(driver, txt )
        if _bool == False:
            rt = False                   

        #_bool = fnClick( driver , "/html/body/div[1]/div[1]/div/div/div[3]/div[3]/div[2]/aside/form/div/div[2]/div[2]" ) #댓글쓰기 버튼
        _bool = fnScript(driver , "apms_comment_submit();")#댓글쓰기 버튼
        time.sleep( __g_wait )
        if _bool == False:
            rt = False        
        
        if _bool:
            fnCapture( driver , list[0]+'_댓글' ) #캡쳐
        time.sleep(0.5)
        return rt
    except Exception as e:
        return False

    
def fnWrite( driver, list ):
    '''글쓰기'''
    try :
        rt = True
        url = 'https://friends001.com/bbs/board.php?bo_table=free'
        driver.get( url )
        driver.implicitly_wait(15)
        time.sleep( __g_wait )   

        _bool = fnClick(driver , '//*[@id="fboardlist"]/div[2]/div[1]/div/a[2]/img') #글쓰기 가기버튼
        time.sleep( __g_wait )
        if _bool == False:
            rt = False 
        
        subject_txt = f"$('#wr_subject').val('{list[6]}');"  #제목쓰기
        _bool = fnScript( driver , subject_txt )
        if _bool == False:
            rt = False 

        content_txt = f"$('#wr_content').val('{list[7]}');"  #내용쓰기
        _bool = fnScript( driver , content_txt )
        time.sleep(0.5)
        if _bool == False:
            rt = False         

        _bool = fnClick(driver , '/html/body/div[1]/div[1]/div/div/div[3]/div[4]/form/div[8]/button/b') #글쓰기 버튼
        time.sleep( __g_wait )
        if _bool == False:
            rt = False         

        if _bool:
            fnCapture( driver , list[0]+'_글쓰기' ) #캡쳐
        time.sleep(0.5)
        return rt
    except Exception as e:
        return False

    

if __name__ == "__main__":  
    '''프렌즈 출석'''    
    datas = readfile("C:\\ncnc_class\\프렌즈 정보.xlsx") # 0:id , 1:ps , 2:출석  , 3,4,5 : 댓글 , 6:제목, 7:내용
    #driver = fnDriver()                 # 드라이버생성
    #fnLogin(driver , datas[0] )         # 로그인
    #fnAttendance(driver , datas[0] )    # 출석체크
    #fnReply(driver , datas[0] , datas)  # 댓글 3개 달기
    #fnWrite(driver , datas[0])          # 글쓰기

        
    
    for i in datas:
        driver = fnDriver()          # 드라이버생성

        # 반복 로그인 한다.
        for j in range(0,20):
            aa = fnLogin(driver , i )
            if aa :         # 로그인
                print(i[0],' : 로그인 완료.')
                break
        
        for j in range(0,20):
            aa = fnAttendance(driver , i )    # 출석체크
            if aa :
                print(i[0],' : 출석체크 완료.')
                break
        
        r_list = [1,2,3,4,5,6]
        line = random.sample(r_list,3)   # 글선택번호        
        cnt = 0
        for j in range(0,20):
            ''''''            
            # 첫댓글
            r1 = random.randrange(0, len(datas) )
            r2 = random.randrange(3,6)
            reply_txt = datas[r1][r2]       #댓글내용       
            aa = fnReply(driver , i , reply_txt , line[cnt] )     # 댓글 3개 달기
            if aa :
                print(i[0],' : ', cnt,'번째 댓글쓰기 완료')
                cnt += 1
            if cnt == 3:
                print(i[0], ' 댓글쓰기 완료.')
                break
        
        for j in range(0,10):
            aa = fnWrite(driver , i )           # 글쓰기        
            if aa:
                print(i[0],' : ', '글쓰기 완료.')
                break

        driver.quit()                   # 드라이버 종료
    