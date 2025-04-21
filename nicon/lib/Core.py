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

''' 자동화 수행 클래스
1.0.0 생성.
'''

class Core:
    ''' Work.py 혹은 work_army.py 가 수행되는 클래스'''
    def __inti__ (self):
        ''' 초기화 함수 현재 기능 없음'''

    def fndbclick(self , xy , wait_time:float):
        '''더블클릭'''
        pyautogui.doubleClick(x= xy.x  , y= xy.y)        
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
        pyperclip.copy( txt )
        pyautogui.hotkey('ctrl', 'v')                   
        time.sleep( wait_sec ) #대기
    
    def fnwrite(self, txt : str , wait_sec:float):
        '''복사 타이핑'''
        for n in txt:
            pyautogui.press(n)
        
        time.sleep( wait_sec ) #대기        
    
    def fnkey(self , txt : str , cnt : int , wait_sec:float ):
        '''키 입력'''
        if txt == 'ctrl+a': # 전체선택
            pyautogui.hotkey('ctrl', 'a' , interval=0.2)            
        elif str == 'ctrl+c': # 복사
            pyautogui.hotkey('ctrl', 'c' , interval=0.2)            
        elif str == 'ctrl+v': # 붙여넣기
            pyautogui.hotkey('ctrl', 'v' , interval=0.2)                        
        else : # 이외 전체 키 처리.
            pyautogui.press( txt , presses = cnt , interval=0.2)  

        time.sleep( wait_sec ) #대기
        time.sleep( 0.5 )

    def fnRandWait(self):
        '''랜덤 대기 시간'''
        rand_wait_t = round(random.uniform(3,20),1)
        time.sleep( rand_wait_t )        
    
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
        file_nm     = base_dttm+'_'+txt
        file_name   = r"c:\\ncnc_class\\capture\\{}{}".format( file_nm ,'.png') 
        pyautogui.screenshot( file_name , region=(r11.x , r11.y , capture_width, capture_height))    
        time.sleep( wait_sec ) #대기       

    def fnDragNDrop(self , rand , wait_sec:float):
        ''' 드래그 앤 드롭 '''
        d1 = rand.get(15)
        d2 = rand.get(16)     
        pyautogui.moveTo( d1 )          # 마우스 이동     
        pyautogui.dragTo( d2.x , d2.y , duration= 0.3)
        time.sleep( wait_sec )    #대기   



    def fnReadCapture(self , step_name:str , xy  , txt:str , rand , wait_sec:float ):
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
        self.fnclick( xy , self.__waitTime )    #클릭            
        self.fnwrite( capcha_number )             ## 타이핑
        time.sleep( wait_sec ) #대기        