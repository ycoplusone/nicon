import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtTest import *
import pyautogui
import pyperclip
import csv
import pandas as pd
import pickle
import time
import random
from datetime import datetime
from pytz import timezone
from PIL import ImageGrab , Image
import lib.util as w2ji
import re

import mouse        # 20241015 마우스 이벤트 pip install mouse
import keyboard     # 20241015 키보드 이벤트 pip install keyboard




class Work(QThread):
    '''
    1.0.1 연속실행

    '''
    __version   = '1.0.1' # 버전
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

    def fn_param(self , url_xy,url_xy_wait,url_path,url_path_wait,cvs_path,div,click_xy,click_evn,click_rand,click_xy_wait,key0,key0_wait,key1,key1_wait,csv_data , seq_start , seq_end , rep , file_nm):
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


    def add_time(self , add_second):
        """
        시간을 더하는 함수
        Args:
        add_second: 더할 초
        Returns:
        """
        now = datetime.now(timezone('Asia/Seoul'))
        hour    = int(now.strftime('%H'))
        minute  = int(now.strftime('%M'))
        second  = int(now.strftime('%S'))    

        total_seconds = (hour * 3600) + (minute * 60) + second + add_second
        new_hour = total_seconds // 3600
        remaining_seconds = total_seconds % 3600
        new_minute = remaining_seconds // 60
        new_second = remaining_seconds % 60
        str = f'{int(new_hour)}:{int(new_minute)}:{int(new_second)}'
        return str

    def fndbclick(self , xy , wait_time):
        '''더블클릭'''
        #print( xy ,xy.x , xy.y  , wait_time)
        pyautogui.doubleClick(x= xy.x  , y= xy.y)        
        time.sleep( wait_time )         

    def fnclick(self , xy , wait_time):
        '''클릭 함수 (좌표 , 대기시간)'''
        #print( xy ,xy.x , xy.y  , wait_time)
        pyautogui.click(x= xy.x  , y= xy.y)        
        time.sleep( wait_time ) 
    
    def fnUrl(self, url , wait_time):
        '''url 처리 복사 붙여넣기'''
        #print( url , wait_time )
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
        
        print('\t 행번호 : ', i ,' , 작업구분 : ', step_name )    
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
                                    #print('소요시간 산출 - 시작','*'*20)
                                    #print(beTime , asTime , useTime)
                                    #print(msg)
                                    #print('소요시간 산출 - 종료','*'*20)
                                    w2ji.send_telegram_message( f'Version {self.__version}\n {msg}\n 시작되었습니다.' )
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
        
        if self.__power == True:
            w2ji.send_telegram_message( f'Version {self.__version}\n 예상시간 [{predictTime}]\n 작업명 [{self.__file_nm}]\n 완료되었습니다.' )
            #pyautogui.alert('완료 되었습니다.')
            self.__power = False            
        #else :
            #pyautogui.alert('정지 되었습니다.')
        

    def stop(self):
        # 멀티쓰레드를 종료하는 메소드
        print('stop ','*'*50)
        self.__power = False


