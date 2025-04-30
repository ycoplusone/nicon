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
import base64
import openai                       # pip install openai == 0.28.0
from dotenv import load_dotenv      # pip install python-dotenv == 1.0.0 , pip install dotenv 
import lib.Core as core

''' 자동화 클래스
1.0.0 자동화 클랙스 work 와 core 분리.
'''


class WorkArmy(QThread):
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

    __waitTime          = 0.01   # 기본 대기 시간. 각 행동당 기본 대시 시간을 의미함.
    
    __core              = core.Core()
    __power = False
    #### 변수 사용 구분 - 시작
    __mk_datas          = []
    __mk_excels         = []
    __process_len       = []
    __rows              = []
    __t1                = None # schedule_time [ 00:00:00 ]
    __t2                = None # TARGET_TIME [%Y-%m-%d %H:%M:%S] 
    #  , 
    ### 변수 사용 구분 - 종료


    def __init__(self ):
        load_dotenv()   #환경변수 로딩    
        super().__init__()
        self.__power    = True     # run 매소드 루프 플래그
        self.__core     = core.Core()

    def fn_param(self , mk_datas , mk_excels , process_len , rows ):
        ''' 변수 가져오기'''
        self.__mk_datas     = mk_datas
        self.__mk_excels    = mk_excels
        self.__process_len  = process_len
        self.__rows         = rows
        #self.__t1           = t1
        #self.__t2           = t2
      


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

    def fnArrayGet(self , arr , str):
        '''배열 검색후 리턴'''
        if arr.get(str) != None:
            ''''''
            return arr.get(str)
        else :
            return None        
    
    def fnMainTest(self , step_name : str , _i  , _j  ): 
        ''''''
        print('fnMainTest => ',step_name ,' seq : ', _i.get('seq') , ' data : ' , _j )
    
    def fnMain(self , step_name : str , _i  , _j  ): 
        '''메인 프로세스
        step_name   : 각 단계의 명령어
        _i          : 단계 데이터터
        _j          : 첨부 데이터
        '''
        xy          = self.fnArrayGet( _i , 'click_xy'      )
        evn         = self.fnArrayGet( _i , 'click_evn'     )
        rand        = self.fnArrayGet( _i , 'click_rand'    )
        xy_wait     = self.fnArrayGet( _i , 'click_xy_wait' )
        key0        = self.fnArrayGet( _i , 'key0'          )
        key0_wait   = self.fnArrayGet( _i , 'key0_wait'     )  #키 입력후 대기 아님 키 입력 횟수 이다.
        key1        = self.fnArrayGet( _i , 'key1'          )
        key1_wait   = self.fnArrayGet( _i , 'key1_wait'     )
        waitTime    = self.fnArrayGet( _i , 'step_wait_time' ) # 구간 전체 대기 시간.
        waitTime    = float(waitTime)
        
        print('\t 행번호 : ', _i.get('seq') ,' , 작업구분 : ', step_name , (f", 키부분 : {key0}" if step_name == '방향전환' else "")  )    
        if ( step_name == '클릭') and ( self.__power == True ):
            for j in range(0, int(evn)): #반복 실행한다.
                self.__core.fnclick( xy , waitTime ) #클릭
            time.sleep( float(xy_wait) ) #대기

        elif ( step_name == '붙여넣기') and ( self.__power == True ):
            self.__core.fnclick( xy , 0.2 )    #클릭Core
            n   = int(evn)                    
            txt = _j[n]
            self.__core.fnpaste( txt , float(xy_wait) ) # 붙여넣기

        elif ( step_name == '글씨쓰기') and ( self.__power == True ):
            self.__core.fnclick( xy , waitTime ) #클릭
            n   = int(evn)                    
            txt = _j[n]
            self.__core.fnwrite( txt  , float(xy_wait) ) #타이핑

        elif ( step_name == '선택하기') and ( self.__power == True ):
            self.__core.fnclick( xy , waitTime ) #클릭
            self.__core.fnRandClick( rand , waitTime , float(xy_wait)) # 랜덤 클릭

        elif ( step_name == '중복선택') and ( self.__power == True ):
            self.__core.fnclick( xy , waitTime ) #클릭   
            self.__core.fnMultClick( rand , waitTime , float(xy_wait) )# 다중선택

        elif ( step_name == '랜덤선택') and ( self.__power == True ):
            self.__core.fnclick( xy , waitTime ) #클릭
            self.__core.fnMultRandClick( rand , waitTime  , float(xy_wait)) # 다중 랜덤 클릭
        
        elif ( step_name == '지정선택') and ( self.__power == True ):
            self.__core.fnclick( xy , waitTime ) #클릭
            n   = int(evn)      # 엑셀의 가져올 컬럼의 번호를 읽어온다.                    
            txt = _j[n]         # 엑셀의 값의 특정 커럼값을 가져온다.
            appoint = int(txt)  # 값을 정수형으로 변경한다.
            self.__core.fnAppointClick(rand , appoint , waitTime , float(xy_wait) ) # 지정된 좌표 클릭
            
        elif ( step_name == '방향전환') and ( self.__power == True ):
            self.__core.fnclick( xy , waitTime ) #클릭                        
            self.__core.fnkey( key0 , int(key0_wait) , float(xy_wait) ) #키 입력

        elif ( step_name == '무시') and ( self.__power == True ):
            '''행동 없음.'''
        elif ( step_name == '랜덤대기') and ( self.__power == True ):            
            self.__core.fnRandWait() #랜덤 대기 시간

        elif ( step_name == '캡쳐') and ( self.__power == True ):
            '''캡쳐'''
            r11 = rand.get(11)
            r12 = rand.get(12)
            self.__core.fnCapture(r11 , r12 , str(_j[0]) , float(xy_wait)) # 캡쳐
        
        elif( step_name =='D&D') and ( self.__power == True ) :
            '''드래드 & 드랍'''
            self.__core.fnDragNDrop( rand , float(xy_wait) ) # 드래그 앤 드랍
        
        elif( (step_name == '자방[숫자]') or (step_name == '자방[문자]') or (step_name == '자방[혼합]') ) and ( self.__power == True ) :
            '''자동등록방지[숫자] 인식 구간.'''
            self.__core.fnReadCapture( step_name , xy  , str(_j[0]) , rand , float(xy_wait) ) # 캡쳐후 인식한 숫자를 파일에 같이 넣어 이후 신뢰도를 확인한다.
        
        
    
    def run(self):        
        '''매크로 시작'''
        _Msg_Flag   = False # 소요시간 관련 메시지 발송 체크 
        asTime      = time.time() # 시작 시간
        useTime     = 0 # 1회 소요 시간        
        totalTime   = 0 # 전체 소요 시간
        predictTime = '' # 예상 종료 시간 
        total_usetime   = [] # 각 작업별 수행 시간.
        step_usetime    = [] # 개별 소요시간
        _second     = ''          
        _minute     = '' 
        _hour       = ''        
        try:            
            _flag = True
            while _flag:
                for i in range(0 , len(self.__process_len)):
                    if self.__process_len[i] > 0:
                        _row = self.__rows[i]
                        _row_data =  self.__mk_excels[i][_row] # 처리 해야 할 엑셀 값
                        for j in self.__mk_datas[i]:                            
                            #print(j ,' \t ', _row_data)
                            if self.__power == True:
                                if j.get('seq') == 0:
                                    self.__core.fnclick(    j.get('url_xy')     , float(j.get('url_xy_wait'))      )
                                    self.__core.fnUrl(      j.get('url_path')   , float(j.get('url_path_wait'))    )
                                # 아미에서는 구간반복은 수행하지 않는다.
                                if (j.get('div') =='끝'):
                                    self.__process_len[i]   -= 1    # 엑셀 1건 처리 하면 감수 하킨다. 끝을 확인하기 위한 값
                                    self.__rows[i]          += 1    # 행값 증감.   처리해야 할 행위치를 확인하는 값
                                    if self.__rows[i] == 1: # 첫회 수행일때만 작업 시간 산출한다.
                                        ''''''
                                    _Msg_Flag = all(x == 1 for x in self.__rows) # 모두 첫행 처리 하면 발송한다.      
                                    if _Msg_Flag:                                        
                                        
                                        print('소요시간 산출 - 시작','*'*20)
                                        print('소요시간 산출 - 종료','*'*20)
                                        #w2ji.sendTelegramMsg( f'[{self.__title_nm}]\n {msg}\n ===== 시작 =====' )
                                        w2ji.sendTelegramMsg( f'===== 아미 시작 =====' )
                                        _Msg_Flag   = False

                                elif ( j.get('div') in ['클릭','붙여넣기','글씨쓰기','선택하기','중복선택','랜덤선택','지정선택','방향전환','무시','캡쳐','D&D','랜덤대기','자방[숫자]','자방[문자]','자방[혼합]'] ) :
                                    self.fnMain( j.get('div') , j , _row_data )
                                

                if sum( self.__process_len ) <= 0:
                    _flag = False
            
            
        except Exception as e:
            print('*'*50)
            print('정지 합니다. error 발생 : ',e)                                        
            self.__power = False
        

    def stop(self):
        # 멀티쓰레드를 종료하는 메소드
        print('stop ','*'*50)        
        self.__power = False

    def qt_sleep(self, msec):
        loop = QEventLoop()
        QTimer.singleShot(msec, loop.quit)  # 지정 시간 후 loop 종료
        loop.exec_()