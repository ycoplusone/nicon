from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import datetime
from pytz import timezone
from PIL import ImageGrab , Image
import lib.util as w2ji
import re
import pyautogui
import pyperclip
import time
import random
import os

''' 자동화 클래스
'''


class Work(QThread):
    __title_nm          = '' #프로그램명칭
    __url_xy            = () # url 클릭 좌표
    __url_xy_wait       = 0.5 # 0.5 초 기본 대기 url 클릭후 대기
    __url_path          = '' #url 주소
    __url_path_wait     = 1 # 2초 기본 대기 url 주소 입력후 대기시간
    __cvs_path          = '' # cvs 파일 위치
    __div               = {} #선택값    
    __click_xy          = {} #클릭    
    __click_evn         = {} #클릭   복사 컬럼 위치 선택후 붙여넣기
    __click_rand        = {} #랜덤클릭
    __click_xy_wait     = {} #클릭 실행후 대기시간    
    __key0              = {} # 키보드0 단일키 하나
    __key0_wait         = {} # 키보드0 대기
    __key1              = {} # 키보드1 복합키 두개 - hot key 하기
    __key1_wait         = {} # 키보드1 대기

    __csv_data          = [] # 데이터 파일 배열
    __seq_start         = 0        # 시작구간
    __seq_end           = 999      # 종료구간

    __waitTime          = 0.1   # 기본 대기 시간. 각 행동당 기본 대시 시간을 의미함.
    

    __power = False

    def __init__(self ):
        super().__init__()
        self.__power = True     # run 매소드 루프 플래그

    def fn_param(self , title_nm , url_xy,url_xy_wait,url_path,url_path_wait,cvs_path,div,click_xy,click_evn,click_rand,click_xy_wait,key0,key0_wait,key1,key1_wait,csv_data , seq_start , seq_end , rep , file_nm , wait_time):
        self.__title_nm          = title_nm         # 프로그램 제목
        self.__url_xy            = url_xy           # url 클릭 좌표
        self.__url_xy_wait       = url_xy_wait      # 0.5 초 기본 대기 url 클릭후 대기
        self.__url_path          = url_path         # url 주소
        self.__url_path_wait     = url_path_wait    # 2초 기본 대기 url 주소 입력후 대기시간
        self.__cvs_path          = cvs_path         # cvs 파일 위치
        self.__div               = div              # 선택값    
        self.__click_xy          = click_xy         # 클릭    
        self.__click_evn         = click_evn        # 클릭   복사 컬럼 위치 선택후 붙여넣기
        self.__click_rand        = click_rand       # 랜덤클릭
        self.__click_xy_wait     = click_xy_wait    # 클릭 실행후 대기시간    
        self.__key0              = key0             # 키보드0 단일키 하나
        self.__key0_wait         = key0_wait        # 키보드0 대기
        self.__key1              = key1             # 키보드1 복합키 두개 - hot key 하기
        self.__key1_wait         = key1_wait        # 키보드1 대기 
        self.__csv_data          = csv_data         # 데이터 파일
        self.__seq_start         = seq_start        # 시작구간
        self.__seq_end           = seq_end          # 종료구간
        self.__rep               = rep              # 구간반복
        self.__file_nm           = file_nm          # 파일명
        self.__waitTime          = float(wait_time)        # 대기 시간


    def add_time(self , add_second):
        """
        시간을 더하는 함수
        Args:
        add_second: 더할 초
        Returns:
        """
        now     = datetime.now(timezone('Asia/Seoul'))
        hour    = int(now.strftime('%H'))
        minute  = int(now.strftime('%M'))
        second  = int(now.strftime('%S'))    

        total_seconds       = (hour * 3600) + (minute * 60) + second + add_second
        new_hour            = total_seconds // 3600
        remaining_seconds   = total_seconds % 3600
        new_minute          = remaining_seconds // 60
        new_second          = remaining_seconds % 60
        str                 = f'{int(new_hour)}:{int(new_minute)}:{int(new_second)}'
        return str

    def fndbclick(self , xy , wait_time):
        '''더블클릭'''
        pyautogui.doubleClick(x= xy.x  , y= xy.y)        
        time.sleep( wait_time )         

    def fnclick(self , xy , wait_time):
        '''클릭 함수 (좌표 , 대기시간)'''
        pyautogui.click(x= xy.x  , y= xy.y)        
        time.sleep( wait_time ) 
    
    def fnUrl(self, url , wait_time):
        '''url 처리 복사 붙여넣기'''
        pyautogui.hotkey('del')   
        pyperclip.copy( url )
        pyautogui.hotkey('ctrl', 'v')   
        pyautogui.hotkey('enter')         
        time.sleep( (wait_time+1.5) )         
    
    def fnpaste(self , str ):
        '''복사 붙여넣기'''        
        pyperclip.copy( str )
        pyautogui.hotkey('ctrl', 'v')                   
    
    def fnwrite(self, str):
        '''복사 타이핑'''
        for n in str:
            pyautogui.press(n)
    
    def fnkey(self , str , cnt):
        '''키 입력'''
        pyautogui.press( str , presses = cnt , interval=0.2)        

    def fnArrayGet(self , arr , pos):
        '''배열 검색후 리턴'''
        if arr.get(pos) != None:
            ''''''
            return arr.get(pos)
        else :
            return None        
    
    def fnMain(self , step_name : str , i : int , _j  ): 
        '''메인 프로세스
        step_name   : 각 단계의 명령어
        i           : 순서 번호
        _j          : 첨부 데이터
        '''
        xy          = self.fnArrayGet( self.__click_xy      , i )
        evn         = self.fnArrayGet( self.__click_evn     , i )
        rand        = self.fnArrayGet( self.__click_rand    , i )
        xy_wait     = self.fnArrayGet( self.__click_xy_wait , i )
        key0        = self.fnArrayGet( self.__key0          , i )
        key0_wait   = self.fnArrayGet( self.__key0_wait     , i )  #키 입력후 대기 아님 키 입력 횟수 이다.
        key1        = self.fnArrayGet( self.__key1          , i )
        key1_wait   = self.fnArrayGet( self.__key1_wait     , i )
        
        print('\t 행번호 : ', i ,' , 작업구분 : ', step_name , (f", 키부분 : {key0}" if step_name == '방향전환' else "")  )    
        if ( step_name == '클릭') and ( self.__power == True ):
            for j in range(0, int(evn)): #반복 실행한다.
                self.fnclick( xy , self.__waitTime ) #클릭
            time.sleep( float(xy_wait) ) #대기

        elif ( step_name == '붙여넣기') and ( self.__power == True ):
            self.fnclick( xy , self.__waitTime ) #클릭
            n = int(evn)                    
            self.fnpaste( _j[n] ) # 붙여넣기
            time.sleep( float(xy_wait) ) #대기

        elif ( step_name == '글씨쓰기') and ( self.__power == True ):
            self.fnclick( xy , self.__waitTime ) #클릭
            n = int(evn)                    
            self.fnwrite( _j[n] ) #타이핑
            time.sleep( float(xy_wait) ) #대기

        elif ( step_name == '선택하기') and ( self.__power == True ):
            self.fnclick( xy , self.__waitTime ) #클릭
            r = random.randrange(0,3)
            r0 = rand.get(0)
            r1 = rand.get(1)
            r2 = rand.get(2)
            r3 = rand.get(3)
            if r == 0:
                self.fnclick( r0 , self.__waitTime ) #클릭   
            elif r == 1:
                self.fnclick( r1 , self.__waitTime ) #클릭   
            elif r == 2:
                self.fnclick( r2 , self.__waitTime ) #클릭   
            elif r == 3:
                self.fnclick( r3 , self.__waitTime ) #클릭   
            time.sleep( float(xy_wait) ) #대기

        elif ( step_name == '중복선택') and ( self.__power == True ):
            self.fnclick( xy , self.__waitTime ) #클릭   
            r0 = rand.get(0)
            r1 = rand.get(1)
            r2 = rand.get(2)
            r3 = rand.get(3)                                            
            self.fnclick( r0 , self.__waitTime ) #클릭                           
            self.fnclick( r1 , self.__waitTime ) #클릭   
            self.fnclick( r2 , self.__waitTime ) #클릭                           
            self.fnclick( r3 , self.__waitTime ) #클릭   
            time.sleep( float(xy_wait) ) #대기 

        elif ( step_name == '랜덤선택') and ( self.__power == True ):
            self.fnclick( xy , self.__waitTime ) #클릭
            numbers = [0,1,2,3]
            n = random.sample(numbers,4)            
            r0 = rand.get(n[0])
            r1 = rand.get(n[1])
            r2 = rand.get(n[2])
            r3 = rand.get(n[3])
            self.fnclick( r0 , self.__waitTime ) #클릭   
            self.fnclick( r1 , self.__waitTime ) #클릭   
            self.fnclick( r2 , self.__waitTime ) #클릭   
            self.fnclick( r3 , self.__waitTime ) #클릭 
            time.sleep( float(xy_wait) ) #대기
            
        elif ( step_name == '방향전환') and ( self.__power == True ):
            self.fnclick( xy , self.__waitTime ) #클릭                        
            self.fnkey( key0 , int(key0_wait) )                        
            time.sleep( float(xy_wait) ) #대기
            time.sleep( 0.5 )

        elif ( step_name == '무시') and ( self.__power == True ):
            '''행동 없음.'''
        elif ( step_name == '랜덤대기') and ( self.__power == True ):            
            rand_wait_t = round(random.uniform(3,20),1)
            time.sleep( rand_wait_t )

        elif ( step_name == '캡쳐') and ( self.__power == True ):
            '''캡쳐'''
            r11 = rand.get(11)
            r12 = rand.get(12)
            capture_width   = r12.x - r11.x
            capture_height  = r12.y - r11.y

            base_dttm   = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d_%H%M%S')
            base_dt     = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
            try:
                os.mkdir('c:\\ncnc_class\\capture')
            except Exception as e:
                '''폴더 생성 있으면 넘어간다.''' 
            file_nm     = base_dttm+'_'+str(_j[0])
            file_name   = r"c:\\ncnc_class\\capture\\{}{}".format( file_nm ,'.png') 
            pyautogui.screenshot( file_name , region=(r11.x , r11.y , capture_width, capture_height))    
            time.sleep( float(xy_wait) ) #대기   
        
        elif( step_name =='D&D') and ( self.__power == True ) :
            '''드래드 & 드랍'''
            d1 = rand.get(15)
            d2 = rand.get(16)     
            pyautogui.moveTo( d1 )          # 마우스 이동     
            pyautogui.dragTo(   d2.x , d2.y   , duration= 0.3)
            time.sleep( float(xy_wait) )    #대기   
    
    def run(self):
        '''매크로 시작'''
        try:            
            _Msg_Flag   = True # 소요시간 관련 메시지 발송 체크 
            asTime      = time.time() # 시작 시간
            useTime     = 0 # 1회 소요 시간
            totalCnt    = len(self.__csv_data) # 전체 횟수
            totalTime   = 0 # 전체 소요 시간
            predictTime = '' # 예상 종료 시간 
            _second     = ''          
            _minute     = '' 
            _hour       = ''
            for j in self.__csv_data:
                if self.__power == True:
                    if self.__seq_start == 0:
                        '''url 클릭은 시작구간이 0일경우에만 수행.'''
                        self.fnclick(   self.__url_xy   , self.__url_xy_wait    ) #클릭
                        self.fnUrl(     self.__url_path , self.__url_path_wait  ) #url 처리    
                    _j = j            
                    print('*'*100)                                
                    print('처리 데이터 : ', _j)
                    print('*'*100)                            
                    for i in self.__div:     
                        if i in range( self.__seq_start , self.__seq_end ) : #전체 특정 구간반복 기능
                            ''' 설정한 구간 에서만 수행하도록 '''                            
                            if (self.__div.get(i) == '끝') :
                                if _Msg_Flag:
                                    beTime      = time.time()
                                    useTime     = beTime - asTime      # 1회 소요 시간
                                    totalTime   = useTime * totalCnt   # 전체 소요 시간 산출
                                    predictTime = self.add_time( (totalTime-useTime) )        # 예상 종료 시간 산출
                                    _second      = int(totalTime%60)         # 초에서 60으로 나눈 나머지
                                    _minute      = int((totalTime//60)%60)   # 초를 분으로 환산하여 60으로 나눈 나머지
                                    _hour        = int(totalTime//60//60)    # 초를 분으로 환산하고, 그 분을 시간으로 환산한 몫

                                    msg         = f'1회 소요시간 [{round(useTime,2)}초]\n 전체횟수 [{totalCnt}건]\n 전체소요시간 [{_hour}:{_minute}:{_second}]\n 예상시간 [{predictTime}]\n 작업명 [{self.__file_nm}]'
                                    print('소요시간 산출 - 시작','*'*20)
                                    print(beTime , asTime , useTime)
                                    print(msg)
                                    print('소요시간 산출 - 종료','*'*20)
                                    w2ji.send_telegram_message( f'[{self.__title_nm}]\n {msg}\n ===== 시작 =====' , 'macro' )
                                    _Msg_Flag   = False
                                # 끝이닷.
                                break
                            elif ( self.__div.get(i) == '구간반복' ):
                                rep         = self.fnArrayGet( self.__rep           , i )  
                                print('구간반복',rep)                              
                                rep0       = int( rep[0] )
                                rep1       = int( rep[1] ) + 1
                                rep2       = int( rep[2] )
                                print(i,'구간반복 - 시작','='*15)
                                for n in range(0 , rep2 ):                                    
                                    for m in range(rep0 , rep1):                                        
                                        self.fnMain( self.__div.get(m) , m , _j ) 
                                print(i,'구간반복 - 종료','='*15)
                                        
                            elif (self.__div.get(i) in ['클릭','붙여넣기','글씨쓰기','선택하기','중복선택','랜덤선택','방향전환','무시','캡쳐','D&D','랜덤대기'] ) :
                                self.fnMain( self.__div.get(i) , i , _j )                            

        except Exception as e:
            print('*'*50)
            print('정지 합니다. error 발생 : ',e)                                        
            self.__power = False
        
        if self.__power == True: # 완료처리
            w2ji.send_telegram_message( f'[{self.__title_nm}]\n 전체소요시간 [{_hour}:{_minute}:{_second}]\n 예상시간 [{predictTime}]\n 작업명 [{self.__file_nm}]\n ===== 완료 =====' , 'macro' )            
            if self.__title_nm == 'Soldier':
                pyautogui.alert('========== 완료 ==========')

            self.__power = False            
        else :
            print('정지 되었습니다')
        

    def stop(self):
        # 멀티쓰레드를 종료하는 메소드
        print('stop ','*'*50)        
        self.__power = False