class MyApp(QWidget):    
    __lb_style  = 'border-radius: 5px;border: 1px solid gray;'
    __lb_style2 = 'border-radius: 5px;border: 1px solid red;'

    __x         = 1024
    __work      = Work()
    __max_obj   = 451

    
    # 전역변수 - begin
    __url_xy            = ()  # url 클릭 좌표
    __url_xy_wait       = 0.5 # 0.5 초 기본 대기 url 클릭후 대기
    __url_path          = ''  # url 주소
    __url_path_wait     = 2   # 2초 기본 대기 url 주소 입력후 대기시간
    __cvs_path          = ''  # cvs 파일 위치
    __div               = {}  # 선택값        
    __click_xy          = {}  # 클릭좌표    
    __click_rand        = {}  # 클릭 랜덤클릭
    __click_xy_wait     = {}  # 클릭 실행후 대기시간    
    __click_evn         = {}  # 클릭   복사 컬럼 위치 선택후 붙여넣기
    __key0              = {}  # 키보드0 단일키 하나
    __key0_wait         = {}  # 키보드0 키입력 횟수이다.
    __key1              = {}  # 키보드1 복합키 두개 - hot key 하기
    __key1_wait         = {}  # 키보드1 대기
    __rep               = {}  # 구간반복 배열

    __seq_start         = 0     # 테스트 시작구간 
    __seq_end           = 9999  # 테스트 종료구간
    __file_nm           = '' # 파일이름
    # 전역변수 - end
    
    '''
    # 임시 시작
    __pos               = -1 # 임시 배열번호 
    __sub_pos           = -1 # 임시 배열번호 랜덤 좌표를 위한   
    __temp_rand         = {} # 랜덤 클릭값 4개 저장해야 한다.
    
    # 임시 종료
    '''
    
    # UI - BEGIN
    __load_cb_ui0        = '' # 로드파일 리스트 ui
    __load_cb_ui1        = '' # 로드파일 리스트 ui
    __load_cb_ui2        = '' # 로드파일 리스트 ui
    __load_cb_ui3        = '' # 로드파일 리스트 ui
    __load_cb_ui4        = '' # 로드파일 리스트 ui
    __load_cb_ui5        = '' # 로드파일 리스트 ui
    __load_cb_ui6        = '' # 로드파일 리스트 ui
    __load_cb_ui7        = '' # 로드파일 리스트 ui
    __load_cb_ui8        = '' # 로드파일 리스트 ui
    __load_cb_ui9        = '' # 로드파일 리스트 ui

    '''
    __url_xy_ui     = '' # url 클릭 좌표
    __url_qe_ui     = '' # url 값
    __csv_lb_ui     = '' # 파일주소 넣기
    __save_file_nm_ui   =  '' # 파일저장명저장 ui
    __qt_div        = {} # 행동구분
    __geo_btn       = {} # 클릭 좌표 설정
    __col           = {} # 클릭후 이벤트
    __geo_xy_wait   = {} # 클릭 의 대기시간
    __ran_btn0      = {} # 좌표0
    __ran_btn1      = {} # 좌표1
    __ran_btn2      = {} # 좌표2
    __ran_btn3      = {} # 좌표3
    __key           = {} # 키보드 키값
    __key_wait      = {} # 키입력후 의 대기시간
    __cap_bnt0      = {} # 캡쳐 begin point
    __cap_bnt1      = {} # 캡쳐 end point
    __rep_st_lb     = {} #구간반복
    __rep_st_qe     = {} #구간반복
    __rep_ed_lb     = {} #구간반복
    __rep_ed_qe     = {} #구간반복
    __rep_cnt_lb    = {} #구간반복
    __rep_cnt_qe    = {} #구간반복                                                   
    __dnd_bnt0      = {} # 드래그 & 드랍
    __dnd_bnt1      = {} # 드래그 & 드랍   
    '''  
    # UI - END

    def init_param(self): # 파라미터 초기화
        ''''''
        # 전역변수 - begin
        self.__url_xy            = ()  # url 클릭 좌표
        self.__url_xy_wait       = 0.5 # 0.5 초 기본 대기 url 클릭후 대기
        self.__url_path          = ''  # url 주소
        self.__url_path_wait     = 2   # 2초 기본 대기 url 주소 입력후 대기시간
        self.__cvs_path          = ''  # cvs 파일 위치
        self.__div               = {}  # 선택값        
        self.__click_xy          = {}  # 클릭좌표    
        self.__click_rand        = {}  # 클릭 랜덤클릭
        self.__click_xy_wait     = {}  # 클릭 실행후 대기시간    
        self.__click_evn         = {}  # 클릭   복사 컬럼 위치 선택후 붙여넣기
        self.__key0              = {}  # 키보드0 단일키 하나
        self.__key0_wait         = {}  # 키보드0 입력 횟수
        self.__key1              = {}  # 키보드1 복합키 두개 - hot key 하기
        self.__key1_wait         = {}  # 키보드1 대기
        self.__rep               = {}  # 구간반복 배열
        self.__seq_start         = 0     # 테스트 시작구간 
        self.__seq_end           = 9999  # 테스트 종료구간

    def keyboard_event(self , evt):
        try:
            if ( evt.name == 'esc' ):   # esc키로 실행 정지 시킨다.
                self.__work.stop()
                pyautogui.alert('정지 되었습니다.')
        except Exception as e:
            print(f'keyboard_event => ')

    def __init__(self):
        super().__init__()
        self.init_param() # 전역변수 초기화
        self.initUI()
        self.setMinimumHeight(330)
        self.setGeometry(self.__x, 100, 380, 330)
        self.show()
        keyboard.hook( self.keyboard_event )    # 키보드 이벤트 훅

    def initUI(self):
        self.pane = QWidget()
        self.view = QScrollArea()
        self.view.setWidget(self.pane)
        self.view.setWidgetResizable(True)
        layout = QVBoxLayout(self)        
        layout.addWidget( self.head0() )
        layout.addWidget(self.view)
        layout = QVBoxLayout(self.pane)        
        layout.addWidget( self.body() )
        self.setWindowTitle('매크로 연속실행')

    def head0(self):
        ''' 두번째 줄'''
        groupbox = QGroupBox('')
        grid = QGridLayout()
        grid.setSpacing(0)

        def fnStart():
            '''매크로 시작 버튼'''
            start_btn.setEnabled(False)
            file_lists = []
            file_lists.append( self.__load_cb_ui0.currentText() )
            file_lists.append( self.__load_cb_ui1.currentText() )
            file_lists.append( self.__load_cb_ui2.currentText() )
            file_lists.append( self.__load_cb_ui3.currentText() )
            file_lists.append( self.__load_cb_ui4.currentText() )
            file_lists.append( self.__load_cb_ui5.currentText() )
            file_lists.append( self.__load_cb_ui6.currentText() )
            file_lists.append( self.__load_cb_ui7.currentText() )
            file_lists.append( self.__load_cb_ui8.currentText() )
            file_lists.append( self.__load_cb_ui9.currentText() )       
            for list in file_lists:
                if list != '':
                    print('*'*50)                    
                    print('시작 파일명 : ',list,'*'*50)                    
                    self.fn_load(list) # 데이터 로드
                    csv_data    = self.readfile( self.__cvs_path )
                    file_name   = list # 파일명
                    self.__work = Work()
                    self.__work.fn_param( 
                        self.__url_xy
                        , self.__url_xy_wait
                        , self.__url_path
                        , self.__url_path_wait
                        , self.__cvs_path
                        , self.__div
                        , self.__click_xy
                        , self.__click_evn
                        , self.__click_rand
                        , self.__click_xy_wait
                        , self.__key0
                        , self.__key0_wait
                        , self.__key1
                        , self.__key1_wait
                        , csv_data
                        , self.__seq_start  # 시작구간
                        , self.__seq_end    # 종료구간
                        , self.__rep        # 구간반복
                        , file_name         # 파일명
                    )
                    self.__work.start()                                     
                    #print('>>>'*10,'대기 시작',time.time())
                    self.__work.wait()
                    print('종료 파일명 : ',list,'*'*50)                    
                    #print('>>>'*10,'대기 종료',time.time())
            
            pyautogui.alert('연속 실행이 완료 되었습니다.')
            print('종료','='*50)
            
       
        def fnStop():
            '''매크로 종료 버튼'''
            print('fnStop','*'*50)
            pyautogui.alert('정지 되었습니다.')
            start_btn.setEnabled(True)            
            self.__work.stop()

        start_btn = QPushButton('Start')
        start_btn.clicked.connect(    fnStart   )  
        grid.addWidget( start_btn , 0 , 0,1,1 )

        stop_btn = QPushButton('Stop')        
        stop_btn.clicked.connect(    fnStop   )  
        grid.addWidget( stop_btn , 0 , 1,1,1 )
        
        groupbox.setFixedHeight(40)
        groupbox.setLayout(grid)
        
        return groupbox    

    def body(self): # 몸체
        '''몸체부분'''
        groupbox = QGroupBox('')
        vbox = QVBoxLayout()
        vbox.setSpacing(0)

        def get_files_sorted_by_mtime():
            directory = "C:\\ncnc_class\\"
            files = os.listdir(directory)
            files = [os.path.join(directory, f) for f in files]

            # 파일 정보 (파일명, 수정 시간)을 튜플로 만들어 리스트에 저장
            file_info = [(f, os.path.getmtime(f)) for f in files]

            # 수정 시간 기준으로 내림차순 정렬 (최신 파일 먼저)
            file_info.sort(key=lambda x: x[1], reverse=True)

            # 파일 목록만 추출
            sorted_files = [ os.path.basename(f[0])  for f in file_info]
            list = []
            for i in sorted_files:
                if i.find( 'pickle' ) != -1 :
                    list.append(i.replace('.pickle',''))
            return list


        file_list = get_files_sorted_by_mtime() #파일 리스트
        self.__load_cb_ui0 = QComboBox()
        self.__load_cb_ui0.addItem('') # 공백파일 
        
        self.__load_cb_ui1 = QComboBox()
        self.__load_cb_ui1.addItem('') # 공백파일 
        
        self.__load_cb_ui2 = QComboBox()
        self.__load_cb_ui2.addItem('') # 공백파일 
        
        self.__load_cb_ui3 = QComboBox()
        self.__load_cb_ui3.addItem('') # 공백파일                         
        
        self.__load_cb_ui4 = QComboBox()
        self.__load_cb_ui4.addItem('') # 공백파일 
        
        self.__load_cb_ui5 = QComboBox()
        self.__load_cb_ui5.addItem('') # 공백파일 
        
        self.__load_cb_ui6 = QComboBox()
        self.__load_cb_ui6.addItem('') # 공백파일 
        
        self.__load_cb_ui7 = QComboBox()
        self.__load_cb_ui7.addItem('') # 공백파일 

        self.__load_cb_ui8 = QComboBox()
        self.__load_cb_ui8.addItem('') # 공백파일 

        self.__load_cb_ui9 = QComboBox()
        self.__load_cb_ui9.addItem('') # 공백파일 

        for i in file_list:
            if i != 'asTEMP': 
                self.__load_cb_ui0.addItem(i)
                self.__load_cb_ui1.addItem(i)
                self.__load_cb_ui2.addItem(i)
                self.__load_cb_ui3.addItem(i)
                self.__load_cb_ui4.addItem(i)
                self.__load_cb_ui5.addItem(i)
                self.__load_cb_ui6.addItem(i)
                self.__load_cb_ui7.addItem(i)
                self.__load_cb_ui8.addItem(i)
                self.__load_cb_ui9.addItem(i)

        vbox.addWidget(self.__load_cb_ui0)
        vbox.addWidget(self.__load_cb_ui1)
        vbox.addWidget(self.__load_cb_ui2)
        vbox.addWidget(self.__load_cb_ui3)
        vbox.addWidget(self.__load_cb_ui4)
        vbox.addWidget(self.__load_cb_ui5)
        vbox.addWidget(self.__load_cb_ui6)
        vbox.addWidget(self.__load_cb_ui7)
        vbox.addWidget(self.__load_cb_ui8)
        vbox.addWidget(self.__load_cb_ui9)

        groupbox.setLayout(vbox)
        return groupbox


