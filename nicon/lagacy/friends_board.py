from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import pymysql
import re
import os
from dotenv import load_dotenv      # pip install python-dotenv , pip install dotenv 
from openai import OpenAI #챗gpt api
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class friends_board(object):
    __url = 'themoreschool.cafe24.com'
    __id = 'themoreschool'
    __ps = 'school2@'
    __db = 'themoreschool'    
    __charset = 'utf8'    
    __conn = ''

    load_dotenv() #환경변수 로딩    

    def fnDbcon(self):
        '''db 연결'''
        print('db1',self.__conn)
        self.__conn = pymysql.connect(host = self.__url , user = self.__id , password = self.__ps , db= self.__db , charset= self.__charset  )    
        print('db2',self.__conn)

    def fnUpsert( self , param ):
        '''데이터 insert  or update '''    
        try :
            cur = self.__conn.cursor()                        
            query = (
                "INSERT INTO friends_board_list (seq, subject, content, c_date, use_yn, site_domin, type_nm)"
                "                        VALUES({seq},'{subject}','{content}',now(), 'N', '{site_domin}', '{type_nm}') "
                " on DUPLICATE key update c_date = now()"
            )
            query = query.format( **param )     
            cur.execute( query )
            self.__conn.commit()
        except Exception as e:
            print( 'fnUpsert', e  )
        finally:
            pass      

    def fnGetlist(self):
        '''요약하기 위해서 글을 하나 가져온다.'''
        try :
            _lists = []
            query = (
                " select site_domin , type_nm , seq , subject , content  "
                " from friends_board_list  "
                " where use_dt is null "                
                " order by rand() limit 1 "
            )
            query = query.format( )
            cur = self.__conn.cursor(  pymysql.cursors.DictCursor)            
            cur.execute( query )            
            return cur.fetchall()         
        except Exception as e:
            print( 'fnGetlist => ' , e )     

    def fnSetlist(self , param):
        '''요약한 글을 summary에 넣는다.'''
        try :
            cur = self.__conn.cursor()
            query = (
                    "INSERT INTO friends_board_summary (site_domin , type_nm , seq, subject,content) "
                    " VALUES('{site_domin}', '{type_nm}',{seq},'{subject}','{content}')"
            )            
            query = query.format( **param )     
            print(query)
            cur.execute( query )
            self.__conn.commit()

            cur = self.__conn.cursor()                        
            query = (
            " update friends_board_list  "
            " set use_dt = now() "
            " WHERE site_domin='{site_domin}' AND type_nm='{type_nm}' AND seq={seq} "
            )            
            query = query.format( **param )                      
            cur.execute( query )
            self.__conn.commit()  

        except Exception as e:
            print( 'fnSetlist', e  )
        finally:
            pass  

    def fnOpenAiAsk( self , text , div ):
        '''인공지능'''
        try:
                    
            client = OpenAI( api_key = os.environ.get('open_api_key') )            
            query = ''
            if div == 'subject':
                query = f"'{text}' 맞춤법 교정"
            else :
                query = f"'{text}'의 문장을 정치, 시사, 날짜, 시간은 제외 하고 일상글 처럼 요약해줘 maxlength:100"
             
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
            rt_txt = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s,.!?;]", "", rt_txt)
            return rt_txt
        except Exception as e:
            print('error : ',e)

    def fnDriver( self, url ):
        '''
        크룸 초기화
        https://googlechromelabs.github.io/chrome-for-testing/#stable
        '''
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--log-level=3')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')


        # Add Image Loading inactive Flag to reduce loading time
        options.add_argument('--disable-images')
        options.add_argument('--blink-settings=imagesEnabled=false') 
        options.add_argument('--disable-gpu')  # GPU 가속 사용 안함 (★★★★★ 많이 사용)
        options.add_argument('--disable-extensions')  # 확장 프로그램 사용 안함
        options.add_argument('--incognito')  # 시크릿 모드로 실행
        options.add_argument('--disable-notifications')  # 알림 사용 안함      
        options.add_argument('--disable-features=DefaultPassthroughCommandDecoder')         
        options.add_argument('--enable-unsafe-swiftshader')         
        options.add_argument("--unsafely-treat-insecure-origin-as-secure=https://m.todayhumor.co.kr")
        
        # 속도 향상을 위한 옵션 해제
        prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
        options.add_experimental_option('prefs', prefs)        

        caps = DesiredCapabilities.CHROME
        caps["pageLoadStrategy"] = "none"
         
        #_rt = webdriver.Chrome('chromedriver.exe' , options=options , desired_capabilities=caps) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
        _rt = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options, desired_capabilities=caps)
        #_rt.get( url )    
        _rt.implicitly_wait(5)  
        time.sleep(1)  
        return _rt



    def getData1(self):
        ''' 데이터를 가져오는 첫번째 함수
        https://www.82cook.com/entiz/enti.php?bn=16&page=1
        '''
        for i in range(301,99999):            
            surl = f"https://www.82cook.com/entiz/enti.php?bn=16&page={i}"
            driver = self.fnDriver( surl )
            for j in range(2,27):
                try:
                    ''' 게시판글 2~26까지 있다. 전체 검색한다.'''                    
                    driver.get( surl )
                    tag_name = f'/html/body/div[3]/div/div[2]/div[2]/div[1]/table/tbody/tr[{j}]/td[1]/a'
                    tag1 = driver.find_element(By.XPATH, tag_name )
                    tag1_seq = tag1.text #시쿼스 번호
                    print(f"page : {i} , seq : {tag1_seq}")                
                    driver.find_element(By.XPATH, tag_name ).click() # 글 로 이동

                    tag1_subject = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/h4/span' ).text           
                    tag1_subject = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", tag1_subject)
                    tag1_content = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[6]' ).text
                    tag1_content = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", tag1_content)
                    param = {'seq':tag1_seq ,'subject' : tag1_subject ,'content': tag1_content ,'site_domin':'82cook','type_nm':'16' }
                    self.fnUpsert(param)
                except Exception as e:
                    ''''''
                    #print(f"error : {e} , page : {i} , seq : {tag1_seq}")
            driver.quit()
                
    def gettodayhumor(self , page):
        '''오늘의 유머'''
        urls = [
            'https://m.todayhumor.co.kr/list.php?table=coffee'
            ,'https://m.todayhumor.co.kr/list.php?table=psy'
            ,'https://m.todayhumor.co.kr/list.php?table=art'
            ,'https://m.todayhumor.co.kr/list.php?table=military2'
            ,'https://m.todayhumor.co.kr/list.php?table=military'
            ,'https://m.todayhumor.co.kr/list.php?table=computer'
            ,'https://m.todayhumor.co.kr/list.php?table=it'
            ,'https://m.todayhumor.co.kr/list.php?table=findmusic'
            ,'https://m.todayhumor.co.kr/list.php?table=readers'
            ,'https://m.todayhumor.co.kr/list.php?table=science'
            ,'https://m.todayhumor.co.kr/list.php?table=jisik'
            ,'https://m.todayhumor.co.kr/list.php?table=gomin'
            ,'https://m.todayhumor.co.kr/list.php?table=love'
            ,'https://m.todayhumor.co.kr/list.php?table=menbung'
            ,'https://m.todayhumor.co.kr/list.php?table=dream'
            ,'https://m.todayhumor.co.kr/list.php?table=diet'
            ,'https://m.todayhumor.co.kr/list.php?table=animal'
        ]
        driver = self.fnDriver( '' ) #드라이버생성
    
        for i in urls:
            url = i+f"&page={page}"
            driver.get(url)
            time.sleep(3)
            for j in range(1,31): # 게시판글 순서
                ''''''
                try:                                                
                    tag     = f'/html/body/a[{j}]' #글에 대한 tag                        
                    driver.find_element(By.XPATH, tag ).click() # 글 로 이동
                    time.sleep(1)
                    tag_url = driver.current_url #이동한글의 url
                    arr     = tag_url.split('&')
                    type_nm = arr[0].split('=')[1] #게시판구분
                    seq     = arr[1].split('=')[1] # seq번호                    
                    subject = driver.find_element(By.XPATH, '/html/body/div[5]' ).text                        
                    subject = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s,.!?;]", "", subject)
                    content = driver.find_element(By.XPATH, '/html/body/div[7]' ).text                        
                    content = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s,.!?;]", "", content)
                    param = {'site_domin':'todayhumor','type_nm':type_nm,'seq':seq,'subject':subject,'content':content}
                    print(f'{page} , type_nm : {type_nm} , seq : {seq}')
                    self.fnUpsert(param)                        
                    driver.back()       
                    time.sleep(1)
                except Exception as e:
                    print('error', e)
                    #print( f'error -> type_nm: {type_nm} , seq : {seq}' )
        driver.quit() #드라이버 종료
                   
                    


    def main(self):
        ''' 수행하기위함 메인 함수'''
        self.getData1()

    def test(self):
        ''' 단위 테스트를 위한 함수'''
        #self.getData1() 글 수집
        for i in range(0,10000):
            data = self.fnGetlist()[0]
            #print(data)
            site_domin = data['site_domin']
            type_nm = data['type_nm']
            seq = data['seq']
            subject = data['subject']
            content = fb.fnOpenAiAsk( data['content'] , 'content' )
            param = {'site_domin':site_domin , 'type_nm':type_nm ,'seq':seq , 'subject':subject , 'content':content}
            #print(param)
            self.fnSetlist(param)        



if __name__ == "__main__":  
    '''게시판 글 수집하기
    
    수집한 데이터를 mysql 에 데이터를 넣는다.        
    '''
    fb = friends_board()    
    fb.fnDbcon()
    for page in range(7,37): # 게시판글 순서
        print('*'*20,'시작')
        fb.gettodayhumor(page)
        print('*'*20,'끝')

    


    
