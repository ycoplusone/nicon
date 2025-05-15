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
import lib.WorkArmy as work
import re

import mouse        # 20241015 마우스 이벤트 pip install mouse
import keyboard     # 20241015 키보드 이벤트 pip install keyboard

'''
다중 매크로 수행 프로그램
1.1.0 workarmy 와 core 분리 작업.
1.0.2 work 클래스 통합작업
'''

class MyApp(QWidget):    
    __version   = '1.1.0'
    __title_nm  = 'army'    

    __lb_style  = 'border-radius: 5px;border: 1px solid gray;'
    __lb_style2 = 'border-radius: 5px;border: 1px solid red;'
    __cb_style  = 'border-radius: 5px;border: 1px solid red;'

    __x         = 1024
    __work      = work.WorkArmy()
    __max_obj   = 451
        
    __seq_start         = 0     # 테스트 시작구간 
    __seq_end           = 9999  # 테스트 종료구간
    # 전역변수 - end
    
    '''
    # 임시 시작
    
    # 임시 종료
    '''
    
    # UI - BEGIN
    __load_cb_ui         = {} # 다중 로드
    # UI - END

    def init_param(self): # 파라미터 초기화
        ''''''
        # 전역변수 - begin
        self.__seq_start         = 0     # 테스트 시작구간 
        self.__seq_end           = 9999  # 테스트 종료구간
        # 전역변수 - end

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

            macro_data  = [] # 메크로 데이터
            csv_data    = None # 엑셀 데이터 #self.readfile( self.__cvs_path )
            self.__work     = work.WorkArmy()   
            for i in range(0,20):
                txt = self.__load_cb_ui[i].currentText()
                if txt != '':
                    file_lists.append( txt )

            if type.currentText() == '개별':            
                # 엑셀 행 기준으로
                macros , excels = self.manybymany(file_lists)  
                self.__work.fnParamMany(macros , excels)
                self.__work.wait()
                self.__work.start()                
            elif type.currentText() == '일괄':            
                # 작업 단위 기준으로
                macros , excels = self.manybymany(file_lists)  
                self.__work.fn_param(macros , excels)
                self.__work.wait()
                self.__work.start() 
      
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

        type = QComboBox()
        type.setFixedHeight(17)        

        type.addItem('개별') # 공백파일 
        type.addItem('일괄') # 공백파일 
        grid.addWidget( type , 0 , 2,1,1 )

        
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
    def onebyone(self, path):
        ''' 데이터를 하나씩 작업해서 리턴한다. '''
        macro_data  = [] # 메크로 데이터
        csv_data    = [] # 엑셀 데이터 #self.readfile( self.__cvs_path )   
        _data       = self.fnFildLoad( path ) # 메크로 데이터 로드     
        file =  _data[0]['cvs_path']
        csv_data    = self.readfile( file )      
        for i in _data[0]['div']:
            _tmp        = {} # 임시 배열
            _tmp.update({'seq'              : i                                     })  
            _tmp.update({'url_xy'           : _data[0]['url_xy']            })  # url_xy 
            _tmp.update({'url_xy_wait'      : _data[0]['url_xy_wait']       })  # url_xy_wait
            _tmp.update({'url_path'         : _data[0]['url_path']          })  # url_path
            _tmp.update({'url_path_wait'    : _data[0]['url_path_wait']     })  # url_path_wait
            _tmp.update({'step_wait_time'   : _data[0]['step_wait_time']    })  # step_wait_time => wait_time 와 동일하다.
            _tmp.update({'cvs_path'         : _data[0]['cvs_path']          })  # cvs_path
            _tmp.update({'file_name'        : path                          })  # 파일명
            _tmp.update({'program_nm'       : self.__title_nm               })  # 프로그램명
            _tmp.update({'version'          : self.__version                })  # 프로그램 버전                                                
            _tmp.update({'div'              : _data[0]['div'].get(i)                })
            _tmp.update({'click_xy'         : _data[0]['click_xy'].get(i)           })
            _tmp.update({'click_evn'        : _data[0]['click_evn'].get(i)          })
            _tmp.update({'click_rand'       : _data[0]['click_rand'].get(i)         })
            _tmp.update({'click_xy_wait'    : _data[0]['click_xy_wait'].get(i)      })
            _tmp.update({'key0'             : _data[0]['key0'].get(i)               })
            _tmp.update({'key0_wait'        : _data[0]['key0_wait'].get(i)          })
            _tmp.update({'key1'             : _data[0]['key1'].get(i)               })
            _tmp.update({'key1_wait'        : _data[0]['key1_wait'].get(i)          })
            _tmp.update({'rep'              : _data[0]['rep'].get(i)                })
            macro_data.append(_tmp)                    
            if _data[0]['div'].get(i) == '끝':
                break   
        return  macro_data ,  csv_data         

    def manybymany(self , paths):
        ''' 데이터들을 한번에 처리 한다. '''
        macros      = [] # 리턴할 매크로 다차원 데이터 셋
        excels      = [] # 리턴할 엑셀 다차원 데이터 셋
        
        for path in paths:
            if path != '':
                macro_data  = [] # 메크로 데이터
                csv_data    = [] # 엑셀 데이터 #self.readfile( self.__cvs_path )   
                macro_data , csv_data = self.onebyone( path )
                macros.append( macro_data   )
                excels.append( csv_data     )
        return macros , excels

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
    
    def fnFildLoad(self, file_name): # 피클 데이터 로드
        '''# 피클 데이터 로드'''
        if file_name == '':
            print('로드할수 없습니다.')
        else :
            file_path = 'C:\\ncnc_class\\{}{}'.format( file_name ,'.pickle')                
            _load_data = []
            with open(file_path, 'rb') as f:
                _load_data = pickle.load(f)
            return _load_data    


# 기능 함수 종료 부분 ##################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
