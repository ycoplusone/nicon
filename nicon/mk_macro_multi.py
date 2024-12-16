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
import lib.Work as work
import re

import mouse        # 20241015 마우스 이벤트 pip install mouse
import keyboard     # 20241015 키보드 이벤트 pip install keyboard

'''
다중 매크로 수행 프로그램
1.0.2 work 클래스 통합작업
'''

class MyApp(QWidget):    
    __version   = '1.0.2'
    __title_nm  = 'amry'    

    __lb_style  = 'border-radius: 5px;border: 1px solid gray;'
    __lb_style2 = 'border-radius: 5px;border: 1px solid red;'
    __cb_style  = 'border-radius: 5px;border: 1px solid red;'

    __x         = 1024
    __work      = work.Work()
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
    __step_wait_time    = '0.1' # 단계별 대기 시간

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
    __load_cb_ui         = {} # 다중 로드
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
                self.__work.terminate() # 강제 종료
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
        self.setWindowTitle(f'{self.__title_nm} version {self.__version}')

    def head0(self):
        ''' 두번째 줄'''
        groupbox = QGroupBox('')
        grid = QGridLayout()
        grid.setSpacing(0)

        def fnStart():
            '''매크로 시작 버튼'''
            start_btn.setEnabled(False)
            file_lists = []
            for i in range(0,20):
                file_lists.append( self.__load_cb_ui[i].currentText() )            
            
            for list in file_lists:
                if list != '':
                    print('[',list,']','시작','>'*50)                    
                    self.fn_load(list) # 데이터 로드
                    csv_data    = self.readfile( self.__cvs_path )
                    file_name   = list # 파일명
                    self.__work = work.Work()
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
                    self.__work.wait()
                    print('[',list,']','종료','>'*50)                                    
            
            pyautogui.alert('===== 연속 실행이 완료 되었습니다 =====')
            print('종료','>'*50)
                
            
       
        def fnStop():
            '''매크로 종료 버튼'''
            print('fnStop','*'*50)
            pyautogui.alert('정지 되었습니다.')
            start_btn.setEnabled(True)            
            self.__work.stop()
            self.__work.terminate() # 강제 종료

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
        vbox.setSpacing(10)

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
        for i in range(0,20):
            self.__load_cb_ui[i] = QComboBox()
            self.__load_cb_ui[i].setFixedHeight(25)
            font = self.__load_cb_ui[i].font()
            font.setPointSize(17)
            self.__load_cb_ui[i].setFont(font)
            
            #self.__load_cb_ui[i].setContentsMargins(0, 5, 0, 5) 
            self.__load_cb_ui[i].addItem('') # 공백파일 
            for j in file_list:
                if j != 'asTEMP': 
                    self.__load_cb_ui[i].addItem( j )
            vbox.addWidget(self.__load_cb_ui[i])

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
            
            try:
                self.__step_wait_time = _load_data[0]['step_wait_time'] # 전체 단계 대기 시간 저장       
            except Exception as e:
                self.__step_wait_time = '0.1'
                print('step_wait_time error',e)

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