# 기능 함수 시작 부분 ##################################################
    def readfile(self , path): #엑셀파일로드
        _rt = []
        df = pd.read_excel(path ,   engine='openpyxl' , dtype=object)
        arr =  df.to_numpy()
        for i in arr :
            aa = []
            for j in i:
                aa.append( str(j) )
            _rt.append( aa )    
        return _rt

    def fn_load( self , file_name ): # 피클 데이터 로드
        self.__file_nm = file_name
        if self.__file_nm == '':
            print('로드할수 없습니다.')
        else :            
            file_path = 'C:\\ncnc_class\\{}{}'.format( self.__file_nm ,'.pickle')                
            _load_data = []
            with open(file_path, 'rb') as f:
                _load_data = pickle.load(f)
            self.__url_xy           = _load_data[0]['url_xy']           # url 클릭 좌표
            self.__url_xy_wait      = _load_data[0]['url_xy_wait']      # 0.5 초 기본 대기 url 클릭후 대기
            self.__url_path         = _load_data[0]['url_path']         # url 클릭 좌표
            self.__url_path_wait    = _load_data[0]['url_path_wait']    # 2초 기본 대기 url 주소 입력후 대기시간
            self.__cvs_path         = _load_data[0]['cvs_path']         # cvs 파일 위치
            self.__div              = _load_data[0]['div']              # 선택값
            self.__click_xy         = _load_data[0]['click_xy']         # 클릭 
            self.__click_evn        = _load_data[0]['click_evn']        # 클릭 복사 컬럼 위치 선택후 붙여넣기
            self.__click_rand       = _load_data[0]['click_rand']       # 랜덤클릭
            self.__click_xy_wait    = _load_data[0]['click_xy_wait']    # 클릭 실행후 대기시간    
            self.__key0             = _load_data[0]['key0']             # 키보드0 단일키 하나
            self.__key0_wait        = _load_data[0]['key0_wait']        # 키보드0 대기
            self.__key1             = _load_data[0]['key1']             # 키보드1 복합키 두개 - hot key 하기
            self.__key1_wait        = _load_data[0]['key1_wait']        # 키보드1 대기                 
            try:
                self.__rep          = _load_data[0]['rep']
            except Exception as e:
                print('rep error',e)                     
            
            # 기존 자료 마이그레이션. 
            for i in self.__div:
                str = self.__div.get(i)
                str = str.replace('클릭-0','클릭').replace('클릭-1','붙여넣기').replace('클릭-2','글씨쓰기').replace('클릭-3','선택하기').replace('클릭-4','중복선택').replace('키보드-0','방향전환')
                self.__div[i] = str   


# 기능 함수 종료 부분 ##################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
