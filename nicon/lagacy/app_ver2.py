from selenium import webdriver
#from seleniumwire import webdriver #  pip install selenium-wire
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import pyperclip #복사
from bs4 import BeautifulSoup
import json
import re
import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtTest import *
from datetime import datetime
from pytz import timezone
import time
import keyboard     # 20241015 키보드 이벤트 pip install keyboard
import lib.dbcon as dbcon 

#from PIL import ImageGrab , Image
#import re

#import subprocess

'''
1.0.0 니콘 내콘 데이터 수집 생성
'''
class WorkCmd(QThread):
    ''''''
    __ps        = '' # 비밀번호
    __data      = '' # 데이터 변경 바인딩
    __driver    = '' # 크롬 드라이버
    def InitParam(self, password , driver ):
        '''파라미터 초기화'''
        self.__ps = password
        self.__driver = driver
        print(self.__ps)

    def run(self):
        '''실행'''        
        nt = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        #self.__data = dbcon.DbConn()            
        
        self.initLogin() # 로그인
        self.getData() # 데이터 처리

        '''
        while True:
            nt = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
            print(f'{nt}','='*50)
            time.sleep(1)
        '''
    ################################ 기능 함수 시작
    def fnClick(self , str):
        time.sleep(0.15)
        WebDriverWait(self.__driver, 5).until(EC.element_to_be_clickable((By.XPATH, str ))).click() 

    def fnCopyNpaste( self , _str ):
        time.sleep(0.2)
        pyperclip.copy( _str )
        ActionChains(self.__driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    ################################ 기능 함수 종료

    def initLogin(self):
        '''
        니콘 내콘 로그인
        '''
        try:
            self.fnClick('//*[@id="app"]/div/div[2]/div/section/section/nav/section/button')
            
            self.fnClick('//*[@id="app"]/div/div[2]/div/div/div/section/div[4]/a/span')

            self.fnClick('/html/body/div[1]/div/div[2]/div/div/div/button[1]/div') #네이버 클릭        
            time.sleep(0.5)
            
            tabs = self.__driver.window_handles
            print(tabs)
            self.__driver.switch_to.window( tabs[1] )        
            print('창 이동', self.__driver.current_window_handle )
            self.fnClick( '/html/body/div[1]/div[2]/div/div[1]/ul/li[2]/a/span/span' ) #일회용 번호 이동
            
            self.fnClick( '/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[2]/input'  ) # 일회용 번호 입력
            self.fnCopyNpaste( self.__ps )

            self.fnClick( '/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[5]/button/span' ) #로그인 클릭
            time.sleep(3)

            self.__driver.switch_to.window( tabs[0] )           
            print('창 이동', self.__driver.current_window_handle )       
            time.sleep(1)
            self.__driver.get('https://ncnc.app/sell/wait-confirmed')  
            time.sleep(1)


        except Exception as e:
            print('initLogin','::',e,'*'*50)

    def getData(self):
        ''' 실제 처리 부분'''
        try :        
            #__lists = self.__data.get_nicon_job_list() # 데이터 스트 가져온다. 사용중이면서 매입보류인 상품 리스트 가져온다.
            #for __list in __lists:
            self.__driver.refresh() #브라이져 새로고침	
            div_nm          = '피' #__list['div_nm']
            category_id     = '56' #__list['category_id']
            category_nm     = '버거킹' #__list['category_nm']
            self.fnDiv01( div_nm ) # 대분류 찾기
            time.sleep(0.5)
            self.fnDiv02( category_nm ) # 중분류 찾기
            time.sleep(0.5)

            print('*'*50)
            print( self.__driver.page_source )
            self.__driver.find(  )
            print('*'*50)


            

   


            




        except Exception as e:
            print('getData','::',e,'*'*50)
            
            
            
            

    def fnDiv01( self , str = '카' ): #str = '카'
        '''대분류 찾기'''
        try:
            self.fnClick( '//*[@id="app"]/div/div[2]/div/section/div/section/section[1]/div/button')    
            _div01 = ''
            if str == '카':
                _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[2]/div'
            elif str == '편':
                _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[3]/div'
            elif str == '빵':
                _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[4]/div'
            elif str == '피':
                _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[5]/div'
            elif str == '문':
                _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[6]/div'
            elif str == '외':
                _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[7]/div'
            elif str == '백':
                _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[8]/div'
            elif str == '휴':
                _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[9]/div'        

            self.fnClick( _div01 )
            time.sleep(0.15)
        except Exception as e:
            print('fnDiv01','::',e,'*'*50)

    def fnDiv02( self ,  _str = '커피빈' ): # _str = '투썸플레이스'
        '''중분류 찾기(카테고리 찾기)'''    
        try:
            self.fnClick( '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/div[2]/input') # 검색바 클릭
            self.fnCopyNpaste( _str )
            self.fnClick( '//*[@id="items-container"]/a[2]') #두번째 아이콘 클릭
            time.sleep(0.15)
        except Exception as e:
            print('fnDiv01','::',e,'*'*50)





class MyApp(QWidget):    
    __version   = '1.0.0'
    __title_nm  = '니콘 내콘 데이터 수집'    

    __lb_style  = 'border-radius: 5px;border: 1px solid gray;'
    __lb_style2 = 'border-radius: 5px;border: 1px solid red;'

    __x         = 1024      # ui 시작 좌표

    
    # 전역변수 - begin
    __workcmd       = '' # 쓰레드
    __driver        = '' # 드라이버 
    __start_flag    = True # 시작 플래그

    # 전역변수 - end    
    
    # UI - BEGIN
    __ps_qe             = '' # 일회성 비밀번호 입력 UI
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
        keyboard.hook( self.keyboard_event )    # 키보드 이벤트 훅

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
        self.__driver = self.initDriver() # 드라이버 초기화
        

    def closeEvent(self, event): # 종료 이벤트 
        ''' 종료'''
        self.CloseApp()

    def keyboard_event(self , evt):
        try:
            if ( evt.name == 'enter' ) & ( self.__start_flag == True ):           # esc키로 실행 정지 시킨다.                
                self.__start_flag = False
                self.StartApp() # 시작
        except Exception as e:
            print(f'keyboard_event => ')        
    
    # Init 종료 부분    ##################################################

    # Ui 시작 부분      ##################################################
    def head0(self):
        ''' 두번째 줄'''
        groupbox = QGroupBox('Input')
        grid = QGridLayout()
        grid.setSpacing(10)
        start_lb        = QLabel('비밀번호')     
        self.__ps_qe    =  QLineEdit('') #IP입력 
        self.__ps_qe.setStyleSheet( self.__lb_style )      
        
        self.__conn_btn = QPushButton('시작')
        self.__conn_btn.clicked.connect( self.StartApp  )

        self.__close_btn = QPushButton('중지')
        self.__close_btn.clicked.connect( self.CloseApp )

        grid.addWidget( start_lb         , 0 , 0  )
        grid.addWidget( self.__ps_qe     , 0 , 1  )
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
    def initDriver(self):
        '''크룸 드라이버 초기화
        로그인 및 드라이버 설정
        '''
        '''
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs']   = {'performance': 'ALL'}        
        caps['loggingPrefs']        = {'performance': 'ALL'}        
        '''
        print('driver init - s')
        options = ChromeOptions() #webdriver.ChromeOptions()
        #options.add_argument('headless')
        options.add_argument('--incognito')
        #options.add_argument('window-size=1024x768')          
        #options.add_argument('window-size=512x384')          

        #driver = webdriver.Chrome( options=options , desired_capabilities=caps) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
        driver = webdriver.Chrome( options=options )    # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
        driver.get('https://ncnc.app/sell/wait-confirmed')
        driver.implicitly_wait(5)  
        driver.set_window_size(1024 , 768)
        time.sleep(0.5)
        print('driver init - e')
        return driver

    def StartApp(self):
        '''시작'''                            
        ps = self.__ps_qe.text()
        self.__ps_qe.setText('') # 값 초기화
        if len(ps) == 0:
            return
        print('시작')
        self.__conn_btn.setEnabled(False)
        self.__workcmd = WorkCmd()
        self.__workcmd.InitParam( ps , self.__driver )
        self.__workcmd.start()        
        
    def CloseApp(self):
        '''중지'''        
        print('중지')        
        self.__start_flag = True
        self.__conn_btn.setEnabled(True)
        self.__workcmd.terminate()
        self.__driver.quit()


    # 기능 함수 종료 부분 ##################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
