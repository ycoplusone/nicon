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
1.0.1 미사용 변수 제거
1.0.0 자동화 클랙스 work 와 core 분리.
'''


class WorkArmy(QThread):    
    __title_nm          = '' #프로그램명칭

    __seq_start         = 0        # 시작구간
    __seq_end           = 9999      # 종료구간

    __core              = core.Core()
    __power = False
    #### 변수 사용 구분 - 시작
    __type              = 'A' # __type {A:한번다 , B:하나씩}

    # type A 일경우 - start
    __mk_datas          = [] # 2차원 매클
    __mk_excels         = [] # 2차원 엑셀
    # type A 일경우 - ENd

    # type b 일경우 - start
    __macros            = [] # 3차원 매클
    __excels            = [] # 3차원 엑셀
    __lenExcel          = [] # 각 엑셀 자료의 전체 행의 크기
    __pointRow          = [] # 처리 해야할 행    
    # type b 일경우 - end
    ### 변수 사용 구분 - 종료


    def __init__(self ):
        load_dotenv()   #환경변수 로딩    
        super().__init__()
        self.__power    = True     # run 매소드 루프 플래그
        self.__core     = core.Core()

    def fn_param(self , mk_datas , mk_excels  ):
        ''' 변수 가져오기'''
        self.__core         = core.Core()
        self.__type         = 'A'
        self.__mk_datas     = mk_datas
        self.__mk_excels    = mk_excels
    
    def fnParamMany(self , macros , excels):
        ''' 3차원 데이터 셋 '''
        self.__core         = core.Core()
        self.__type         = 'B'
        self.__macros       = macros
        self.__excels       = excels
        for i in self.__excels:
            self.__pointRow.append( 0 )
            self.__lenExcel.append( len(i) )        

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
    
    def runTypeA(self):
        ''' 일괄 수행 asis '''
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
                        self.__core.fnclick( xy=url_xy , wait_time=float(url_xy_wait) )  #클릭
                        self.__core.fnUrl(url=url_path , wait_time=float(url_path_wait) ) #url 처리    
                    _j = j            
                    print('*'*100)                                
                    print('처리 데이터 : ', _j)
                    print('*'*100)                            
                    for i in self.__mk_datas:     
                        step_name   = i['div']
                        seq         = i['seq']
                        self.__file_nm      = i['file_name']
                        self.__title_nm     = i['program_nm']

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
                                rep         =  i['rep']
                                print('구간반복',rep)                              
                                rep0       = int( rep[0] )
                                rep1       = int( rep[1] ) + 1
                                rep2       = int( rep[2] )
                                print('구간반복 - 시작','='*15)
                                for n in range(0 , rep2 ):                                    
                                    for m in range(rep0 , rep1):                                        
                                        if (self.__power == True):
                                            self.__core.fnMain( self.__mk_datas[m]['div'] , self.__mk_datas[m] , _j )
                                print('구간반복 - 종료','='*15)
                                        
                            elif (step_name in ['클릭','붙여넣기','글씨쓰기','선택하기','중복선택','랜덤선택','지정선택','방향전환','무시','캡쳐','D&D','랜덤대기','자방[숫자]','자방[문자]','자방[혼합]'] ) :
                                if (self.__power == True):
                                    self.__core.fnMain( step_name , i , _j )                      


        except Exception as e:
            print('*'*50)
            print('정지 합니다. error 발생 : ',e)                                        
            self.__power = False
        
        if self.__power == True: # 완료처리
            w2ji.sendTelegramMsg( f'[{self.__title_nm}]\n 전체소요시간 [{_hour}:{_minute}:{_second}]\n 예상시간 [{predictTime}]\n 작업명 [{self.__file_nm}]\n ===== 완료 ====='  )            
            self.__power = False
        else :
            print('정지 되었습니다')       

    def runTypeB(self): 
        ''' 한번에 하나씩 다차원 수행'''
        try:            
            _Msg_Flag   = True # 소요시간 관련 메시지 발송 체크 
            asTime      = [] #time.time() # 시작 시간
            beTime      = [] 
            useTime     = [] # 1회 소요 시간            
            totalTime   = [] # 전체 소요 시간
            predictTime = [] # 예상 종료 시간 

            _second     = ''          
            _minute     = '' 
            _hour       = ''
            pt          = ''
            
            file_nms      = []
            title_nms     = []
            for i in self.__excels:
                file_nms.append('')
                title_nms.append('')
                asTime.append( time.time() )
                beTime.append( time.time() )
                useTime.append( 0 )
                totalTime.append( 0 )
                predictTime.append( 0 )

            for x in range(0 , max(self.__lenExcel) ):
                for y in range(0 , len(self.__excels)):
                    if (self.__lenExcel[y] > self.__pointRow[y]):
                        now_row   = self.__pointRow[y]
                        _j = self.__excels[y][now_row] # 현재 수행되고 있는 엑셀의 n차원의 row 를 가져온다. 기존의 _J와 동일하다.
                        if self.__power == True:
                            # 수행 시작 부분
                            if self.__pointRow[y] == 0:
                                asTime[y] = time.time() # 시작 시간 설정

                            url_xy          = self.__macros[y][0]['url_xy']
                            url_xy_wait     = self.__macros[y][0]['url_xy_wait']
                            url_path        = self.__macros[y][0]['url_path']
                            url_path_wait   = self.__macros[y][0]['url_path_wait']
                            self.__core.fnclick(    xy=url_xy       , wait_time=float(url_xy_wait) )  #클릭
                            self.__core.fnUrl(      url=url_path    , wait_time=float(url_path_wait) ) #url 처리  
                            print('*'*100)                                
                            print('처리 데이터 : ', _j)
                            print('*'*100)    
                            for i in self.__macros[y]:                                                                                           
                                step_name   = i['div']
                                seq         = i['seq']                                
                                file_nms[y] = i['file_name']
                                title_nms[y]= i['program_nm']
                                if ( step_name == '끝') :                                    
                                    if self.__pointRow[y] == 0:
                                        beTime[y]      = time.time()
                                        useTime[y]     = beTime[y] - asTime[y]      # 1회 소요 시간 시작과 마지막의 시간을 검사
                                        totalTime[y]   = useTime[y] * max( (self.__lenExcel[y]-1) , 1)   # 전체 소요 시간 산출
                                        predictTime[y] = self.add_time( totalTime[y] )        # 예상 종료 시간 산출
                                        if y == (len(self.__pointRow)-1):
                                            pt           = self.add_time( sum(totalTime) )        # 전체 예상 종료 시간
                                            _second      = int(sum(totalTime)%60)         # 초에서 60으로 나눈 나머지
                                            _minute      = int((sum(totalTime)//60)%60)   # 초를 분으로 환산하여 60으로 나눈 나머지
                                            _hour        = int(sum(totalTime)//60//60)    # 초를 분으로 환산하고, 그 분을 시간으로 환산한 몫                                        
                                            msg         = f'1회 소요시간 [{round(sum(useTime),2)}초]\n 전체소요시간 [{_hour}:{_minute}:{_second}]\n 예상시간 [{pt}]'
                                            print('소요시간 산출 - 시작','*'*20)
                                            print(msg)
                                            print('소요시간 산출 - 종료','*'*20)
                                            w2ji.sendTelegramMsg( f'[{file_nms}]\n {msg}\n ===== 시작 =====' )
                                    break
                                elif ( step_name == '구간반복' ):
                                    rep         =  i['rep']
                                    print('구간반복',rep)                              
                                    rep0       = int( rep[0] )
                                    rep1       = int( rep[1] ) + 1
                                    rep2       = int( rep[2] )
                                    print('구간반복 - 시작','='*15)
                                    for n in range(0 , rep2 ):                                    
                                        for m in range(rep0 , rep1):                                        
                                            if (self.__power == True):                                                
                                                self.__core.fnMain( self.__macros[y][m]['div'] , self.__macros[y][m] , _j )
                                    print('구간반복 - 종료','='*15)
                                elif (step_name in ['클릭','붙여넣기','글씨쓰기','선택하기','중복선택','랜덤선택','지정선택','방향전환','무시','캡쳐','D&D','랜덤대기','자방[숫자]','자방[문자]','자방[혼합]'] ) :
                                    if (self.__power == True):
                                        self.__core.fnMain( step_name , i , _j ) 

                        self.__pointRow[y] += 1     # 최종 수행후 행 마감 처리 필수   
                        
            w2ji.sendTelegramMsg( f'[{file_nms}]\n 전체소요시간 [{_hour}:{_minute}:{_second}] ]\n 예상시간 [{pt}] \n ===== 완료 ====='  )            

        except Exception as e:
            print('*'*50)
            print('정지 합니다. error 발생 : ',e)                                        
            self.__power = False
        
        
        if self.__power == True: # 완료처리            
            self.__power = False




    def run(self):
        '''매크로 시작'''
        self.__core = core.Core()
        if self.__type == 'A':
            self.runTypeA()
        elif self.__type =='B':
            self.runTypeB()

        

    def stop(self):
        # 멀티쓰레드를 종료하는 메소드
        print('stop ','*'*50)        
        self.__power = False

