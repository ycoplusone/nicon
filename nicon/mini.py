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
import re

import subprocess

'''
스마트폰 & PC 연동.
1.0.0 mini 프로그램 생성
'''
class WorkCmd(QThread):
    ''''''
    __msg   = '' # 메세지
    def InitParam(self,msg):
        '''파라미터 초기화'''
        self.__msg = msg

    def run(self):
        '''실행'''        
        nt = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        print(f'{nt}','='*50)
        print(f'{self.__msg}')
        os.popen( self.__msg )
        nt = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        print(f'{nt}','='*50)

class MyApp(QWidget):    
    __version   = '1.0.0'
    __title_nm  = 'mini'    

    __lb_style  = 'border-radius: 5px;border: 1px solid gray;'
    __lb_style2 = 'border-radius: 5px;border: 1px solid red;'

    __x         = 1024      # ui 시작 좌표

    
    # 전역변수 - begin
    __workcmd       = '' # 쓰레드

    # 전역변수 - end    
    
    # UI - BEGIN
    __ip_qe             = '' # ip 입력 UI
    __conn_btn          = '' # 연결 버튼
    __close_btn         = '' # 닫기 버튼

    __log_ui            = '' # log 창
    # UI - END

    # Init 시작 부분 ##################################################
    def __init__(self):
        super().__init__()
        self.init_param() # 전역변수 초기화
        self.initUI()
        self.setMinimumHeight(100)
        self.setGeometry(self.__x, 100, 500, 80)
        self.show()

    def initUI(self):
        self.pane = QWidget()
        self.view = QScrollArea()
        self.view.setWidget(self.pane)
        self.view.setWidgetResizable(True)
        layout = QVBoxLayout(self)        
        layout.addWidget( self.head0() )
        #layout.addWidget( self.body() )        
        self.setWindowTitle(f'{self.__title_nm} version {self.__version}')

    def init_param(self): # 파라미터 초기화
        ''' 파라미터 초기화 '''
        self.__workcmd = WorkCmd()

    def closeEvent(self, event): # 종료 이벤트 
        ''' 종료'''
        self.DisconnectAdbScrcpy()
    
    # Init 종료 부분    ##################################################

    # Ui 시작 부분      ##################################################
    def head0(self):
        ''' 두번째 줄'''
        groupbox = QGroupBox('Input')
        grid = QGridLayout()
        grid.setSpacing(10)
        start_lb        = QLabel('IP')     
        self.__ip_qe    =  QLineEdit('') #IP입력 
        self.__ip_qe.setStyleSheet( self.__lb_style )      
        
        self.__conn_btn = QPushButton('연결')
        self.__conn_btn.clicked.connect( self.ConnectAdbScrcpy  )

        self.__close_btn = QPushButton('종료')
        self.__close_btn.clicked.connect( self.DisconnectAdbScrcpy  )
        

        grid.addWidget( start_lb         , 0 , 0  )
        grid.addWidget( self.__ip_qe     , 0 , 1  )
        grid.addWidget( self.__conn_btn  , 0 , 2  )
        grid.addWidget( self.__close_btn , 0 , 3  )
        
        groupbox.setLayout(grid)
        
        return groupbox    

    def body(self): # 몸체
        '''몸체부분'''
        groupbox = QGroupBox('Log')
        vbox = QVBoxLayout()
        vbox.setSpacing(0)        
        self.__log_ui = QListWidget()
        vbox.addWidget( self.__log_ui )
        groupbox.setLayout(vbox)
        return groupbox
    
    # Ui 종료 부분 ##################################################



    # 기능 함수 시작 부분 ##################################################
    def append_log(self, message): # 로그 넣기        
        '''
        msg     = f'{message}'
        item    = QListWidgetItem(msg)
        self.__log_ui.addItem(item)   
        self.__log_ui.scrollToBottom() 
        '''

    def ConnectAdbScrcpy(self):
        ''' adb & scrcpy 연결'''
        self.append_log('connect')
        ip = self.__ip_qe.text()
        if ip != '':
            self.__conn_btn.setEnabled(False)
            self.__ip_qe.setEnabled(False)
            command = []
            command.append( f'adb start-server' )      
            command.append( f'adb tcpip 5555' )      
            command.append( f'adb connect {ip}:5555')
            command.append( f'scrcpy --window-x 0 --window-y 30 --window-height 900 -s {ip}:5555')


            for i in command:
                self.__workcmd.InitParam( i )
                self.__workcmd.start()     
                time.sleep(5)                                                       

        else:
            self.append_log('Ip오류')
    
    def DisconnectAdbScrcpy(self):
        ''' adb & scrcpy 종료'''        
        self.append_log('disconnect')
        self.__conn_btn.setEnabled(True)  
        self.__ip_qe.setEnabled(True)      
        command = []
        command.append( f'scrcpy --kill')        
        command.append( f'adb kill-server' )      
        for i in command:
            self.__workcmd.InitParam( i )
            self.__workcmd.start()            
            self.append_log( i )        
        
        




    # 기능 함수 종료 부분 ##################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
