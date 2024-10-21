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
import pyperclip #복사
from dotenv import load_dotenv
from openai import OpenAI #챗gpt api
import lib.util as w2ji
import re
import pymysql



class friends(object):
    __g_wait = 5
    __conn = ''
    load_dotenv() #환경변수 로딩
    def fnDbcon(self):
        '''db연결'''
        self.__conn = pymysql.connect(  host        = os.environ.get('mysql_url') 
                                        , user      = os.environ.get('mysql_id')
                                        , password  = os.environ.get('mysql_ps')
                                        , db        = os.environ.get('mysql_db') 
                                        , charset   = os.environ.get('mysql_charset')  )    
        #print('__conn' , self.__conn)
        self.fnDbBoardInit() # 360일 이상된 자료 사용할수 있도록 상태 변경
    
    def fnDbreply(self , param):
        '''db에 댓글 기록하기'''
        try :
            cur = self.__conn.cursor()
            query = (
                    "INSERT INTO friends_reply_list (query, result, c_date) "
                    " VALUES('{query}', '{result}', now())"
            )            
            query = query.format( **param )     
            print(query)
            cur.execute( query )
            self.__conn.commit()
        except Exception as e:
            print( 'fnDbreply', e  )
        finally:
            pass         
    
    def fnDbBoardInit(self):
        '''게시판 db에 사용이력이 360일 이상된 자료 사용가능으로 변경하기.'''
        try :
            cur = self.__conn.cursor()                        
            query = (
            " update friends_board_list "
            " set use_yn = 'N'  "
            " where DATE_FORMAT(use_dt ,'%Y%m%d') <= DATE_FORMAT(ADDDATE(now() , -360),'%Y%m%d') " 
            " and use_yn = 'Y'        "
            )            
            query = query.format( )                      
            cur.execute( query )
            self.__conn.commit()    
        except Exception as e:
            print( 'fnDbBoardInit', e )
        finally:
            pass         


    def fnDbBoard(self ):
        '''게시판 db에 랜덤의 글 하나 가져오기'''
        try :
            _lists = []
            query = (
                " select site_domin , type_nm , seq , subject , content  "
                " from friends_board_list  "
                " where use_yn = 'N' "
                " order by rand() limit 1 "
            )
            query = query.format( )
            cur = self.__conn.cursor(  pymysql.cursors.DictCursor)            
            cur.execute( query )            
            return cur.fetchall()         
        except Exception as e:
            print( 'fnDbBoard => ' , e )        
    
    def fnDbBoardUse(self , param):
        '''게시판 db에 사용한 글 사용처리하기'''
        try :
            cur = self.__conn.cursor()
                        
            query = (
            " update friends_board_list  "
            " set use_yn='Y', use_dt = now() "
            " WHERE site_domin='{site_domin}' AND type_nm='{type_nm}' AND seq={seq} "
            )            
            query = query.format( **param )                      
            cur.execute( query )
            self.__conn.commit()          
            
        except Exception as e:
            print( 'fnDbBoardUse => ', e )
        finally:
            pass         

    def fnOpenAiAsk( self , text ):
        '''인공지능'''
        try:
                    
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
            rt_txt = response.choices[0].message.content 
            rt_txt = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", rt_txt)
            return rt_txt
        except Exception as e:
            print('error : ',e)


    def fnClick( self,  driver , str):    
        time.sleep(0.5)
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, str ))).click()
            return True
        except Exception as e:
            print('error : fnClick')
            return False

    def fnCopyNpaste( self, driver , _str ):
        time.sleep(0.2)
        pyperclip.copy( _str )
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    def fnScript( self, driver , txt):
        '''콘솔 스크립트로 '''
        time.sleep(0.5)
        try:
            driver.execute_script(txt)
            return True
        except Exception as e:
            print('error : fnScript')
            return False



    def readfile(self , path ):
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

    def fnDriver(self):
        '''
        크룸 초기화
        https://googlechromelabs.github.io/chrome-for-testing/#stable
        '''
        options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        #options.add_argument('--window-size=900x1080')   
        options.add_argument('--incognito')
        _rt = webdriver.Chrome('chromedriver.exe' , options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
        #_rt.get('https://friends001.com/?fbclid=PAZXh0bgNhZW0BMAABpjtt8PFV4Z-qo0fbbTCQfcSblUECKe0sghHasBnz18cjQcwh9v_MQJoq5Q_aem_LjkNBXjTNTleWqoHEcb8yg')
        _rt.get('https://friends001.com/bbs/login.php?url=%2F')    
        _rt.implicitly_wait(15)  
        
        time.sleep(1)  
        return _rt

    def fnCapture(self , driver , str):
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

    def fnGetTag(self,driver , xpath_str):
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
            



    def fnLogin( self , driver , list ):
        '''로그인'''    
        try:
            rt = True        
            print('')
            id_txt = f"$('#login_id').val('{list[0]}');"
            ps_txt = f"$('#login_pw').val('{list[1]}');"    
            
            _bool = self.fnScript(driver, id_txt )
            if _bool == False:
                rt = False        

            _bool = self.fnScript(driver, ps_txt )
            if _bool == False:
                rt = False                
            
            _bool = self.fnClick( driver , '/html/body/div[1]/div[1]/div/div/div/div/div[1]/div[2]/form/div[3]/div[2]/button')
            time.sleep(1)    
            if _bool == False:
                rt = False    

            driver.implicitly_wait(15)
            time.sleep(0.5)        
            return rt
        except Exception as e:
            return False
        

    def fnAttendance(self , driver , list):
        '''출석 체크 페이지'''    
        try :        
            rt = True
            url = 'https://friends001.com/plugin/attendance/attendance.php'
            driver.get( url )
            driver.implicitly_wait(15)
            time.sleep( self.__g_wait )
            txt = f"$('#subject').val('{list[2]}');"
            
            _bool = self.fnScript(driver, txt )
            if _bool == False:
                rt = False           
            
            _bool = self.fnClick( driver , '/html/body/div[1]/div[1]/div/div/div[3]/div[3]/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td/form/div/li[3]/input')
            time.sleep( self.__g_wait )
            if _bool == False:
                rt = False        
            
            Alert(driver).accept()
            if _bool:
                self.fnCapture( driver , list[0]+'_출석' ) #캡쳐
            time.sleep(0.5)
            return rt
        except Exception as e:
            ''''''
            return False
            

    def fnReply(self , driver, list , seq):
        '''댓글쓰기'''    
        try:
            rt = True
            rep_txt = '' #댓글내용
            pages = [1,2,3,4,5,6,7,8,9,10]
            page = random.sample(pages,1)   # 글선택번호        
            url = f'https://friends001.com/bbs/board.php?bo_table=free&page={page[0]}'
            
            driver.get( url )     
            driver.implicitly_wait(15)
            time.sleep( self.__g_wait )
            tag = f"/html/body/div[1]/div[1]/div/div/div[3]/section/div/form/div[1]/ul/li[{seq}]/div[2]/a"

            _bool = self.fnClick( driver , tag )
            time.sleep( self.__g_wait )
            if _bool == False:
                rt = False        
            
            # 글읽기
            ask_txt = self.fnGetTag(driver,'//*[@id="thema_wrapper"]/div[1]/div/div/div[3]/div[3]/section/article/div[2]/div[2]')
            if ask_txt == '':
                rt = False
            else :    
                rep_txt = self.fnOpenAiAsk(ask_txt)
            print('\t 답변 : ',rep_txt)

            actions = driver.find_element(By.CSS_SELECTOR, 'body')
            actions.send_keys(Keys.DOWN)    
            actions.send_keys(Keys.DOWN)    
            actions.send_keys(Keys.DOWN)    
            actions.send_keys(Keys.DOWN)    
            actions.send_keys(Keys.DOWN)    
            actions.send_keys(Keys.DOWN)    
            time.sleep(0.1)
            _bool = self.fnClick( driver , '/html/body/div[1]/div[1]/div/div/div[3]/div[3]/div[2]/aside/form/div/div[2]/div[1]/textarea' )      
            time.sleep(0.1)
            self.fnCopyNpaste(driver , rep_txt)
            time.sleep(0.5)
            if _bool == False:
                rt = False                      

            _bool = self.fnScript(driver , "apms_comment_submit();")#댓글쓰기 버튼
            time.sleep( self.__g_wait )
            if _bool == False:
                rt = False        
            
            if _bool:
                time.sleep(1)
                self.fnCapture( driver , list[0]+'_댓글' ) #캡쳐      
                aa = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", ask_txt)  # 특수문자 제외
                aa = aa[0:1024]
                bb = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", rep_txt)  # 특수문자 제외        
                bb = bb[0:1024]
                self.fnDbreply({'query': aa ,'result':bb}) # 인공지능 댓글 기록하기.
            time.sleep(0.5)
            
            return rt
        except Exception as e:
            return False

        
    def fnWrite( self , driver, list ):
        '''글쓰기'''
        try :
            #subject = list[6]
            #content = list[7]
            str = self.fnDbBoard()
            site_domin  = str[0]['site_domin']
            type_nm     = str[0]['type_nm']
            seq         = str[0]['seq']
            subject     = str[0]['subject']
            content     = str[0]['content']            
            print('subject : ', subject)
            print('content : ', content)
            rt = True
            url = 'https://friends001.com/bbs/board.php?bo_table=free'
            driver.get( url )
            driver.implicitly_wait(15)
            time.sleep( self.__g_wait )   

            _bool = self.fnClick(driver , '//*[@id="fboardlist"]/div[2]/div[1]/div/a[2]/img') #글쓰기 가기버튼
            time.sleep( self.__g_wait )
            if _bool == False:
                rt = False 
            
            _bool = self.fnClick( driver , '/html/body/div[1]/div[1]/div/div/div[3]/div[4]/form/div[3]/div/div/input' )        
            self.fnCopyNpaste(driver , subject)
            if _bool == False:
                rt = False 

            _bool = self.fnClick( driver , '/html/body/div[1]/div[1]/div/div/div[3]/div[4]/form/div[4]/div/textarea' )        
            self.fnCopyNpaste(driver,content)
            if _bool == False:
                rt = False                

            actions = driver.find_element(By.CSS_SELECTOR, 'body')
            actions.send_keys(Keys.PAGE_DOWN)    
            
            _bool = self.fnClick(driver , '//*[@id="btn_submit"]') #글쓰기 버튼        
            
            time.sleep( self.__g_wait )
            if _bool == False:
                rt = False         

            if _bool:
                self.fnCapture( driver , list[0]+'_글쓰기' ) #캡쳐
                self.fnDbBoardUse({'site_domin':site_domin , 'type_nm':type_nm , 'seq':seq}) # 사용이력 남기기
            time.sleep(0.5)
            return rt
        except Exception as e:
            return False



    def fnMain(self):
        datas = self.readfile("C:\\ncnc_class\\프렌즈 정보.xlsx") # 0:id , 1:ps , 2:출석  , 3,4,5 : 댓글 , 6:제목, 7:내용
        for i in datas:
            driver = self.fnDriver()          # 드라이버생성

            #로그인 한다. - begin
            for j in range(0,20):
                aa = self.fnLogin(driver , i )
                if aa :         # 로그인
                    print(i[0],' : 로그인 완료.')
                    break
            #로그인 한다. - end
            

            # 출석체크 - begin
            for j in range(0,20):
                aa = self.fnAttendance(driver , i )    # 출석체크
                if aa :
                    print(i[0],' : 출석체크 완료.')
                    break
            # 출석체크 - end            

            # 댓글달기 - begin        
            cnt = 0
            for j in range(0,20):
                ''''''        
                r_list = [1,2,3,4,5]
                line = random.sample(r_list,3)   # 글선택번호            
                aa = self.fnReply(driver , i ,  line[cnt] )     # 댓글 3개 달기
                if aa :
                    print(i[0],' : ', cnt,'번째 댓글쓰기 완료')
                    cnt += 1
                if cnt == 3:
                    print(i[0], ' 댓글쓰기 완료.')
                    break
            # 댓글달기 - end
            
            # 글쓰기 - begin
            for j in range(0,10):
                aa = self.fnWrite(driver , i )           # 글쓰기        
                if aa:
                    print(i[0],' : ', '글쓰기 완료.')
                    break        
            # 글쓰기 - end
            driver.quit()                   # 드라이버 종료    
            
        w2ji.send_telegram_message( '프렌즈 작업이 완료 되었습니다. 확인은 필요힙니다. 캡쳐를 확인하세요.' )
        

    def  fntest(self):
        '''테스트 함수'''    
        datas = self.readfile("C:\\ncnc_class\\프렌즈 정보.xlsx") # 0:id , 1:ps , 2:출석  , 3,4,5 : 댓글 , 6:제목, 7:내용
        driver = self.fnDriver()                 # 드라이버생성
        #time.sleep(1)
        self.fnLogin(driver , datas[0] )         # 로그인
        #self.fnAttendance(driver , datas[0] )    # 출석체크
        self.fnReply(driver , datas[0] , 2 )     # 댓글 3개 달기
        #self.fnWrite(driver , datas[0])     # 글쓰기
        

if __name__ == "__main__":  
    '''프렌즈 출석'''    
    
    fr = friends() # 선언
    fr.fnDbcon() # db 변경 할당.
    #fr.fnMain() #메인프로세스 전체 수행부분
    fr.fntest() # 테스트 프로세스

    
    