import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
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
#import lib.Work as work
import lib.WorkSoldier as work
import re

import mouse        # 20241015 마우스 이벤트 pip install mouse
import keyboard     # 20241015 키보드 이벤트 pip install keyboard


'''
매크로 작업 생성및 단일 수행 프로그램    
    25.0.6 work 클래스 worksoldier 로 변경
    25.0.5 '자방[문자]' , '자방[혼합]' 인식 추가.
    25.0.4 '자방[숫자]' 자동방지숫자 인식 추가.
    25.0.3 fnSave 에 try catch 구문 추가
    25.0.2 시작구간, 종료구간 초기화 오류 수정 , 대기시간 0.01 초기값 설정.
    25.0.1 work 클래스 통합작업
    24.12.4 url 입력 기본대기 시간 2-> 1 , @ 대기시간 2.5 -> 1.5 변경
    24.12.3 기본 대기 시간을 기존 0.5 -> 0.1 변경.
    24.12.2 클릭 후 기본 대기 시간을 변수화 하여 적용 기존 0.5 -> 0.1
    24.12.1 소요시간 산출 개선
    24.11.9 시작시 소요시간 산출.
    24.11.8 new 버튼 선택시 저장파일 이름 초기화 기능 수정.
    24.11.7 로드되는 피클 정렬순서 최신 순으로 변경
    24.11.6 0~5까지 무시 기본, new 버튼 , 로드할 파일 asTEMP 우선.
    24.11.5 임시 파일로 자동 저장.
    24.11.4 저장시 특수문자일경우 오류일경우 방지.
    24.11.3 콤보박스 리스트 길이 늘리기.
    24.11.2 랜덤선택 , 랜덤대기 생성.    
'''



