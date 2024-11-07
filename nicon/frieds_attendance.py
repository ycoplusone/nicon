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
from openai import OpenAI #챗gpt api
import lib.util as w2ji
import re
import pymysql
import sys




class friends(object):
    __version = '2411.2' #버전.
    __g_wait = 5
    __conn = ''

    __nick_name = '' # 로그인후 닉네임을 가져와서 할당한다.

    def __init__(self):
        self.load_env()

    def load_env( self , filepath=".env"): # .env 파일 읽기 함수
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):  # 공백과 주석(#) 생략                
                    key, value = line.split("=", 1)    # "KEY=VALUE" 형식으로 분리
                    key = key.replace(' ','')
                    value = value.lstrip().rstrip() #양쪽 공백제거                
                    value = value.strip('"').strip("'") # 양쪽 떠블 싱글 쿼테이션 제거
                    os.environ[key] = value.strip('"').strip("'")  # 환경변수 설정

    def fnDbcon(self):
        '''db연결'''        
        self.__conn = pymysql.connect(  host        = os.environ.get("mysql_url")
                                        , user      = os.environ.get("mysql_id")
                                        , password  = os.environ.get("mysql_ps")
                                        , db        = os.environ.get("mysql_db")
                                        , charset   = os.environ.get("mysql_charset")
                                    )    
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
            " update friends_board_summary "
            " set use_yn = 'N'  "
            " where DATE_FORMAT(use_dt ,'%Y%m%d') <= DATE_FORMAT(ADDDATE(now() , -180),'%Y%m%d') " 
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
                " from friends_board_summary  "
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
            " update friends_board_summary  "
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
                    
            client = OpenAI( api_key = os.environ.get("open_api_key") )
            
            query = f"'{text}'에 대한 20자이내의 짧은 댓글."  
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
            rt_txt = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s,.!?;]", "", rt_txt) #re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", rt_txt)
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
        _rt.get('https://friends001.com/bbs/login.php?url=%2F')    
        _rt.implicitly_wait(15)  
        
        time.sleep(1)  
        return _rt

    def fnCapture(self , driver , str):
        try:
            base_dttm   = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d_%H%M%S')
            os.mkdir('c:\\ncnc_class\\friends')
        except Exception as e:           ''''''
            

        file_name   = r"c:\\ncnc_class\\friends\\{}_{}{}".format( base_dttm , str ,'.png') 
        try:
            driver.save_screenshot(file_name)
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
    
    def fnGetAttribute(self, driver , xpath_str , attr_str): # attribute 읽기
        '''태그 읽어오기'''
        time.sleep(0.5)
        rt_str = ''
        try:            
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_str )))
            rt_str  = element.get_attribute( attr_str )
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

    def fnGetNickName(self , driver):
        self.__nick_name ='' # 닉네임 초기화
        driver.get('https://friends001.com/bbs/mypage.php') #닉네임을 가져가기위해서 페이지를 이동한다.
        time.sleep(2)
        self.__nick_name = self.fnGetTag(driver,'/html/body/div[1]/div[1]/div/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/b/a/span')
        print( f'self.__nick_name : {self.__nick_name}' )

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
            
    def fnReply(self , driver, list, page):
        '''댓글쓰기'''            
        try:
            rt = True    
            rep_txt = '' #댓글내용           
            artcle_seq = [1,2,3,4,5,6,7,8,10]
            for seq in artcle_seq: # 게시판 목록 1~10까지에서
                rt = True  #초기화한다. 중간에 False로 반복구간을 다시 처리해야 한다.
                url = f'https://friends001.com/bbs/board.php?bo_table=free&page={page}'
                print('페이지',url)
                driver.get( url )     
                driver.implicitly_wait(15)
                time.sleep( self.__g_wait )
                actions = driver.find_element(By.CSS_SELECTOR, 'body')
                actions.send_keys(Keys.DOWN)    
                actions.send_keys(Keys.DOWN)    
                actions.send_keys(Keys.DOWN)    
                actions.send_keys(Keys.DOWN)    
                actions.send_keys(Keys.DOWN)                   
                time.sleep(1)                            
                _nick_nm = self.fnGetTag(driver,f'/html/body/div[1]/div[1]/div/div/div[3]/section/div/form/div[1]/ul/li[{seq}]/div[3]/a/span') # 글의 작성자명가져오기
                _nick_nm = _nick_nm.lstrip().rstrip() #양쪽 공백제거
                print(f'닉네임 : {self.__nick_name} , 글이름 : {_nick_nm}')
                if self.__nick_name != _nick_nm: # 계정의 닉네임과 글의 닉네임이 다르면
                    tag = f"/html/body/div[1]/div[1]/div/div/div[3]/section/div/form/div[1]/ul/li[{seq}]/div[2]/a"        
                    _bool = self.fnClick( driver , tag ) # 해당글 클릭
                    time.sleep( self.__g_wait )
                    if _bool == False:
                        rt = False
                    
                    max_reply_cnt = self.fnGetTag(driver,'/html/body/div[1]/div[1]/div/div/div[3]/div[3]/div[1]/span') # 댓글수 가져오기
                    for reply_seq in range(1,int(max_reply_cnt)+1):
                        try:
                            _reply_nick = self.fnGetTag(driver,f'/html/body/div[1]/div[1]/div/div/div[3]/div[3]/section[2]/div[{reply_seq}]/div[2]/div[1]/b/a/span') # 댓글 장성자 
                            _reply_nick = _reply_nick.lstrip().rstrip() #양쪽 공백제거
                            print(f'self.__nick_name:{self.__nick_name},_temp_txt:{_reply_nick}')
                            if self.__nick_name == _reply_nick:
                                rt = False                                
                                break
                        except Exception as e:
                            print('reply_seq 에서 오류')
                            break;
                    if rt == True:
                        print('글 댓글에 해당 사용자의 댓글은 없습니다.')
                        break
            
            if rt == True:
                # 글읽기
                ask_subject = self.fnGetAttribute(driver ,'/html/body/div[1]/div[1]/div/div/div[3]/div[3]/section[1]/article/h1' , 'content' )            
                ask_subject = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s,.!?;]", "", ask_subject) # 특수문자 제외
                ask_txt     = self.fnGetTag(driver,'//*[@id="thema_wrapper"]/div[1]/div/div/div[3]/div[3]/section/article/div[2]/div[2]')

                if (ask_txt == '') or (ask_subject == '') :
                    rt = False
                else :    
                    _temp_txt = ask_subject+' '+ask_txt
                rep_txt = self.fnOpenAiAsk(_temp_txt)            

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
                    try:
                        time.sleep(1)
                        self.fnCapture( driver , list[0]+'_댓글' ) #캡쳐      
                        aa = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", ask_txt)  # 특수문자 제외
                        aa = aa[0:1024]
                        bb = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", rep_txt)  # 특수문자 제외        
                        bb = bb[0:1024]
                        self.fnDbreply({'query': aa ,'result':bb}) # 인공지능 댓글 기록하기.
                    except Exception as e:
                        print('마지막',e)
                time.sleep(0.5)
            return rt
        except Exception as e:
            return False
       
    def fnWrite( self , driver, list ):
        '''글쓰기'''
        try :
            subject = list[6]
            content = list[7]
            '''
            str = self.fnDbBoard()
            site_domin  = str[0]['site_domin']
            type_nm     = str[0]['type_nm']
            seq         = str[0]['seq']
            subject     = str[0]['subject']
            content     = str[0]['content']            
            '''
            print('subject : ', subject)
            print('content : ', content)
            rt = True
            url = 'https://friends001.com/bbs/write.php?bo_table=free'
            driver.get( url )
            driver.implicitly_wait(15)
            time.sleep( 2 )   

            actions = driver.find_element(By.CSS_SELECTOR, 'body')
            actions.send_keys(Keys.DOWN)    
            actions.send_keys(Keys.DOWN)               
            actions.send_keys(Keys.DOWN)  
            actions.send_keys(Keys.DOWN)  
            actions.send_keys(Keys.DOWN)  
            actions.send_keys(Keys.DOWN)  
            actions.send_keys(Keys.DOWN)  
            actions.send_keys(Keys.DOWN)  
            time.sleep(1)

            _bool = self.fnClick( driver , '/html/body/div[1]/div[1]/div/div/div[3]/div[4]/form/div[3]/div/div/input' )        
            self.fnCopyNpaste(driver , subject)
            if _bool == False:
                rt = False 

            _bool = self.fnClick( driver , '/html/body/div[1]/div[1]/div/div/div[3]/div[4]/form/div[4]/div/textarea' )        
            self.fnCopyNpaste(driver,content)
            if _bool == False:
                rt = False                

            _bool = self.fnClick(driver , '//*[@id="btn_submit"]') #글쓰기 버튼        
            
            time.sleep( self.__g_wait )
            if _bool == False:
                rt = False         

            if _bool:
                self.fnCapture( driver , list[0]+'_글쓰기' ) #캡쳐
                #self.fnDbBoardUse({'site_domin':site_domin , 'type_nm':type_nm , 'seq':seq}) # 사용이력 남기기
            time.sleep(0.5)
            
            return rt
        except Exception as e:
            return False

    def fnApplication( self ): # 포인트신청하기
        '''
        로그인후 
        id 값과 닉네임 값을 가져온다.
        페이지로 이동한다.
        '''
        datas = self.readfile("C:\\ncnc_class\\프렌즈 포인트.xlsx") # 0:id , 1:ps , 2:출석  , 3,4,5 : 댓글 , 6:제목, 7:내용
        
        for i in datas:
            try:
                condition = datetime.now(timezone('Asia/Seoul')).strftime('%H')
                if ( condition not in ['10','11','12','13','14','15','16','17','18','19'] ) :                    
                    print('*'*100)
                    print(f'현재 {condition}시 입니다. 실행을 종료 합니다.')
                    print('*'*100)
                    break
                else :
                    driver      = self.fnDriver()          # 드라이버생성
                    time.sleep(1)
                    _app_url    = 'https://friends001.com/bbs/write.php?bo_table=free_3'    # 신청 페이지 url
                    
                    _user_nick  = ''    # 닉네임
                    _user_id    = i[0]  # ID
                    _app_dt     = datetime.now(timezone('Asia/Seoul')).strftime('%m월 %d일')    # 신청일자 10월 30일
                    _app_tm     = datetime.now(timezone('Asia/Seoul')).strftime('%p %H:%M')     # 신청시간 AM 11:02
                    _app_tx     = '(기존) GS25 1만원'    # 신청내용 (기존) GS25 1만원


                    id_tag = f"$('#login_id').val('{i[0]}');"
                    ps_tag = f"$('#login_pw').val('{i[1]}');"    
                    
                    self.fnScript(driver, id_tag )  # id 입력
                    self.fnScript(driver, ps_tag )  # ps 입력
                    self.fnClick( driver , '/html/body/div[1]/div[1]/div/div/div/div/div[1]/div[2]/form/div[3]/div[2]/button')  # 로그인버튼
                    time.sleep(1)    
                    driver.get('https://friends001.com/bbs/mypage.php') #닉네임을 가져가기위해서 페이지를 이동한다.
                    time.sleep(2)
                    _user_nick     = self.fnGetTag(driver,'/html/body/div[1]/div[1]/div/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/b/a/span')            
                    _app_text  = (
                    f"아이디 : {_user_id} \n\n"
                    f"닉네임 : {_user_nick} \n\n"
                    f"신청 날짜 : {_app_dt} \n\n"
                    f"신청 시간 : {_app_tm} \n\n"
                    f"신청 내용 : {_app_tx}"                           
                    ) #신청문구
                    print('*'*30)
                    print( _app_text )
                    print('*'*30)

                    driver.get( _app_url )
                    time.sleep(2)
                    self.fnClick( driver , '/html/body/div[1]/div[1]/div/div/div[3]/div[4]/form/div[3]/div/div/input' ) 
                    time.sleep(0.5)
                    self.fnCopyNpaste(driver , '기프티콘 신청합니다')
                    time.sleep(0.5)
                    actions = driver.find_element(By.CSS_SELECTOR, 'body')
                    for x in range(0,9):
                        actions.send_keys(Keys.DOWN)            

                    self.fnClick( driver , '/html/body' )                
                    time.sleep(0.5)
                    self.fnCopyNpaste(driver,_app_text)                
                    time.sleep(0.5)
                    actions = driver.find_element(By.CSS_SELECTOR, 'body')
                    actions.send_keys(Keys.DOWN)            
                    actions.send_keys(Keys.DOWN)            
                    actions.send_keys(Keys.DOWN)            
                    actions.send_keys(Keys.DOWN)            

                    self.fnClick(driver , '//*[@id="btn_submit"]') #글쓰기 버튼  
                    time.sleep(1)      
                    self.fnCapture( driver , i[0]+'_신청' ) #캡쳐                
                    rest_time = 60 + random.randint(60, 100)
                    print(f'{rest_time} 초 대기합니다.')
                    driver.quit()
                    time.sleep( rest_time )
            except Exception as e:
                print('에러')
            
        




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
            
            #닉네임 가져오기 - begin
            self.fnGetNickName(driver) #닉네임 가져오기
            #닉네임 가져오기 - end
            '''
            # 출석체크 - begin
            for j in range(0,20):
                aa = self.fnAttendance(driver , i )    # 출석체크
                if aa :
                    print(i[0],' : 출석체크 완료.')
                    break
            # 출석체크 - end            
            
            # 댓글달기 - begin        
            cnt = 0
            pages = [1,2,3,4,5,6,7,8,9,10]
            page = random.sample(pages,10)   # 글선택번호        
            for j in range(0,20):
                ''''''                        
                aa = self.fnReply(driver , i , page[cnt]  )     # 댓글 3개 달기                
                if aa :
                    print(i[0],' : ', cnt,'번째 댓글쓰기 완료')
                    cnt += 1
                if cnt == 3:
                    print(i[0], ' 댓글쓰기 완료.')
                    break
                print('오잉?',j,aa,cnt)
                
            # 댓글달기 - end
            '''
            # 글쓰기 - begin
            for j in range(0,10):
                aa = self.fnWrite(driver , i )           # 글쓰기        
                if aa:
                    print(i[0],' : ', '글쓰기 완료.')
                    break        
            # 글쓰기 - end
            driver.quit()                   # 드라이버 종료    
            
        w2ji.send_telegram_message( '프렌즈 작업이 완료 되었습니다. 확인은 필요힙니다. 캡쳐를 확인하세요.' )
        
    def fnChk(self): # 출석체크만
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

    def fnEvent(self): # 이벤트 프로그램
        datas = self.readfile("C:\\ncnc_class\\프렌즈 정보.xlsx") # 0:id , 1:ps , 2:출석  , 3,4,5 : 댓글 , 6:제목, 7:내용
        for i in datas:
            driver = self.fnDriver()          # 드라이버생성            
            
            for j in range(0,20): #로그인 한다. - begin
                aa = self.fnLogin(driver , i )
                if aa :         # 로그인
                    print(i[0],' : 로그인 완료.')
                    break      

            time.sleep(2)
            url1 = 'https://friends001.com/bbs/board.php?bo_table=daily_event&sca=%EC%A7%84%ED%96%89%EC%A4%91' # 진행이벤트 페이지 이동
            driver.get( url1 )
            time.sleep(2)

            state_txt = self.fnGetTag(driver , '/html/body/div[1]/div[1]/div/div/div[3]/section/div[2]/form/div[2]/li[1]/div[1]/div[1]/div[1]') 
            if state_txt == '진행중':
                '''진행중 추가 개발한다.'''
                


                  
    
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
    args = sys.argv # 실행시 매개값으로 실행 방법 구분 2번째 값이 특정 값 무엇이면 처리하는 방식이다.
    print( args  , len(args) )
    if len(args) == 1:
        print( '로그인 & 댓글 & 게시판글 신청.' )
        fr = friends() # 선언
        fr.fnDbcon() # db 변경 할당.
        fr.fnMain() #메인프로세스 전체 수행부분        
    elif (len(args) >= 2) and (args[1] == 'point'): # 신청으로 포
        print( '신청페이지 시작' )
        fr = friends() # 선언
        fr.fnApplication()
    elif (len(args) >= 2) and (args[1] == 'chk'): # 출체만
        print( '출석 시작' )
        fr = friends() # 선언
        fr.fnChk()
    elif (len(args) >= 2) and (args[1] == 'event'): # 이벤트 실행.
        ''''''
        fr = friends() # 선언
        fr.fnDbcon()
        fr.fnEvent() # 이벤트 수행.





    
    