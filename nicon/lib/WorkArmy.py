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
    __seq_end           = 9999      # 종료구간

    __waitTime          = 0.01   # 기본 대기 시간. 각 행동당 기본 대시 시간을 의미함.
    
    __core              = core.Core()
    __power = False
    #### 변수 사용 구분 - 시작
    __mk_datas          = []
    __mk_excels         = []
    __t1                = None # schedule_time [ 00:00:00 ]
    __t2                = None # TARGET_TIME [%Y-%m-%d %H:%M:%S] 
    #  , 
    ### 변수 사용 구분 - 종료


    def __init__(self ):
        load_dotenv()   #환경변수 로딩    
        super().__init__()
        self.__power    = True     # run 매소드 루프 플래그
        self.__core     = core.Core()

    def fn_param(self , mk_datas , mk_excels  ):
        ''' 변수 가져오기'''
        self.__core     = core.Core()
        self.__mk_datas     = mk_datas
        self.__mk_excels    = mk_excels

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
        
    
    def run(self):
        '''매크로 시작'''
        self.__core = core.Core()
        try:            
            _Msg_Flag   = True # 소요시간 관련 메시지 발송 체크 
            asTime      = time.time() # 시작 시간
            useTime     = 0 # 1회 소요 시간
            totalCnt    = len(self.__mk_excels) # 전체 횟수
            totalTime   = 0 # 전체 소요 시간
            predictTime = '' # 예상 종료 시간 
            _second     = ''          
            _minute     = '' 
            _hour       = ''
            for j in self.__mk_excels:
                if self.__power == True:
                    if self.__seq_start == 0:
                        '''url 클릭은 시작구간이 0일경우에만 수행.'''
                        url_xy          = self.__mk_datas[0]['url_xy']
                        url_xy_wait     = self.__mk_datas[0]['url_xy_wait']
                        url_path        = self.__mk_datas[0]['url_path']
                        url_path_wait   = self.__mk_datas[0]['url_path_wait']
                        #self.fnclick(   self.__url_xy   , self.__url_xy_wait    ) #클릭
                        self.__core.fnclick( xy=url_xy , wait_time=float(url_xy_wait) )
                        #self.fnUrl(     self.__url_path , self.__url_path_wait  ) #url 처리    
                        self.__core.fnUrl(url=url_path , wait_time=float(url_path_wait) )
                    _j = j            
                    print('*'*100)                                
                    print('처리 데이터 : ', _j)
                    print('*'*100)                            
                    for i in self.__mk_datas:     
                        step_name   = i['div']
                        seq         = i['seq']
                        self.__file_nm     = i['file_name']
                        self.__title_nm  = i['program_nm']
                        #print( step_name  , step_name == '끝')                        
                        if seq in range( self.__seq_start , self.__seq_end ) : #전체 특정 구간반복 기능
                            ''' 설정한 구간 에서만 수행하도록 '''                            
                            if ( step_name == '끝') :
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
                                    w2ji.sendTelegramMsg( f'[{self.__title_nm}]\n {msg}\n ===== 시작 =====' )
                                    _Msg_Flag   = False
                                # 끝이닷.
                                break
                            elif ( step_name == '구간반복' ):
                                rep         =  i['rep'] #self.fnArrayGet( self.__rep           , i )  
                                print('구간반복',rep)                              
                                rep0       = int( rep[0] )
                                rep1       = int( rep[1] ) + 1
                                rep2       = int( rep[2] )
                                print('구간반복 - 시작','='*15)
                                for n in range(0 , rep2 ):                                    
                                    for m in range(rep0 , rep1):                                        
                                        #self.fnMain( self.__div.get(m) , m , _j ) 
                                        if (self.__power == True):
                                            self.__core.fnMain( self.__mk_datas[m]['div'] , self.__mk_datas[m] , _j )
                                print('구간반복 - 종료','='*15)
                                        
                            elif (step_name in ['클릭','붙여넣기','글씨쓰기','선택하기','중복선택','랜덤선택','지정선택','방향전환','무시','캡쳐','D&D','랜덤대기','자방[숫자]','자방[문자]','자방[혼합]'] ) :
                                #self.fnMain( self.__div.get(i) , i , _j )    
                                if (self.__power == True):
                                    self.__core.fnMain( step_name , i , _j )                      


        except Exception as e:
            print('*'*50)
            print('정지 합니다. error 발생 : ',e)                                        
            self.__power = False
        
        if self.__power == True: # 완료처리
            w2ji.sendTelegramMsg( f'[{self.__title_nm}]\n 전체소요시간 [{_hour}:{_minute}:{_second}]\n 예상시간 [{predictTime}]\n 작업명 [{self.__file_nm}]\n ===== 완료 ====='  )            
            if self.__title_nm == 'Soldier':
                pyautogui.alert('========== 완료 ==========')

            self.__power = False            
        else :
            print('정지 되었습니다')
        

    def stop(self):
        # 멀티쓰레드를 종료하는 메소드
        print('stop ','*'*50)        
        self.__power = False

    def qt_sleep(self, msec):
        loop = QEventLoop()
        QTimer.singleShot(msec, loop.quit)  # 지정 시간 후 loop 종료
        loop.exec_()