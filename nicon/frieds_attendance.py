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
from dotenv import load_dotenv
from openai import OpenAI #챗gpt api
import lib.util as w2ji

__g_wait = 5


def fnOpenAiAsk( text ):
    '''인공지능'''
    try:
        load_dotenv()        
        client = OpenAI( api_key = os.environ.get('open_api_key') )
        ages    = [20,30,40,50,60]
        age     = random.sample(ages,1)
        sexs    = ['남자','여자']
        sex     = random.sample(sexs,1)
        query = f"'{text}'에 대한 {age[0]}대 {sex[0]}같은 짧은 댓글."  
        print('\t task : ', query)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo" ,
            messages=[
            {   "role": "system"
                , "content": "You are a helpful assistant. You must answer in only Korean."
            }
            , {   
                "role": "user"
                , "content": query
            }            
            ]
        )
        return response.choices[0].message.content 
    except Exception as e:
        print('error : ',e)


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

def fnGetTag(driver , xpath_str):
    '''태그 읽어오기'''
    time.sleep(0.5)
    rt_str = ''
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_str )))
        rt_str = element.text
        return rt_str
    except Exception as e:
        print('error : fnGetTag')
        return ''
        



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
        

def fnReply(driver, list , seq):
    '''댓글쓰기'''    
    try:
        rt = True
        rep_txt = '' #댓글내용
        pages = [1,2,3,4,5,6,7,8,9,10]
        page = random.sample(pages,1)   # 글선택번호        
        url = f'https://friends001.com/bbs/board.php?bo_table=free&page={page[0]}'
        
        driver.get( url )     
        driver.implicitly_wait(15)
        time.sleep( __g_wait )
        tag = f"/html/body/div[1]/div[1]/div/div/div[3]/section/div/form/div[1]/ul/li[{seq}]/div[2]/a"

        _bool = fnClick( driver , tag )
        time.sleep( __g_wait )
        if _bool == False:
            rt = False        
        
        # 글읽기
        ask_txt = fnGetTag(driver,'//*[@id="thema_wrapper"]/div[1]/div/div/div[3]/div[3]/section/article/div[2]/div[2]')
        if ask_txt == '':
            rt = False
        else :    
            rep_txt = fnOpenAiAsk(ask_txt)
        print('\t 답변 : ',rep_txt)

        
        txt = f"$('#wr_content').val('{rep_txt}');"                
        _bool = fnScript(driver, txt )
        if _bool == False:
            rt = False                   

        _bool = fnScript(driver , "apms_comment_submit();")#댓글쓰기 버튼
        time.sleep( __g_wait )
        if _bool == False:
            rt = False        
        
        if _bool:
            time.sleep(1)
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



def fnMain():
    datas = readfile("C:\\ncnc_class\\프렌즈 정보.xlsx") # 0:id , 1:ps , 2:출석  , 3,4,5 : 댓글 , 6:제목, 7:내용
    for i in datas:
        driver = fnDriver()          # 드라이버생성

        #로그인 한다. - begin
        for j in range(0,20):
            aa = fnLogin(driver , i )
            if aa :         # 로그인
                print(i[0],' : 로그인 완료.')
                break
        #로그인 한다. - end
        
        
        # 출석체크 - begin
        for j in range(0,20):
            aa = fnAttendance(driver , i )    # 출석체크
            if aa :
                print(i[0],' : 출석체크 완료.')
                break
        # 출석체크 - end
        

        # 댓글달기 - begin
        r_list = [1,2,3,4,5,6]
        line = random.sample(r_list,3)   # 글선택번호        
        cnt = 0
        for j in range(0,20):
            ''''''            
            aa = fnReply(driver , i ,  line[cnt] )     # 댓글 3개 달기
            if aa :
                print(i[0],' : ', cnt,'번째 댓글쓰기 완료')
                cnt += 1
            if cnt == 3:
                print(i[0], ' 댓글쓰기 완료.')
                break
        # 댓글달기 - end
        
        
        # 글쓰기 - begin
        for j in range(0,10):
            aa = fnWrite(driver , i )           # 글쓰기        
            if aa:
                print(i[0],' : ', '글쓰기 완료.')
                break        
        # 글쓰기 - end
        driver.quit()                   # 드라이버 종료    
    
    w2ji.send_telegram_message( '프렌즈 작업이 완료 되었습니다. 확인은 필요힙니다. 캡쳐를 확인하세요.' )
    

def  fntest():
    '''테스트 함수'''    
    datas = readfile("C:\\ncnc_class\\프렌즈 정보.xlsx") # 0:id , 1:ps , 2:출석  , 3,4,5 : 댓글 , 6:제목, 7:내용
    driver = fnDriver()                 # 드라이버생성
    #fnLogin(driver , datas[0] )         # 로그인
    #fnAttendance(driver , datas[0] )    # 출석체크
    fnReply(driver , datas[0] , 2 )     # 댓글 3개 달기

if __name__ == "__main__":  
    '''프렌즈 출석'''    
    #fntest() # 테스트 프로세스

    fnMain() #메인프로세스 전체 수행부분

    
    