class MyApp(QWidget):
    __version   = '25.0.6'
    __title_nm  = 'Soldier'    

    __lb_style  = 'border-radius: 5px;border: 1px solid gray;'
    __lb_style2 = 'border-radius: 5px;border: 1px solid red;'
    
    __x         = 1024
    __work      = work.WorkSoldier()
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
    __step_wait_time    = '0.01' # 단계별 대기 시간

    __seq_start         = 0     # 테스트 시작구간 
    __seq_end           = 9999  # 테스트 종료구간
    # 전역변수 - end

    # 임시 시작
    __pos               = -1 # 임시 배열번호 
    __sub_pos           = -1 # 임시 배열번호 랜덤 좌표를 위한   
    __temp_rand         = {} # 랜덤 클릭값 4개 저장해야 한다.
    __file_nm           = '' # 파일이름
    # 임시 종료
    
    # UI - BEGIN
    __url_xy_ui     = '' # url 클릭 좌표
    __url_qe_ui     = '' # url 값
    __csv_lb_ui     = '' # 파일주소 넣기
    __save_file_nm_ui   =  '' # 파일저장명저장 ui
    __load_cb_ui        = '' # 로드파일 리스트 ui
    __start_btn     = '' # 시작 버튼

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
    __wait_time_cb  = '' # 대기시간 조정  

    __start_qe      = '' # 전체구간반복 시작
    __end_qe        = '' # 전체구간반복 종료
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
        # 전역변수 - end
        for i in range(0,self.__max_obj): #초기화
            if i in range(0,5):
                self.__div[i]        = '무시'
                self.__click_evn[i]  = '1'
                self.__rep[i]        = {0:'0', 1:'0' , 2:'1'} #구간반복 초기값 설정.            
            else :
                self.__div[i]        = '끝'
                self.__click_evn[i]  = '1'
                self.__rep[i]        = {0:'0', 1:'0' , 2:'1'} #구간반복 초기값 설정.        

    def mouse_event(self , event): #마우스이벤트처리
        '''마우스 이벤트 처리'''
        try:
            xy = pyautogui.position() # 지정 좌표
            if event.button == 'right': #좌표입력중단하기.
                self.__pos      = -1    # 배열초기화
                self.__sub_pos  = -1    # 배열초기화  
            
            if self.__pos == 9999: #url 클릭 좌표
                self.__url_xy = xy
                self.__url_xy_ui.setText('( x : {0} , y : {1} )'.format( self.__url_xy.x , self.__url_xy.y ) )
                self.__pos      = -1 # 배열초기화
                self.__sub_pos  = -1 # 배열초기화 


            if (event.event_type == 'up') and (self.__pos != -1 ) and (self.__sub_pos == -1 ) and (self.__pos != 9999):
                ''''''  
                self.__click_xy[self.__pos] = xy # 클릭좌표
                self.__geo_btn[self.__pos].setText( '(x:{0},y:{1})'.format(self.__click_xy[self.__pos].x , self.__click_xy[self.__pos].y) )       # 좌표 지정.

                self.__pos      = -1 # 배열초기화
                self.__sub_pos  = -1 # 배열초기화            
            elif (event.event_type == 'up') and (self.__pos != -1 ) and (self.__sub_pos != -1 ) and (self.__pos != 9999):
                ''''''
                if self.__click_rand.get(self.__pos) != None:
                    self.__temp_rand =     self.__click_rand[self.__pos]
                
                self.__temp_rand[ self.__sub_pos ] = xy
                self.__click_rand[self.__pos] = self.__temp_rand # 클릭랜덤 좌료
                if self.__sub_pos == 0:
                    self.__ran_btn0[self.__pos].setText( '(x:{0},y:{1})'.format(self.__click_rand[self.__pos][0].x , self.__click_rand[self.__pos][0].y) )      # 좌표0
                elif self.__sub_pos == 1: 
                    self.__ran_btn1[self.__pos].setText( '(x:{0},y:{1})'.format(self.__click_rand[self.__pos][1].x , self.__click_rand[self.__pos][1].y) )      # 좌표1
                elif self.__sub_pos == 2: 
                    self.__ran_btn2[self.__pos].setText( '(x:{0},y:{1})'.format(self.__click_rand[self.__pos][2].x , self.__click_rand[self.__pos][2].y) )      # 좌표2
                elif self.__sub_pos == 3: 
                    self.__ran_btn3[self.__pos].setText( '(x:{0},y:{1})'.format(self.__click_rand[self.__pos][3].x , self.__click_rand[self.__pos][3].y) )      # 좌표3                                
                    self.__pos      = -1    # 배열초기화
                    self.__sub_pos  = -1    # 배열초기화
                
                if self.__sub_pos == 11: 
                    self.__cap_bnt0[self.__pos].setText( '(x:{0},y:{1})'.format(self.__click_rand[self.__pos][11].x , self.__click_rand[self.__pos][11].y) )      # 캡쳐 좌표1
                elif self.__sub_pos == 12: 
                    self.__cap_bnt1[self.__pos].setText( '(x:{0},y:{1})'.format(self.__click_rand[self.__pos][12].x , self.__click_rand[self.__pos][12].y) )      # 캡쳐 좌표2
                    self.__pos      = -1    # 배열초기화
                    self.__sub_pos  = -1    # 배열초기화
                
                if self.__sub_pos == 15:  # 드랍앤 드롭부분
                    self.__dnd_bnt0[self.__pos].setText( '(x:{0},y:{1})'.format(self.__click_rand[self.__pos][15].x , self.__click_rand[self.__pos][15].y) )
                elif self.__sub_pos == 16: 
                    self.__dnd_bnt1[self.__pos].setText( '(x:{0},y:{1})'.format(self.__click_rand[self.__pos][16].x , self.__click_rand[self.__pos][16].y) )
                    self.__pos      = -1    # 배열초기화
                    self.__sub_pos  = -1    # 배열초기화

                if self.__sub_pos != -1: #클릭을 연속으로 지정하기 위해 구문
                    self.__sub_pos += 1
      
        except Exception as e:
            ''''''

    def keyboard_event(self , evt):
        try:
            if ( evt.name == 'esc' ):           # esc키로 실행 정지 시킨다.
                self.__start_btn.setEnabled(True)  
                self.__work.stop()
                self.__work.terminate()         # 강제 종료                
            elif( evt.name == 'z' or evt.name == 'Z' ):
                ''''''
                #self.__work.inputWait = False
                self.__work.fnInputWait2()

        except Exception as e:
            print(f'keyboard_event => ')

    def __init__(self):
        super().__init__()
        self.init_param() # 전역변수 초기화
        self.initUI()
        self.setMinimumHeight(800)
        self.setGeometry(self.__x, 30, 712, 800)
        self.show()
        mouse.hook( self.mouse_event )          # 마우스 이벤트 훅
        keyboard.hook( self.keyboard_event )    # 키보드 이벤트 훅

    def initUI(self):
        self.pane = QWidget()
        self.view = QScrollArea()
        self.view.setWidget(self.pane)
        self.view.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget( self.head() )
        layout.addWidget( self.head2() )
        layout.addWidget( self.repeat() )
        layout.addWidget(self.view)
        layout = QVBoxLayout(self.pane)        
        layout.addWidget( self.body() )
        self.setWindowTitle(f'{self.__title_nm} version {self.__version}')

    def head( self ): # url 등 첫줄
        ''' 첫째줄'''
        groupbox = QGroupBox('')       
        grid = QGridLayout()
        grid.setSpacing(0)

        def fn_geo( ):
            '''좌표할당 행번호 지정'''
            self.__pos = 9999
        
        def fnUrl(): #url 입력 
            self.__url_path = self.__url_qe_ui.text()

        # url 클릭 좌표 - being
        url_lb = QLabel('1. URL')         
        self.__url_xy_ui = QLabel('( x : {0} , y : {1} )'.format( 0 , 0 ) )
        self.__url_xy_ui.setStyleSheet( self.__lb_style  )
        url_xy_btn = QPushButton('좌표지정')
        url_xy_btn.clicked.connect( fn_geo )
        grid.addWidget( url_lb  , 0 , 0)
        grid.addWidget( self.__url_xy_ui  , 0 , 1)        
        # url 클릭 좌표 - end


        # url 입력 - being
        self.__url_qe_ui = QLineEdit()
        self.__url_qe_ui.setStyleSheet( self.__lb_style )
        self.__url_qe_ui.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        self.__url_qe_ui.textChanged.connect( fnUrl )
        grid.addWidget( url_xy_btn  , 0 , 2)  
        grid.addWidget(self.__url_qe_ui  , 0 , 3)        
        # url 입력 - end



        
        # 파일 로드 - begin
        file_lb = QLabel('2. 엑셀')
        self.__csv_lb_ui = QLabel()
        self.__csv_lb_ui.setStyleSheet( self.__lb_style )
        self.__csv_lb_ui.setAlignment(Qt.AlignVCenter|Qt.AlignLeft) 
        def fileopen():
            try:        
                fname = QFileDialog.getOpenFileName()
                _nm = fname[0]            
                self.__cvs_path = _nm
                self.__csv_lb_ui.setText( self.__cvs_path )
            except Exception as e:
                print('def fileopen',e)  
        filebtn = QPushButton('Load')        
        filebtn.clicked.connect( fileopen )  
        if len(self.__cvs_path) != 0:
            self.__csv_lb_ui.setText( self.__cvs_path )
        grid.addWidget(file_lb  , 1 , 0)
        grid.addWidget(self.__csv_lb_ui   , 1 , 1 , 1 , 3)
        grid.addWidget(filebtn  , 1 , 4)     
        # 파일 로드 - end  

        groupbox.setFixedHeight(70)
        groupbox.setLayout( grid )  

        return groupbox

    def head2(self):
        ''' 두번째 줄'''
        groupbox = QGroupBox('')
        grid = QGridLayout()
        grid.setSpacing(0)

        def fnNew():# 초기
            '''            '''
            print('new - s',  self.__click_rand )
            self.init_param() #전역 변수 초기화
            print('new - e',  self.__click_rand )
            self.fnAfterUiLoad('new')

        new_btn  = QPushButton('New')
        new_btn.clicked.connect( fnNew )
        grid.addWidget( new_btn , 0 , 0 ,1,1)


        save_btn = QPushButton('Save')
        save_btn.clicked.connect(    self.fnSave   )  
        grid.addWidget( save_btn , 0 , 1 ,1,1)
   
        def fn_load(): # 피클 데이터 로드
            self.__file_nm = self.__load_cb_ui.currentText()
            if self.__file_nm == '':
                print('로드할수 없습니다.')
            else :
                if  self.__file_nm == 'asTEMP': # asTEMP는 임시 파일명이기때문에 로드 명으로 하지 않느다.
                    self.__save_file_nm_ui.setText( '' ) # 로드한 파일명 저장이름에 등록
                else:    
                    self.__save_file_nm_ui.setText( self.__file_nm.replace('ver3_','') ) # 로드한 파일명 저장이름에 등록                

                self.__load_cb_ui.setCurrentText('') # 로드파일 초기화
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

                try:
                    self.__step_wait_time = _load_data[0]['step_wait_time'] # 전체 단계 대기 시간 저장       
                except Exception as e:
                    print('step_wait_time error',e)
                
                # 기존 자료 마이그레이션. 
                for i in self.__div:
                    str = self.__div.get(i)
                    str = str.replace('클릭-0','클릭').replace('클릭-1','붙여넣기').replace('클릭-2','글씨쓰기').replace('클릭-3','선택하기').replace('클릭-4','중복선택').replace('키보드-0','방향전환')
                    self.__div[i] = str     

                self.fnAfterUiLoad('load') # 피클 파일 로드후 UI 반영
               
               
        load_btn = QPushButton('Load')
        load_btn.clicked.connect( fn_load )
        grid.addWidget( load_btn , 0 , 2 ,1,1 )

         

        def fnStart():
            '''매크로 시작 버튼'''
            self.__start_btn.setEnabled(False)
            csv_data = self.readfile( self.__cvs_path )   
            file_name   = self.__save_file_nm_ui.text() # 파일명                    
            self.__work = work.WorkSoldier() # work.Work()
            self.__work.fn_param( 
                self.__title_nm # 프로그램명칭
                , self.__url_xy
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
                , self.__step_wait_time # 대기 시간 문자열입니다.
            )
            self.__work.start()
            #self.__work.wait()
            #pyautogui.alert('완료 되었습니다')
        
        def fnStop():
            '''매크로 종료 버튼'''
            print('fnStop','*'*50)
            self.__start_btn.setEnabled(True)            
            self.__work.stop()
            self.__work.terminate() # 강제 종료


        self.__start_btn = QPushButton('Start')
        self.__start_btn.clicked.connect(    fnStart   )  
        grid.addWidget( self.__start_btn , 0 , 3,1,1 )

        stop_btn = QPushButton('Stop')        
        stop_btn.clicked.connect(    fnStop   )  
        grid.addWidget( stop_btn , 0 , 4,1,1 )

        save_lb = QLabel('저장파일 : '   )
        grid.addWidget( save_lb , 1 , 0 ,1,1 )
        
        self.__save_file_nm_ui = QLineEdit()     
        self.__save_file_nm_ui.setStyleSheet( self.__lb_style )
        if self.__file_nm != '':
            self.__save_file_nm_ui.setText( self.__file_nm )
        
        grid.addWidget( self.__save_file_nm_ui , 1 , 1,1,2 )

        load_lb = QLabel('     로드파일 : '  )        
        grid.addWidget( load_lb , 1 , 3,1,2 )        

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
        self.__load_cb_ui = QComboBox()
        self.__load_cb_ui.addItem('') # 공백파일 
        self.__load_cb_ui.addItem('asTEMP') # 임시파일이 우선 한다.
        for i in file_list:
            if i != 'asTEMP': 
                self.__load_cb_ui.addItem(i)


        grid.addWidget( self.__load_cb_ui , 1 , 4,1,2 )
        
        groupbox.setFixedHeight(70)
        groupbox.setLayout(grid)
        
        return groupbox    

    def fnAfterUiLoad(self, str): # 로드후 UI 함수
        ''''''
        print('로드후 ui 적용.')
        print('fnAfterUiLoad',str)
        # 로드후 ui 적용.        

        # url 클릭 좌표
        if (str == 'load'):
            if  len(self.__url_xy) > 0: 
                self.__url_xy_ui.setText('( x : {0} , y : {1} )'.format( self.__url_xy.x , self.__url_xy.y ) )
        elif (str == 'new'):
            self.__url_xy_ui.setText('( x : {0} , y : {1} )'.format( 0 , 0 ) )

        
        # url 주소 매핑  
        if str == 'load': 
            if len(self.__url_path) >0 : 
                self.__url_qe_ui.setText( self.__url_path )                        
        elif str == 'new':
            self.__url_qe_ui.setText( '' )
        
        if str == 'load':
            if len(self.__cvs_path) >0 : # 파일 패스
                self.__csv_lb_ui.setText( self.__cvs_path )
        elif str == 'new':
            self.__csv_lb_ui.setText( '' )
        
        if str == 'load':
            self.__wait_time_cb.setCurrentText( self.__step_wait_time )
        elif str == 'new':
            self.__step_wait_time = '0.01'
            self.__wait_time_cb.setCurrentText( self.__step_wait_time )


        if str == 'new':
            self.__save_file_nm_ui.setText('') #저장파일 이름 초기화
            self.__start_qe.setText('0')       # 전체 구간반복 시작 초기화            
            #print(self.__max_obj, type(self.__max_obj) , f'{self.__max_obj}', type(f'{self.__max_obj}'))
            self.__end_qe.setText( f'{self.__max_obj}' )  # 전체 구간반복 종료 초기화
            
        for i in self.__qt_div:
            div_nm = self.__div[i]
            self.__qt_div[i].setCurrentText( div_nm )  # 행동구분
            self.fnDivEvn( i , div_nm ) 

            
            if str == 'load':
                if self.__click_xy.get(i) != None: #기본클릭 좌표 UI
                    self.__geo_btn[i].setText( '(x:{0},y:{1})'.format(self.__click_xy[i].x , self.__click_xy[i].y) )       # 좌표 지정.
            elif str == 'new':
                self.__geo_btn[i].setText( '좌표지정' )       # 좌표 지정.
            
            
            if str == 'load':
                if self.__click_xy_wait.get(i) != None: #기본클릭 후 대기시간
                    self.__geo_xy_wait[i].setText( self.__click_xy_wait[i] )
            elif str == 'new':
                self.__geo_xy_wait[i].setText( '0.1' )
            
            
            if str == 'load':
                if self.__click_evn.get(i) != None:  # 데이터의 컬럼 데이터 매핑
                    self.__col[i].setCurrentText( self.__click_evn[i] )
            elif str == 'new':
                self.__col[i].setCurrentText( '1' )

            
            if str == 'load':
                if (self.__key0.get(i) != None): #키보드 입력
                    self.__key[i].setCurrentText( self.__key0[i] )

                if ( self.__key0_wait.get(i) != None ): # 키보드 대기시간.
                    self.__key_wait[i].setText( self.__key0_wait[i] )                
            elif str == 'new':
                self.__key_wait[i].setText( '1' )
                

            try: #구간반복
                if self.__rep.get(i) != None:                     
                    if str == 'load':
                        if self.__rep[i].get(0) != None:
                            self.__rep_st_qe[i].setText(self.__rep[i][0])
                    elif str == 'new':
                        self.__rep_st_qe[i].setText('0')
                    
                    if str == 'load':
                        if self.__rep[i].get(1) != None:
                            self.__rep_ed_qe[i].setText(self.__rep[i][1])
                    elif str == 'new':
                        self.__rep_ed_qe[i].setText('0')

                    if str == 'load':
                        if self.__rep[i].get(2) != None:
                            self.__rep_cnt_qe[i].setText(self.__rep[i][2])
                    elif str == 'new':
                        self.__rep_cnt_qe[i].setText('1')
            except Exception as e:
                print( 'error self.__rep.get(i) ' )

            if self.__click_rand.get(i) != None: #랜덤과 캡쳐                 
                if str == 'load':
                    if self.__click_rand[i].get(0) != None: #0 번재 값이 있을경우
                        self.__ran_btn0[i].setText( '(x:{0},y:{1})'.format(self.__click_rand[i][0].x , self.__click_rand[i][0].y) )      # 좌표0                                    
                
                    if self.__click_rand[i].get(1) != None: #1 번재 값이 있을경우
                        self.__ran_btn1[i].setText( '(x:{0},y:{1})'.format(self.__click_rand[i][1].x , self.__click_rand[i][1].y) )      # 좌표1
                
                    if self.__click_rand[i].get(2) != None: #2 번재 값이 있을경우
                        self.__ran_btn2[i].setText( '(x:{0},y:{1})'.format(self.__click_rand[i][2].x , self.__click_rand[i][2].y) )      # 좌표2
                
                    if self.__click_rand[i].get(3) != None: #3 번재 값이 있을경우
                        self.__ran_btn3[i].setText( '(x:{0},y:{1})'.format(self.__click_rand[i][3].x , self.__click_rand[i][3].y) )      # 좌표3
                
                    if self.__click_rand[i].get(11) != None: # 캡쳐 1번째
                        self.__cap_bnt0[i].setText( '(x:{0},y:{1})'.format(self.__click_rand[i][11].x , self.__click_rand[i][11].y) )      # 캡쳐 좌표1
                
                    if self.__click_rand[i].get(12) != None: # 캡쳐 2번째
                        self.__cap_bnt1[i].setText( '(x:{0},y:{1})'.format(self.__click_rand[i][12].x , self.__click_rand[i][12].y) )      # 캡쳐 좌표2

                    if self.__click_rand[i].get(15) != None: # 드래그앤 드랍
                        self.__dnd_bnt0[i].setText( '(x:{0},y:{1})'.format(self.__click_rand[i][15].x , self.__click_rand[i][15].y) )                

                    if self.__click_rand[i].get(16) != None: # 드래그앤 드랍
                        self.__dnd_bnt1[i].setText( '(x:{0},y:{1})'.format(self.__click_rand[i][16].x , self.__click_rand[i][16].y) )           
            
            if str == 'new':
                self.__ran_btn0[i].setText( '좌표0' )      # 좌표0
                self.__ran_btn1[i].setText( '좌표1' )      # 좌표1
                self.__ran_btn2[i].setText( '좌표2' )      # 좌표2
                self.__ran_btn3[i].setText( '좌표3' )      # 좌표3             
                self.__cap_bnt0[i].setText( '시작점' )     # 캡쳐 좌표1
                self.__cap_bnt1[i].setText( '끝점' )       # 캡쳐 좌표2
                self.__dnd_bnt0[i].setText( '시작점' )
                self.__dnd_bnt1[i].setText( '끝점' )                          
                
    def repeat(self):
        '''테스트 구간 시작구간 종료구간 설정'''
        groupbox = QGroupBox('')
        grid = QGridLayout()
        grid.setSpacing(0)        

        def repeatEvent():
            '''키이벤트'''
            s = self.__start_qe.text()
            e = self.__end_qe.text()
            if s == '':
                self.__start_qe.setText( '0' )
                self.__seq_start = 0
            else :
                self.__start_qe.setText( str(int(s)) )    
                self.__seq_start = int(s)

            if e == '':
                self.__end_qe.setText( '0' )
                self.__seq_end = 0
            else :
                self.__end_qe.setText( str(int(e)) )                    
                self.__seq_end = int(e)     

        def ChgWaitTime(): # 전체 대기 시간 조정
            ''''''
            str = self.__wait_time_cb.currentText()
            self.__step_wait_time = str
            


        # 시작구간 , 끝구간 지정. - START
        start_lb    = QLabel('시작구간')
        self.__start_qe    = QLineEdit('0')
        self.__start_qe.setFixedWidth(120)  # 가로 크기 지정
        self.__start_qe.setStyleSheet( self.__lb_style )
        self.__start_qe.setValidator(QIntValidator(0,999999,self))    # 100..999사이의 정수        
        self.__start_qe.textChanged.connect( repeatEvent )
        
        end_lb      = QLabel('     종료구간')
        self.__end_qe      = QLineEdit(  str(self.__max_obj)  )
        self.__end_qe.setFixedWidth(120)  # 가로 크기 지정
        self.__end_qe.setStyleSheet( self.__lb_style )
        self.__end_qe.setValidator(QIntValidator(0,999999,self))    # 100..999사이의 정수   
        self.__end_qe.textChanged.connect( repeatEvent )

        wait_lb      = QLabel('     대기시간')
        self.__wait_time_cb = QComboBox()        
        self.__wait_time_cb.addItem( '0.01' )
        for num in range(1,21) :
            f = str(num / 10)
            self.__wait_time_cb.addItem( f )
        self.__wait_time_cb.currentIndexChanged.connect( ChgWaitTime )
                
        grid.addWidget( start_lb    , 0 , 0)
        grid.addWidget( self.__start_qe    , 0 , 1)        
        grid.addWidget( end_lb      , 0 , 2)
        grid.addWidget( self.__end_qe      , 0 , 3)  
        grid.addWidget( wait_lb     , 0 , 4)  
        grid.addWidget( self.__wait_time_cb   , 0 , 5)  
        groupbox.setFixedHeight(40)
        groupbox.setLayout(grid)        
        # 시작구간 , 끝구간 지정. - end
        return groupbox        

    def fnSave(self):
        '''통합 저장'''
        try:
            file_name = self.__save_file_nm_ui.text()        
            file_name = re.sub('[/:*?"<>|]','',file_name)
            file_name = file_name.replace(' ','').replace('ver3_','')   
            if file_name == '':
                QMessageBox.about(self,'About Title','파일이름이 없습니다... ')
            else :
                QMessageBox.about(self,'About Title',f'파일명 {file_name} 저장합니다... ' )
                self.fnSavePickle( file_name )
        except Exception as e:
            QMessageBox.about(self,'About Title','저장 중 이상이 발생하였습니다.')
            

    def fnSavePickle( self , name ):
        '''피클 저장 부분'''
        if name == 'asTEMP':
            file_name = name
        else :
            file_name = 'ver3_'+name
        
        # 항목 추가 함수        
        def add_item( item_t ):
            try:
                # 모든 항목 목록 가져오기
                item_count = self.__load_cb_ui.count()
                items = []
                for i in range(item_count):
                    item = self.__load_cb_ui.itemText(i)
                    items.append(item)                        
                if item_t not in items: #중복이 있으면 추가하지 않는다.
                    self.__load_cb_ui.addItem(item_t)     
            except Exception as e:
                print( '항목 추가 오류',e )

        save_array = []
        save_array.append(
            {
                'url_xy'            : self.__url_xy                 # url 클릭 좌표
                , 'url_xy_wait'     : self.__url_xy_wait            # 0.5 초 기본 대기 url 클릭후 대기
                , 'url_path'        : self.__url_path               # url 클릭 좌표
                , 'url_path_wait'   : self.__url_path_wait          # 2초 기본 대기 url 주소 입력후 대기시간
                , 'cvs_path'        : self.__cvs_path               # cvs 파일 위치
                , 'div'             : self.__div                    # 선택값
                , 'click_xy'        : self.__click_xy               # 클릭 
                , 'click_evn'       : self.__click_evn              # 클릭   복사 컬럼 위치 선택후 붙여넣기
                , 'click_rand'      : self.__click_rand             # 랜덤클릭
                , 'click_xy_wait'   : self.__click_xy_wait          # 클릭 실행후 대기시간    
                , 'key0'            : self.__key0                   # 키보드0 단일키 하나
                , 'key0_wait'       : self.__key0_wait              # 키보드0 대기
                , 'key1'            : self.__key1                   # 키보드1 복합키 두개 - hot key 하기
                , 'key1_wait'       : self.__key1_wait              # 키보드1 대기    
                , 'rep'             : self.__rep                    # 구간반복     
                , 'step_wait_time'  : self.__step_wait_time         # 전체 단계 대기 시간 저장          
            }
        )      
        with open('c:\\ncnc_class\\'+file_name+'.pickle',"wb") as f:
            pickle.dump(save_array, f) # 위에서 생성한 리스트를 list.pickle로 저장              
            #self.__load_cb_ui.addItem(file_name)               
            add_item(file_name)

    def fnDivEvn( self , i , str ): # 행동구분 이벤트
        '''행동구분 이벤트
        i : 행번호 , str : 행동명
        '''
        self.__div[i] = self.__qt_div[i].currentText()
        self.__geo_btn[i].setVisible( False )       # 좌표 지정.
        self.__col[i].setVisible( False )           # 엑셀파일 column 번호
        self.__geo_xy_wait[i].setVisible( False )   # 클릭후 대기 시간
        self.__ran_btn0[i].setVisible( False )      # 좌표0
        self.__ran_btn1[i].setVisible( False )      # 좌표1
        self.__ran_btn2[i].setVisible( False )      # 좌표2
        self.__ran_btn3[i].setVisible( False )      # 좌표3
        self.__key[i].setVisible( False )           # 키보드 입력값
        self.__key_wait[i].setVisible( False )      # 키보드 입력후 대기 시간
        self.__cap_bnt0[i].setVisible( False )      # 캡쳐 시작 포인트
        self.__cap_bnt1[i].setVisible( False )      # 캡쳐 종료 포인트
        self.__rep_st_lb[i].setVisible( False )     # 구간반복
        self.__rep_st_qe[i].setVisible( False )     # 구간반복
        self.__rep_ed_lb[i].setVisible( False )     # 구간반복
        self.__rep_ed_qe[i].setVisible( False )     # 구간반복
        self.__rep_cnt_lb[i].setVisible( False )    # 구간반복
        self.__rep_cnt_qe[i].setVisible( False )    # 구간반복                                                   
        self.__dnd_bnt0[i].setVisible( False )      # 드래그 & 드랍
        self.__dnd_bnt1[i].setVisible( False )      # 드래그 & 드랍     
        if (str == '끝') or (str == '무시')or (str == '랜덤대기')or (str == '입력대기'):                
            ''''''                                             
        elif (str == '클릭') or (str == '붙여넣기') or (str == '글씨쓰기'):
            self.__geo_btn[i].setVisible( True )                
            self.__geo_xy_wait[i].setVisible( True )
            self.__col[i].setVisible(True)
        elif (str == '선택하기') or ( str == '중복선택' ) or ( str == '랜덤선택' ):
            self.__geo_btn[i].setVisible( True )
            self.__geo_xy_wait[i].setVisible( True )                                                
            self.__ran_btn0[i].setVisible( True )
            self.__ran_btn1[i].setVisible( True )
            self.__ran_btn2[i].setVisible( True )
            self.__ran_btn3[i].setVisible( True )                  
        elif str =='지정선택':
            self.__geo_btn[i].setVisible( True )
            self.__geo_xy_wait[i].setVisible( True )                                                
            self.__ran_btn0[i].setVisible( True )
            self.__ran_btn1[i].setVisible( True )
            self.__ran_btn2[i].setVisible( True )
            self.__ran_btn3[i].setVisible( True )   
            self.__col[i].setVisible(True)                           
        elif str =='방향전환':
            self.__geo_btn[i].setVisible( True )
            self.__geo_xy_wait[i].setVisible( True )  
            self.__key[i].setVisible( True )
            self.__key_wait[i].setVisible( True )                  
        elif str == '캡쳐':
            self.__geo_xy_wait[i].setVisible( True )  
            self.__cap_bnt0[i].setVisible( True )
            self.__cap_bnt1[i].setVisible( True )
        elif str == 'D&D' :    
            self.__geo_xy_wait[i].setVisible( True )  
            self.__dnd_bnt0[i].setVisible( True ) # 드래그 & 드랍
            self.__dnd_bnt1[i].setVisible( True ) # 드래그 & 드랍
        elif str == '구간반복':
            self.__rep_st_lb[i].setVisible(  True )  # 구간반복
            self.__rep_st_qe[i].setVisible(  True )  # 구간반복
            self.__rep_ed_lb[i].setVisible(  True )  # 구간반복
            self.__rep_ed_qe[i].setVisible(  True )  # 구간반복
            self.__rep_cnt_lb[i].setVisible( True )  # 구간반복
            self.__rep_cnt_qe[i].setVisible( True )  # 구간반복   
        elif (str == '자방[숫자]') or ( str == '자방[문자]' ) or ( str == '자방[혼합]' ):
            self.__geo_xy_wait[i].setVisible( True )  
            self.__cap_bnt0[i].setVisible( True )
            self.__cap_bnt1[i].setVisible( True )     
            self.__geo_btn[i].setVisible( True )  
        elif str == '브라우저':          
            self.__geo_xy_wait[i].setVisible( True )  
               

    def body(self): # 몸체
        '''몸체부분'''
        groupbox = QGroupBox('')        
        vbox = QVBoxLayout()
        vbox.setSpacing(0)        
        for i in range( 0, self.__max_obj  ): # 0~20까지
            vbox.addWidget(self.exec_obj(i))
        groupbox.setLayout(vbox)
        return groupbox        

    def exec_obj(self , i): # 실제 몸체 부분
        ''' 수행 부분'''             
        groupbox = QGroupBox('')        
        hbox = QHBoxLayout()
        hbox.setSpacing(0)            

        def fnDiv( str ): # 행동구분 이벤트
            '''행동구분 이벤트'''
            self.__div[i] = str
            fnClickEvn()    # __col 컬럼 매핑
            fnkey() # __key0   키보드 입력값   
            fnkeywait() # __key_wait 키보드 입력후 대기시간                  
            fnGeo_xy_wait() # __geo_xy_wait 클릭후 대기 시간 초기값                 
            self.fnDivEvn( i , str ) #메인 호출
            self.fnSavePickle('asTEMP')

        def fnGeo( pos : int , sub_pos : int): # 좌표지정 이벤트
            '''
                ※ 이벤트 처리후 self.__pos의 값이 -1로 변경해서 추가 입력을 막는 로직을 가진다.
                pos : 할당된 행번호
                sub_pos : 부가 순서번호 순서가 없을시 -1을 기본값으로 한다.
            '''
            self.__pos              = pos
            self.__sub_pos          = sub_pos  
            self.__temp_rand        = {} # 랜덤 좌표 초기화
            #print(f'fnGeo => self.__pos : {self.__pos} , self.__sub_pos : {self.__sub_pos}')      

        def fn_rep( str ): # 구간반복 변수저장
            '''구간반복 변수 저장'''
            temp_arr = {}
            if self.__rep.get(i) != None:
                temp_arr =     self.__rep[i]            
            if str =='st':
                temp_arr[0] = self.__rep_st_qe[i].text()
            elif str == 'ed':
                temp_arr[1] = self.__rep_ed_qe[i].text()
            elif str == 'cnt':
                temp_arr[2] = self.__rep_cnt_qe[i].text()
            self.__rep[i] = temp_arr


        def fnClickEvn(): # __click_evn 컬럼 매핑
            self.__click_evn[i]         = self.__col[i].currentText() # 클릭후 컬럼 초기값 설정
            #print( i,' : ',self.__click_evn[i] )            
            
        def fnGeo_xy_wait():#  __geo_xy_wait 클릭후 대기 시간 초기값
            ''''''
            self.__click_xy_wait[i]     = self.__geo_xy_wait[i].text()
            #print( i,' : ',self.__click_xy_wait[i] )            

        def fnkey(): # __key0   키보드 입력값
            ''''''
            self.__key0[i]      = self.__key[i].currentText()
            #print( self.__key0[i] )
        
        def fnkeywait(): # __key_wait 키보드 입력후 대기시간
            ''''''
            self.__key0_wait[i]     = self.__key_wait[i].text()
            #print(self.__key0_wait[i])

        # 행번호 출력 - begin
        row_seq = QLabel( str(i)+' : '   )
        hbox.addWidget( row_seq )
        # 행번호 출력 - end

        # 행동구분 - begin
        combo_style = 'QAbstractItemView {min-height: 220px;}' # 콤보박스 리스트 길이 스타일        
        self.__qt_div[i] = QComboBox()        
        self.__qt_div[i].setStyleSheet(combo_style)
        self.__qt_div[i].addItems(['끝','클릭','붙여넣기','글씨쓰기','선택하기','중복선택','랜덤선택','지정선택','방향전환','무시','캡쳐','구간반복','D&D','랜덤대기','입력대기','자방[숫자]','자방[문자]','자방[혼합]','브라우저' ])
        self.__qt_div[i].setCurrentText( self.__div[i] )  # 행동구분        
        self.__qt_div[i].activated[str].connect( fnDiv )                           
        hbox.addWidget( self.__qt_div[i] )        
        # 행동구분 - end

        # 클릭 좌표 설정 버튼
        self.__geo_btn[i] = QPushButton('좌표지정')
        self.__geo_btn[i].clicked.connect(    lambda : fnGeo( i , -1 )   )
        self.__geo_btn[i].setVisible( False )
        hbox.addWidget( self.__geo_btn[i] )

        # 클릭후 이벤트 ( 클릭-0 : 클릭횟수 , 클릭-1 : 복사붙여넣기 컬럼위치 , 클릭-2 : 타이핑 컬럼위치 , 클릭-3 : 랜덤클릭 , 키보드-1  )
        self.__col[i] = QComboBox()
        self.__col[i].addItems(['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39'])                
        self.__col[i].setCurrentText('1')
        self.__col[i].setVisible( False )
        self.__col[i].currentTextChanged.connect( fnClickEvn )
        self.__col[i].setFixedWidth(70)
        hbox.addWidget( self.__col[i] )     
        
        # 좌표0
        self.__ran_btn0[i] = QPushButton('좌표0')
        self.__ran_btn0[i].clicked.connect(   lambda : fnGeo( i , 0 )   )
        self.__ran_btn0[i].setVisible( False )
        hbox.addWidget( self.__ran_btn0[i] )  

        # 좌표1
        self.__ran_btn1[i] = QPushButton('좌표1')
        self.__ran_btn1[i].clicked.connect(    lambda : fnGeo( i , 1 )   )
        self.__ran_btn1[i].setVisible( False )
        hbox.addWidget( self.__ran_btn1[i] )                  

        # 좌표2
        self.__ran_btn2[i] = QPushButton('좌표2')
        self.__ran_btn2[i].clicked.connect(    lambda : fnGeo( i , 2 )   )
        self.__ran_btn2[i].setVisible( False )
        hbox.addWidget( self.__ran_btn2[i] )                          

        # 좌표3
        self.__ran_btn3[i] = QPushButton('좌표3')
        self.__ran_btn3[i].clicked.connect(    lambda : fnGeo( i , 3 )  )
        self.__ran_btn3[i].setVisible( False )
        hbox.addWidget( self.__ran_btn3[i] )      

        # 키보드 키값 - begin
        self.__key[i] = QComboBox()
        self.__key[i].setStyleSheet(combo_style) 
        self.__key[i].addItems(['pagedown','pageup','up','down','left','right','enter', 'del', 'delete','backspace','space','tab','ctrl+a','ctrl+c','ctrl+v'])        
        self.__key[i].setVisible( False )
        self.__key[i].currentTextChanged.connect( fnkey )
        hbox.addWidget( self.__key[i] )  
        # 키보드 키값 - end

        # 키입력후 의 대기시간 - begin
        self.__key_wait[i] = QLineEdit()     
        self.__key_wait[i].setStyleSheet( self.__lb_style2 )
        self.__key_wait[i].setText('1')      
        self.__key_wait[i].setFixedWidth(50)
        self.__key_wait[i].setVisible( False )
        self.__key_wait[i].textChanged.connect(  fnkeywait )
        hbox.addWidget( self.__key_wait[i] )
        # 키입력후 의 대기시간 - end        

        #캡쳐 - begin
        self.__cap_bnt0[i] = QPushButton('시작점')
        self.__cap_bnt0[i].clicked.connect(   lambda : fnGeo( i , 11 )   )
        self.__cap_bnt0[i].setVisible( False )
        hbox.addWidget( self.__cap_bnt0[i] )          
        self.__cap_bnt1[i] = QPushButton('끝점')
        self.__cap_bnt1[i].clicked.connect(   lambda : fnGeo( i , 12 )   )
        self.__cap_bnt1[i].setVisible( False )
        hbox.addWidget( self.__cap_bnt1[i] )  
        #캡쳐 - end

        #구간반복 - START
        self.__rep_st_lb[i]    = QLabel('시작구간 : ')
        self.__rep_st_lb[i].setVisible(False)
        self.__rep_st_qe[i]    = QLineEdit( '0' )
        self.__rep_st_qe[i].setVisible(False)
        self.__rep_st_qe[i].setStyleSheet( self.__lb_style )
        self.__rep_st_qe[i].setValidator(QIntValidator(0,999,self))    # 0..999사이의 정수        
        self.__rep_st_qe[i].textChanged.connect(  lambda : fn_rep('st') )
        hbox.addWidget( self.__rep_st_lb[i] )
        hbox.addWidget( self.__rep_st_qe[i] )

        self.__rep_ed_lb[i]      = QLabel('종료구간 : ')
        self.__rep_ed_lb[i].setVisible(False)
        self.__rep_ed_qe[i]      = QLineEdit( '0' )
        self.__rep_ed_qe[i].setVisible(False)
        self.__rep_ed_qe[i].setStyleSheet( self.__lb_style )
        self.__rep_ed_qe[i].setValidator(QIntValidator(0,999,self))    # 100..999사이의 정수   
        self.__rep_ed_qe[i].textChanged.connect( lambda : fn_rep('ed') )
            
        hbox.addWidget( self.__rep_ed_lb[i] )
        hbox.addWidget( self.__rep_ed_qe[i] ) 

        self.__rep_cnt_lb[i]      = QLabel('횟수 : ')
        self.__rep_cnt_lb[i].setVisible(False)
        self.__rep_cnt_qe[i]      = QLineEdit( '1' )
        self.__rep_cnt_qe[i].setVisible(False)
        self.__rep_cnt_qe[i].setStyleSheet( self.__lb_style )
        self.__rep_cnt_qe[i].setValidator(QIntValidator(0,999,self))    # 100..999사이의 정수   
        self.__rep_cnt_qe[i].textChanged.connect( lambda : fn_rep('cnt') )
        hbox.addWidget( self.__rep_cnt_lb[i] )
        hbox.addWidget( self.__rep_cnt_qe[i] )
        #구간반복 - END

        # D&D - START
        self.__dnd_bnt0[i] = QPushButton('시작점')
        self.__dnd_bnt0[i].clicked.connect(   lambda : fnGeo( i , 15 )   )
        self.__dnd_bnt0[i].setVisible( False )
        hbox.addWidget( self.__dnd_bnt0[i] )          
        self.__dnd_bnt1[i] = QPushButton('끝점')
        self.__dnd_bnt1[i].clicked.connect(    lambda : fnGeo( i , 16 )   )
        self.__dnd_bnt1[i].setVisible( False )
        hbox.addWidget( self.__dnd_bnt1[i] )  
        # D&D - END

        # 클릭 의 대기시간 - begin
        self.__geo_xy_wait[i] = QLineEdit()     
        self.__geo_xy_wait[i].setStyleSheet( self.__lb_style )
        self.__geo_xy_wait[i].setText('0.1')      
        self.__geo_xy_wait[i].setFixedWidth(50)
        self.__geo_xy_wait[i].setVisible( False )
        self.__geo_xy_wait[i].textChanged.connect( fnGeo_xy_wait )
        hbox.addWidget( self.__geo_xy_wait[i] )
        hbox.addStretch()
        # 클릭 의 대기시간 - end

        hbox.addStretch()
        groupbox.setLayout(hbox)
        return groupbox

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
