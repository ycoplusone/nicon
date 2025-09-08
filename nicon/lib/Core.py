import pyautogui
import pyperclip
import time
import random
from datetime import datetime
from pytz import timezone
import os
import base64
import openai                       # pip install openai == 0.28.0
import re
import ctypes



''' 자동화 수행 클래스
1.0.0 생성.
'''

class Core:
    
    inputWait = False # 입력대기 z키 입력 대기 제어 변수
    pyautogui.FAILSAFE = False

    ''' Work.py 혹은 work_army.py 가 수행되는 클래스'''
    def __inti__ (self):
        ''' 초기화 함수 현재 기능 없음'''
        pyautogui.FAILSAFE = False

    def fndbclick(self , xy , wait_time:float):
        '''더블클릭'''
        pyautogui.doubleClick(x= xy.x  , y= xy.y)                
        time.sleep( wait_time )         
    
    def fntripleClick(self , xy , wait_time:float):
        '''트리풀'''
        #pyautogui.tripleClick(x= xy.x  , y= xy.y)                
        pyautogui.click(x= xy.x  , y= xy.y, clicks=3)
        time.sleep( wait_time )         

    def fnclick(self , xy , wait_time:float):
        '''클릭 함수 (좌표 , 대기시간)'''
        pyautogui.click(x= xy.x  , y= xy.y)        
        time.sleep( wait_time ) 
    
    def fnUrl(self, url , wait_time:float):
        '''url 처리 복사 붙여넣기'''
        pyautogui.hotkey('del')   
        pyperclip.copy( url )
        pyautogui.hotkey('ctrl', 'v')   
        pyautogui.hotkey('enter')         
        time.sleep( (wait_time) )         
    
    def fnpaste(self , txt:str , wait_sec:float ):
        '''복사 붙여넣기'''        
        txt = '' if txt == 'nan' else txt
        pyperclip.copy( txt )
        pyautogui.hotkey('ctrl', 'v')                   
        time.sleep( wait_sec ) #대기
    
    def fnwrite(self, txt : str , wait_sec:float):
        '''복사 타이핑'''
        txt = '' if txt == 'nan' else txt
        for n in txt:
            pyautogui.press(n)
        
        time.sleep( wait_sec ) #대기        
    
    def fnkey(self , txt : str , cnt : int , wait_sec:float ):
        '''키 입력'''
        if txt == 'ctrl+a': # 전체선택
            pyautogui.hotkey('ctrl', 'a' )
        elif txt == 'ctrl+c': # 복사
            pyautogui.hotkey("ctrl", "c")
        elif txt == 'ctrl+v': # 붙여넣기
            pyautogui.hotkey("ctrl", "v")
        else : # 이외 전체 키 처리.
            pyautogui.press( txt , presses = cnt , interval=0.2)  

        time.sleep( wait_sec ) #대기
        time.sleep( 0.5 )

    def fnRandWait(self):
        '''랜덤 대기 시간'''
        rand_wait_t = round(random.uniform(3,20),1)
        time.sleep( rand_wait_t )    

    def fnInputWait( self ):
        '''입력 대기 외부 키 입력 이벤트를 위한 함수'''
        print('\t\t (Z키 또는 +키) 입력대기 (Z키 또는 +키)를 입력해서 다음 단계를 수행하세요.','?'*10)
        while True:
            if not self.inputWait:
                break
            time.sleep( 1 ) #대기            
            

    
    def fnRandClick(self , rand , waitTime : float , wait_sec:float):
        '''랜덤 클릭'''
        r = random.randrange(0,3)
        r0 = rand.get(0)
        r1 = rand.get(1)
        r2 = rand.get(2)
        r3 = rand.get(3)
        if r == 0:
            self.fnclick( r0 , waitTime ) #클릭   
        elif r == 1:
            self.fnclick( r1 , waitTime ) #클릭   
        elif r == 2:
            self.fnclick( r2 , waitTime ) #클릭   
        elif r == 3:
            self.fnclick( r3 , waitTime ) #클릭   
        time.sleep( wait_sec ) #대기        
    
    def fnMultClick(self , rand , waitTime : float , wait_sec:float):
        ''' 다중 선택 '''
        r0 = rand.get(0)
        r1 = rand.get(1)
        r2 = rand.get(2)
        r3 = rand.get(3)                                            
        self.fnclick( r0 , waitTime ) #클릭                           
        self.fnclick( r1 , waitTime ) #클릭   
        self.fnclick( r2 , waitTime ) #클릭                           
        self.fnclick( r3 , waitTime ) #클릭   
        time.sleep( wait_sec ) #대기         
    
    def fnMultRandClick(self , rand , waitTime : float , wait_sec:float):
        ''' 다중 랜덤 클릭'''
        numbers = [0,1,2,3]
        n = random.sample(numbers,4)            
        r0 = rand.get(n[0])
        r1 = rand.get(n[1])
        r2 = rand.get(n[2])
        r3 = rand.get(n[3])
        self.fnclick( r0 , waitTime ) #클릭   
        self.fnclick( r1 , waitTime ) #클릭   
        self.fnclick( r2 , waitTime ) #클릭   
        self.fnclick( r3 , waitTime ) #클릭 
        time.sleep( wait_sec ) #대기       
    
    def fnAppointClick(self , rand , appoint : int ,  waitTime : float , wait_sec:float):
        ''' 지정된 좌표 클릭 '''          
        r0 = rand.get( appoint )
        self.fnclick( r0 , waitTime ) #클릭   
        time.sleep( wait_sec ) #대기     

    def fnCapture(self , r11 , r12 , txt:str ,wait_sec:float):
        '''화면 캡쳐'''
        capture_width   = r12.x - r11.x
        capture_height  = r12.y - r11.y

        base_dttm   = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d_%H%M%S')
        base_dt     = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
        try:
            os.mkdir('c:\\ncnc_class\\capture')
        except Exception as e:
            '''폴더 생성 있으면 넘어간다.''' 
        file_nm     = txt+'_'+base_dttm
        file_name   = r"c:\\ncnc_class\\capture\\{}{}".format( file_nm ,'.png') 
        pyautogui.screenshot( file_name , region=(r11.x , r11.y , capture_width, capture_height))    
        time.sleep( wait_sec ) #대기       

    '''
    def fnDragNDrop(self , rand , wait_sec:float):
        # 드래그 앤 드롭
        d1 = rand.get(15)
        d2 = rand.get(16)     
        pyautogui.moveTo( d1 )          # 마우스 이동     
        pyautogui.dragTo( d2.x , d2.y , duration= 0.3)
        time.sleep( wait_sec )    #대기 
    '''
    def fnDragNDrop(self , rand , wait_sec:float):
        #드래그 앤 드롭
        d1 = rand.get(15)
        d2 = rand.get(16)     
        pyautogui.moveTo( d1 )          # 마우스 이동    
        pyautogui.mouseDown(button='left') 
        pyautogui.dragTo( d2.x , d2.y , duration= 0.3  ,button='left' , mouseDownUp =False )
        time.sleep(0.2)
        pyautogui.mouseUp(button='left')
        #pyautogui.dragRel(d2.x , d2.y , duration= 1 )
        time.sleep( wait_sec )    #대기         

    def fnReadCapture(self , step_name:str , xy  , txt:str , rand ,waitTime : float , wait_sec:float ):
        '''자동등록방지[숫자] 인식 구간.'''
        # 캡쳐후 해당 부분 챗GPT에 인식후 복사하는 방식.
        # 캡쳐후 인식한 숫자를 파일에 같이 넣어 이후 신뢰도를 확인한다.
            
        ask_txt = '이 이미지에서 숫자만 읽어줘.'
        system_txt = '당신은 이미지에서 숫자를 정확하게 인식하는 AI입니다.'
        
        if step_name == '자방[숫자]':
            ask_txt = '이 이미지에서 숫자만 읽어줘.'
            system_txt = '당신은 이미지에서 숫자를 정확하게 인식하는 AI입니다.'
        elif step_name == '자방[문자]':
            ask_txt = '이 이미지에서 문자만 읽어줘.'
            system_txt = '당신은 이미지에서 문자를 정확하게 인식하는 AI입니다.'
        elif step_name == '자방[혼합]':
            ask_txt = '이 이미지에서 문자와 숫자만 읽어줘.'
            system_txt = '당신은 이미지에서 문자와 숫자를 정확하게 인식하는 AI입니다.'

        r11 = rand.get(11)
        r12 = rand.get(12)
        capture_width   = r12.x - r11.x
        capture_height  = r12.y - r11.y

        base_dttm   = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d_%H%M%S')
        base_dt     = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')    
        try:
            os.mkdir('c:\\ncnc_class\\recapcha')
        except Exception as e:
            '''폴더 생성 있으면 넘어간다.'''  
        file_nm     = base_dttm+'_'+txt         # str(_j[0])
        file_name   = f"c:\\ncnc_class\\recapcha\\{file_nm}.png"
        pyautogui.screenshot( file_name , region=(r11.x , r11.y , capture_width, capture_height))    
        
        def encode_image(image_path):
            """이미지를 Base64로 인코딩하는 함수"""
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        
        def recognize_numbers(image_path):
            """
            이미지에서 숫자를 인식하는 함수 (GPT-4-Vision 사용)
            """
            openai.api_key = os.environ.get('open_api_key')

            base64_image = encode_image(image_path)  # 이미지 Base64 변환

            response = openai.ChatCompletion.create(
                model="gpt-4o",  # GPT-4-Vision 모델 사용
                messages=[
                    {"role": "system", "content": system_txt },
                    {"role": "user", "content": [
                        {"type": "text", "text": ask_txt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]}
                ],
                max_tokens=100
            )
            # 이 이미지에 있는 숫자를 모두 읽어주세요.
            return response["choices"][0]["message"]["content"]
        
        capcha_number = recognize_numbers(file_name) 
        if step_name == '자방[숫자]':
            capcha_number = re.sub(r'[^0-9]', '', capcha_number) # 숫자만 산출하는 정규식     
        elif step_name == '자방[문자]':
            capcha_number = re.sub(r'[^a-zA-Z]', '', capcha_number) # 문자만 산출하는 정규식
        elif step_name == '자방[혼합]':
            capcha_number = re.sub(r'[^a-zA-Z0-9]', '', capcha_number) # 숫자와 문자만 산출하는 정규식       

        new_file_name   = f"c:\\ncnc_class\\recapcha\\{file_nm}_{capcha_number}.png" # 새로 변경할 파일 이름
        
        os.rename(file_name ,new_file_name )     # 파일 이름 변환.            
        self.fnclick( xy , waitTime )    #클릭            
        self.fnwrite( capcha_number , 0.1 )             ## 타이핑
        time.sleep( wait_sec ) #대기        

    def run_as_admin(self , exe_path, params, wait_time :float  ):
        # ShellExecuteW를 통해 관리자 권한으로 실행
        ctypes.windll.shell32.ShellExecuteW(
            None,                # hwnd
            "runas",             # operation
            exe_path,            # 실행할 파일
            params,              # 파라미터
            None,                # 디렉토리 (None이면 현재 디렉토리)
            1                    # show command (1: SW_SHOWNORMAL, 0: SW_HIDE)
        )
        time.sleep(wait_time)


    def fnMain(self , step_name : str , mdata , cdata  ): 
        '''메인 프로세스
        step_name   : 각 단계의 명령어
        m_data      : 매크로 데이터 한행.
        c_data      : 첨부 데이터 한행.
        '''
        seq             = mdata['seq']
        xy              = mdata['click_xy']         # self.fnArrayGet( self.__click_xy      , i )
        evn             = mdata['click_evn']        # self.fnArrayGet( self.__click_evn     , i )
        rand            = mdata['click_rand']       # self.fnArrayGet( self.__click_rand    , i )
        xy_wait         = mdata['click_xy_wait']    # self.fnArrayGet( self.__click_xy_wait , i )
        key0            = mdata['key0']             # self.fnArrayGet( self.__key0          , i )
        key0_wait       = mdata['key0_wait']        # self.fnArrayGet( self.__key0_wait     , i )  #키 입력후 대기 아님 키 입력 횟수 이다.
        key1            = mdata['key1']             # self.fnArrayGet( self.__key1          , i )
        key1_wait       = mdata['key1_wait']        # self.fnArrayGet( self.__key1_wait     , i )
        waitTime        = float( mdata['step_wait_time']) # 기존 waitTime 와 동일
        job_name        = mdata['file_name']        # 실행 작엄명
        
        print('\t 행번호 : ', seq ,' , 작업구분 : ', step_name , (f", 키부분 : {key0}" if step_name == '방향전환' else "")  )    
        if ( step_name == '클릭'):
            for j in range(0, int(evn)): #반복 실행한다.
                self.fnclick( xy = xy , wait_time = waitTime  )
            time.sleep( float(xy_wait) ) #대기

        elif ( step_name == '붙여넣기'):
            self.fnclick(xy=xy , wait_time = 0.2 ) #클릭Core
            n       = int(evn)                    
            txt     = cdata[n]
            self.fnpaste( txt , float(xy_wait) )  # 붙여넣기

        elif ( step_name == '글씨쓰기'):
            self.fnclick(xy=xy , wait_time = waitTime)  #클릭
            n   = int(evn)                    
            txt     = cdata[n]
            self.fnwrite( txt=txt , wait_sec= float(xy_wait) )  #타이핑

        elif ( step_name == '선택하기') :
            self.fnclick(xy=xy , wait_time=waitTime) #클릭
            self.fnRandClick( rand=rand , waitTime=waitTime , wait_sec=float(xy_wait)  )  # 랜덤 클릭

        elif ( step_name == '중복선택') :
            self.fnclick(xy=xy , wait_time=waitTime) #클릭   
            self.fnMultClick(rand=rand , waitTime=waitTime , wait_sec=float(xy_wait))  # 다중선택

        elif ( step_name == '랜덤선택') :
            self.fnclick(xy=xy , wait_time=waitTime) #클릭
            self.fnMultRandClick(rand=rand , waitTime=waitTime , wait_sec=float(xy_wait)) # 다중 랜덤 클릭
        
        elif ( step_name == '지정선택') :
            self.fnclick(xy=xy , wait_time=waitTime) #클릭
            n   = int(evn)      # 엑셀의 가져올 컬럼의 번호를 읽어온다.                    
            txt = cdata[n]      # 엑셀의 값의 특정 커럼값을 가져온다.
            appoint = int(txt)  # 값을 정수형으로 변경한다.
            self.fnAppointClick( rand=rand , appoint=appoint , waitTime=waitTime , wait_sec=float(xy_wait) ) # 지정된 좌표 클릭
            
        elif ( step_name == '방향전환'):        
            if (key0 != 'ctrl+a' or key0 != 'ctrl+c' or key0 != 'ctrl+v' ):
                self.fnclick(xy=xy , wait_time=waitTime) #클릭
            self.fnkey(     txt=key0    , cnt=int(key0_wait) , wait_sec=float(xy_wait)) #키 입력

        elif ( step_name == '무시'):
            '''행동 없음.'''
        elif ( step_name == '랜덤대기'):
            self.fnRandWait() #랜덤 대기 시간

        elif ( step_name == '캡쳐'):
            '''캡쳐'''
            r11 = rand.get(11)
            r12 = rand.get(12)
            file_name = f'{job_name[5:10]}_{cdata[0]}' # 작업명_수행데이터의 열값
            self.fnCapture(r11=r11 , r12=r12 , txt= file_name , wait_sec=float(xy_wait) ) # 캡쳐
        
        elif( step_name =='D&D') :
            '''드래드 & 드랍'''
            self.fnDragNDrop( rand=rand , wait_sec= float(xy_wait) ) # 드래그 앤 드랍
        
        elif( (step_name == '자방[숫자]') or (step_name == '자방[문자]') or (step_name == '자방[혼합]') ) :
            '''자동등록방지[숫자] 인식 구간.'''
            self.fnReadCapture( step_name=step_name , xy=xy , txt= str(cdata[0]) ,rand=rand , waitTime=waitTime , wait_sec=float(xy_wait) ) # 캡쳐후 인식한 숫자를 파일에 같이 넣어 이후 신뢰도를 확인한다.
        
        elif( step_name =='브라우저') :
            exe_path    = os.environ.get('brower_path')
            exe_option  = os.environ.get('brower_options')  
            self.run_as_admin(exe_path , exe_option , float(xy_wait))