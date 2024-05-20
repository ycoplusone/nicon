import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import pyautogui
import pyperclip
import csv
import pickle
import time

class Work(QThread):
    __load_data  = []
    __csv_data = []
    __url = ''
    __driver = ''

    def __init__(self ):
        super().__init__()
        self.power = True                           # run 매소드 루프 플래그
    
    def __del__(self):
        self.destroyed()

    
    def fn_param(self , load_data , csv_data , url ):
        self.__load_data = load_data
        self.__csv_data = csv_data
        self.__url = url

    def run(self):
        chrome_options = Options()
        chrome_options.add_argument('window-size=512x1080')        
        chrome_options.add_argument('--incognito')
        self.__driver = webdriver.Chrome( options= chrome_options )    
        time.sleep(2)    
        for j in self.__csv_data:
            if self.power == True:
                self.__driver.get( self.__url )
                time.sleep(2)
                for i in self.__load_data:                    
                    if (i['div'] != 'act0'):                        
                        if i['yn'] == 'Y' :
                            if i['select'] =='클릭':
                                ''''''
                                pyautogui.click(x=int(i['x'])  , y=int(i['y']))
                                pyautogui.leftClick()
                            elif i['select'] =='방향키':
                                cnt = int( i['dir_cnt'] )
                                if i['dir'] =='상':
                                    pyautogui.press('up'   , presses = cnt , interval=0.2)
                                elif i['dir'] =='하':
                                    pyautogui.press('down' , presses = cnt , interval=0.2)
                                elif i['dir'] =='좌':
                                    pyautogui.press('left' , presses = cnt , interval=0.2)
                                elif i['dir'] =='우':
                                    pyautogui.press('right', presses = cnt , interval=0.2)
                            elif i['select'] =='붙여넣기':
                                _str = j[int(i['paste'])]
                                print('_str',_str)
                                pyperclip.copy( _str )
                                pyautogui.hotkey('ctrl', 'v')   

                            time.sleep( float( i['wait'] ) )
                        else :
                            break                              
            else:
                break
        pyautogui.alert('완료 되었습니다.')
        



    def stop(self):
        # 멀티쓰레드를 종료하는 메소드
        self.power = False
        self.__driver.close()
        self.quit()
        self.wait(3000)  # 3초 대기 (바로 안꺼질수도)


class mk_macro( QWidget ):
    ''' 매크로 프로그램'''
    _lb_style = 'border-radius: 5px;border: 1px solid gray;'
    __load_date = [] # 로드 데이터
    __start_stop = 'stop'
    __work = Work()
    
    __gps_info = '' #좌표 변수 선택값. 

    __driver    = '' # 드라이버 변수
    __url       = '' # url 주소
    __file_path = '' # csv 파일 주소

    
    __gps1_x  , __gps1_y  = 0,0
    __gps2_x  , __gps2_y  = 0,0
    __gps3_x  , __gps3_y  = 0,0
    __gps4_x  , __gps4_y  = 0,0
    __gps5_x  , __gps5_y  = 0,0
    __gps6_x  , __gps6_y  = 0,0
    __gps7_x  , __gps7_y  = 0,0
    __gps8_x  , __gps8_y  = 0,0
    __gps9_x  , __gps9_y  = 0,0
    __gps10_x , __gps10_y = 0,0
    __gps11_x , __gps11_y = 0,0
    __gps12_x , __gps12_y = 0,0
    __gps13_x , __gps13_y = 0,0
    __gps14_x , __gps14_y = 0,0
    __gps15_x , __gps15_y = 0,0
    __gps16_x , __gps16_y = 0,0
    __gps17_x , __gps17_y = 0,0
    __gps18_x , __gps18_y = 0,0
    __gps19_x , __gps19_y = 0,0
    __gps20_x , __gps20_y = 0,0

    
     


    
    def __init__(self):
        '''생성자'''        
        super().__init__()
        self.setBr() # 브라우저 생성.
        self.initUI()        
        #pyautogui.mouseInfo()
        
    
    def __del__(self):
        '''소멸자.'''
        self.__driver.close()
        

    def set_start_stop(self,ss):
        self.__start_stop = ss

    def initUI(self):            
            # URL 지정
            self.URL_lb = QLabel('1. URL',self)            
            self.URL_lb.setGeometry(10,10,100,30) # x , y , w , h  

            self.url_qe = QLineEdit(self)
            self.url_qe.setStyleSheet( self._lb_style )
            self.url_qe.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
            self.url_qe.setGeometry(110,10,500,30) # x , y , w , h     
            
            self.url_btn = QPushButton('반영',self)
            self.url_btn.clicked.connect(self.setURL)  
            self.url_btn.setGeometry(610,10,100,30) # x , y , w , h  


            # 1. 파일 로드
            self.file_lb = QLabel('2. CSV',self)
            self.file_lb.setGeometry(10,45,100,30) # x , y , w , h

            #self.file_yn = QComboBox(self)
            #self.file_yn.addItem('N')
            #self.file_yn.addItem('Y')
            #self.file_yn.setGeometry(110,45,40,30) # x , y , w , h
            
            self.file_lb = QLabel('',self)
            self.file_lb.setStyleSheet( self._lb_style )
            self.file_lb.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
            self.file_lb.setGeometry(110,45,400,30) # x , y , w , h
            
            self.filebtn = QPushButton('Load',self)
            self.filebtn.clicked.connect(self.fileopen)  
            self.filebtn.setGeometry(550,45,100,30) # x , y , w , h      

            # ACT1 - 시작
            self.act1_lb = QLabel('3. act1',self)
            self.act1_lb.setGeometry(10,80,100,30) # x , y , w , h
            
            self.act1_yn = QComboBox(self)
            self.act1_yn.addItem('N')
            self.act1_yn.addItem('Y')
            self.act1_yn.setGeometry(110,80,40,30) # x , y , w , h       

            self.act1_select = QComboBox(self)
            self.act1_select.addItem('클릭')
            self.act1_select.addItem('방향키')
            self.act1_select.addItem('붙여넣기')
            self.act1_select.setGeometry(150,80,70,30) # x , y , w , h    
            self.act1_select.activated[str].connect( self.fn_act1_select )

            # 클릭 - 시작
            self.act1_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps1_x , self.__gps1_y ) , self )
            self.act1_gps.setStyleSheet( self._lb_style )
            self.act1_gps.setGeometry( 220,80,350,30 ) # x , y , w , h     
            self.act1_gps.setVisible( True )

            self.act1_gps_btn = QPushButton('좌표지정',self)
            self.act1_gps_btn.clicked.connect(    self.fn_act1_gps   )  
            
            self.act1_gps_btn.setGeometry( 570,80,100,30 ) # x , y , w , h 
            self.act1_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act1_direct = QComboBox(self)
            self.act1_direct.addItem('상')
            self.act1_direct.addItem('하')
            self.act1_direct.addItem('좌')
            self.act1_direct.addItem('우')
            self.act1_direct.setGeometry(220,80,100,30) # x , y , w , h    
            self.act1_direct.setVisible( False )
            
            self.act1_direct_cnt = QLineEdit(self)
            self.act1_direct_cnt.setStyleSheet( self._lb_style )
            self.act1_direct_cnt.setText('1')
            self.act1_direct_cnt.setGeometry(320,80,100,30) # x , y , w , h
            self.act1_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act1_paste = QComboBox(self)
            self.act1_paste.addItem('0')
            self.act1_paste.addItem('1')
            self.act1_paste.addItem('2')
            self.act1_paste.addItem('3')
            self.act1_paste.addItem('4')
            self.act1_paste.addItem('5')
            self.act1_paste.addItem('6')
            self.act1_paste.addItem('7')
            self.act1_paste.addItem('8')
            self.act1_paste.setGeometry(220,80,100,30) # x , y , w , h    
            self.act1_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act1_wait = QLineEdit(self)     
            self.act1_wait.setStyleSheet( self._lb_style )
            self.act1_wait.setText('0.5')
            self.act1_wait.setGeometry(670,80,40,30) # x , y , w , h       
            # ACT1-끝


            # ACT2 - 시작
            self.act2_lb = QLabel('3. act2',self)
            self.act2_lb.setGeometry(10,115,100,30) # x , y , w , h
            
            self.act2_yn = QComboBox(self)
            self.act2_yn.addItem('N')
            self.act2_yn.addItem('Y')
            self.act2_yn.setGeometry(110,115,40,30) # x , y , w , h       

            self.act2_select = QComboBox(self)
            self.act2_select.addItem('클릭')
            self.act2_select.addItem('방향키')
            self.act2_select.addItem('붙여넣기')
            self.act2_select.setGeometry(150,115,70,30) # x , y , w , h    
            self.act2_select.activated[str].connect( self.fn_act2_select )
            
            # 클릭 - 시작
            self.act2_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps2_x , self.__gps2_y ) , self )
            self.act2_gps.setStyleSheet( self._lb_style )
            self.act2_gps.setGeometry( 220,115,350,30 ) # x , y , w , h     
            self.act2_gps.setVisible( True )

            self.act2_gps_btn = QPushButton('좌표지정',self)
            self.act2_gps_btn.clicked.connect(    self.fn_act2_gps   )  
            
            self.act2_gps_btn.setGeometry( 570,115,100,30 ) # x , y , w , h 
            self.act2_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act2_direct = QComboBox(self)
            self.act2_direct.addItem('상')
            self.act2_direct.addItem('하')
            self.act2_direct.addItem('좌')
            self.act2_direct.addItem('우')
            self.act2_direct.setGeometry(220,115,100,30) # x , y , w , h    
            self.act2_direct.setVisible( False )
            
            self.act2_direct_cnt = QLineEdit(self)
            self.act2_direct_cnt.setStyleSheet( self._lb_style )
            self.act2_direct_cnt.setText('1')
            self.act2_direct_cnt.setGeometry(320,115,100,30) # x , y , w , h
            self.act2_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act2_paste = QComboBox(self)
            self.act2_paste.addItem('0')
            self.act2_paste.addItem('1')
            self.act2_paste.addItem('2')
            self.act2_paste.addItem('3')
            self.act2_paste.addItem('4')
            self.act2_paste.addItem('5')
            self.act2_paste.addItem('6')
            self.act2_paste.addItem('7')
            self.act2_paste.addItem('8')
            self.act2_paste.setGeometry(220,115,100,30) # x , y , w , h    
            self.act2_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act2_wait = QLineEdit(self)     
            self.act2_wait.setStyleSheet( self._lb_style )
            self.act2_wait.setText('0.5')
            self.act2_wait.setGeometry(670,115,40,30) # x , y , w , h       
            # ACT2-끝

            # ACT3 - 시작
            self.act3_lb = QLabel('3. act3',self)
            self.act3_lb.setGeometry(10, 150 ,100,30) # x , y , w , h
            
            self.act3_yn = QComboBox(self)
            self.act3_yn.addItem('N')
            self.act3_yn.addItem('Y')
            self.act3_yn.setGeometry(110, 150 ,40,30) # x , y , w , h       

            self.act3_select = QComboBox(self)
            self.act3_select.addItem('클릭')
            self.act3_select.addItem('방향키')
            self.act3_select.addItem('붙여넣기')
            self.act3_select.setGeometry(150, 150 ,70,30) # x , y , w , h    
            self.act3_select.activated[str].connect( self.fn_act3_select )
            
            # 클릭 - 시작
            self.act3_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps3_x , self.__gps3_y ) , self )
            self.act3_gps.setStyleSheet( self._lb_style )
            self.act3_gps.setGeometry( 220, 150 ,350,30 ) # x , y , w , h     
            self.act3_gps.setVisible( True )

            self.act3_gps_btn = QPushButton('좌표지정',self)
            self.act3_gps_btn.clicked.connect(    self.fn_act3_gps   )  
            
            self.act3_gps_btn.setGeometry( 570, 150 ,100,30 ) # x , y , w , h 
            self.act3_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act3_direct = QComboBox(self)
            self.act3_direct.addItem('상')
            self.act3_direct.addItem('하')
            self.act3_direct.addItem('좌')
            self.act3_direct.addItem('우')
            self.act3_direct.setGeometry(220, 150 ,100,30) # x , y , w , h    
            self.act3_direct.setVisible( False )
            
            self.act3_direct_cnt = QLineEdit(self)
            self.act3_direct_cnt.setStyleSheet( self._lb_style )
            self.act3_direct_cnt.setText('1')
            self.act3_direct_cnt.setGeometry(320, 150 ,100,30) # x , y , w , h
            self.act3_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act3_paste = QComboBox(self)
            self.act3_paste.addItem('0')
            self.act3_paste.addItem('1')
            self.act3_paste.addItem('2')
            self.act3_paste.addItem('3')
            self.act3_paste.addItem('4')
            self.act3_paste.addItem('5')
            self.act3_paste.addItem('6')
            self.act3_paste.addItem('7')
            self.act3_paste.addItem('8')
            self.act3_paste.setGeometry(220, 150 ,100,30) # x , y , w , h    
            self.act3_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act3_wait = QLineEdit(self)     
            self.act3_wait.setStyleSheet( self._lb_style )
            self.act3_wait.setText('0.5')
            self.act3_wait.setGeometry(670, 150 ,40,30) # x , y , w , h       
            # ACT3-끝

            # act4 - 시작
            self.act4_lb = QLabel('3. act4',self)
            self.act4_lb.setGeometry(10, 185 ,100,30) # x , y , w , h
            
            self.act4_yn = QComboBox(self)
            self.act4_yn.addItem('N')
            self.act4_yn.addItem('Y')
            self.act4_yn.setGeometry(110, 185 ,40,30) # x , y , w , h       

            self.act4_select = QComboBox(self)
            self.act4_select.addItem('클릭')
            self.act4_select.addItem('방향키')
            self.act4_select.addItem('붙여넣기')
            self.act4_select.setGeometry(150, 185 ,70,30) # x , y , w , h    
            self.act4_select.activated[str].connect( self.fn_act4_select )
            
            # 클릭 - 시작
            self.act4_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps4_x , self.__gps4_y ) , self )
            self.act4_gps.setStyleSheet( self._lb_style )
            self.act4_gps.setGeometry( 220, 185 ,350,30 ) # x , y , w , h     
            self.act4_gps.setVisible( True )

            self.act4_gps_btn = QPushButton('좌표지정',self)
            self.act4_gps_btn.clicked.connect(    self.fn_act4_gps   )  
            
            self.act4_gps_btn.setGeometry( 570, 185 ,100,30 ) # x , y , w , h 
            self.act4_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act4_direct = QComboBox(self)
            self.act4_direct.addItem('상')
            self.act4_direct.addItem('하')
            self.act4_direct.addItem('좌')
            self.act4_direct.addItem('우')
            self.act4_direct.setGeometry(220, 185 ,100,30) # x , y , w , h    
            self.act4_direct.setVisible( False )
            
            self.act4_direct_cnt = QLineEdit(self)
            self.act4_direct_cnt.setStyleSheet( self._lb_style )
            self.act4_direct_cnt.setText('1')
            self.act4_direct_cnt.setGeometry(320, 185 ,100,30) # x , y , w , h
            self.act4_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act4_paste = QComboBox(self)
            self.act4_paste.addItem('0')
            self.act4_paste.addItem('1')
            self.act4_paste.addItem('2')
            self.act4_paste.addItem('3')
            self.act4_paste.addItem('4')
            self.act4_paste.addItem('5')
            self.act4_paste.addItem('6')
            self.act4_paste.addItem('7')
            self.act4_paste.addItem('8')
            self.act4_paste.setGeometry(220, 185 ,100,30) # x , y , w , h    
            self.act4_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act4_wait = QLineEdit(self)     
            self.act4_wait.setStyleSheet( self._lb_style )
            self.act4_wait.setText('0.5')
            self.act4_wait.setGeometry(670, 185 ,40,30) # x , y , w , h       
            # act4-끝

            # act5 - 시작
            self.act5_lb = QLabel('3. act5',self)
            self.act5_lb.setGeometry(10, 220 ,100,30) # x , y , w , h
            
            self.act5_yn = QComboBox(self)
            self.act5_yn.addItem('N')
            self.act5_yn.addItem('Y')
            self.act5_yn.setGeometry(110, 220 ,40,30) # x , y , w , h       

            self.act5_select = QComboBox(self)
            self.act5_select.addItem('클릭')
            self.act5_select.addItem('방향키')
            self.act5_select.addItem('붙여넣기')
            self.act5_select.setGeometry(150, 220 ,70,30) # x , y , w , h    
            self.act5_select.activated[str].connect( self.fn_act5_select )
            
            # 클릭 - 시작
            self.act5_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps5_x , self.__gps5_y ) , self )
            self.act5_gps.setStyleSheet( self._lb_style )
            self.act5_gps.setGeometry( 220, 220 ,350,30 ) # x , y , w , h     
            self.act5_gps.setVisible( True )

            self.act5_gps_btn = QPushButton('좌표지정',self)
            self.act5_gps_btn.clicked.connect(    self.fn_act5_gps   )  
            
            self.act5_gps_btn.setGeometry( 570, 220 ,100,30 ) # x , y , w , h 
            self.act5_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act5_direct = QComboBox(self)
            self.act5_direct.addItem('상')
            self.act5_direct.addItem('하')
            self.act5_direct.addItem('좌')
            self.act5_direct.addItem('우')
            self.act5_direct.setGeometry(220, 220 ,100,30) # x , y , w , h    
            self.act5_direct.setVisible( False )
            
            self.act5_direct_cnt = QLineEdit(self)
            self.act5_direct_cnt.setStyleSheet( self._lb_style )
            self.act5_direct_cnt.setText('1')
            self.act5_direct_cnt.setGeometry(320, 220 ,100,30) # x , y , w , h
            self.act5_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act5_paste = QComboBox(self)
            self.act5_paste.addItem('0')
            self.act5_paste.addItem('1')
            self.act5_paste.addItem('2')
            self.act5_paste.addItem('3')
            self.act5_paste.addItem('4')
            self.act5_paste.addItem('5')
            self.act5_paste.addItem('6')
            self.act5_paste.addItem('7')
            self.act5_paste.addItem('8')
            self.act5_paste.setGeometry(220, 220 ,100,30) # x , y , w , h    
            self.act5_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act5_wait = QLineEdit(self)     
            self.act5_wait.setStyleSheet( self._lb_style )
            self.act5_wait.setText('0.5')
            self.act5_wait.setGeometry(670, 220 ,40,30) # x , y , w , h       
            # act5-끝

            # act6 - 시작
            self.act6_lb = QLabel('3. act6',self)
            self.act6_lb.setGeometry(10, 255 ,100,30) # x , y , w , h
            
            self.act6_yn = QComboBox(self)
            self.act6_yn.addItem('N')
            self.act6_yn.addItem('Y')
            self.act6_yn.setGeometry(110, 255 ,40,30) # x , y , w , h       

            self.act6_select = QComboBox(self)
            self.act6_select.addItem('클릭')
            self.act6_select.addItem('방향키')
            self.act6_select.addItem('붙여넣기')
            self.act6_select.setGeometry(150, 255 ,70,30) # x , y , w , h    
            self.act6_select.activated[str].connect( self.fn_act6_select )
            
            # 클릭 - 시작
            self.act6_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps6_x , self.__gps6_y ) , self )
            self.act6_gps.setStyleSheet( self._lb_style )
            self.act6_gps.setGeometry( 220, 255 ,350,30 ) # x , y , w , h     
            self.act6_gps.setVisible( True )

            self.act6_gps_btn = QPushButton('좌표지정',self)
            self.act6_gps_btn.clicked.connect(    self.fn_act6_gps   )  
            
            self.act6_gps_btn.setGeometry( 570, 255 ,100,30 ) # x , y , w , h 
            self.act6_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act6_direct = QComboBox(self)
            self.act6_direct.addItem('상')
            self.act6_direct.addItem('하')
            self.act6_direct.addItem('좌')
            self.act6_direct.addItem('우')
            self.act6_direct.setGeometry(220, 255 ,100,30) # x , y , w , h    
            self.act6_direct.setVisible( False )
            
            self.act6_direct_cnt = QLineEdit(self)
            self.act6_direct_cnt.setStyleSheet( self._lb_style )
            self.act6_direct_cnt.setText('1')
            self.act6_direct_cnt.setGeometry(320, 255 ,100,30) # x , y , w , h
            self.act6_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act6_paste = QComboBox(self)
            self.act6_paste.addItem('0')
            self.act6_paste.addItem('1')
            self.act6_paste.addItem('2')
            self.act6_paste.addItem('3')
            self.act6_paste.addItem('4')
            self.act6_paste.addItem('5')
            self.act6_paste.addItem('6')
            self.act6_paste.addItem('7')
            self.act6_paste.addItem('8')
            self.act6_paste.setGeometry(220, 255 ,100,30) # x , y , w , h    
            self.act6_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act6_wait = QLineEdit(self)     
            self.act6_wait.setStyleSheet( self._lb_style )
            self.act6_wait.setText('0.5')
            self.act6_wait.setGeometry(670, 255 ,40,30) # x , y , w , h       
            # act6-끝

            # act7 - 시작
            self.act7_lb = QLabel('3. act7',self)
            self.act7_lb.setGeometry(10, 290 ,100,30) # x , y , w , h
            
            self.act7_yn = QComboBox(self)
            self.act7_yn.addItem('N')
            self.act7_yn.addItem('Y')
            self.act7_yn.setGeometry(110, 290 ,40,30) # x , y , w , h       

            self.act7_select = QComboBox(self)
            self.act7_select.addItem('클릭')
            self.act7_select.addItem('방향키')
            self.act7_select.addItem('붙여넣기')
            self.act7_select.setGeometry(150, 290 ,70,30) # x , y , w , h    
            self.act7_select.activated[str].connect( self.fn_act7_select )
            
            # 클릭 - 시작
            self.act7_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps7_x , self.__gps7_y ) , self )
            self.act7_gps.setStyleSheet( self._lb_style )
            self.act7_gps.setGeometry( 220, 290 ,350,30 ) # x , y , w , h     
            self.act7_gps.setVisible( True )

            self.act7_gps_btn = QPushButton('좌표지정',self)
            self.act7_gps_btn.clicked.connect(    self.fn_act7_gps   )  
            
            self.act7_gps_btn.setGeometry( 570, 290 ,100,30 ) # x , y , w , h 
            self.act7_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act7_direct = QComboBox(self)
            self.act7_direct.addItem('상')
            self.act7_direct.addItem('하')
            self.act7_direct.addItem('좌')
            self.act7_direct.addItem('우')
            self.act7_direct.setGeometry(220, 290 ,100,30) # x , y , w , h    
            self.act7_direct.setVisible( False )
            
            self.act7_direct_cnt = QLineEdit(self)
            self.act7_direct_cnt.setStyleSheet( self._lb_style )
            self.act7_direct_cnt.setText('1')
            self.act7_direct_cnt.setGeometry(320, 290 ,100,30) # x , y , w , h
            self.act7_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act7_paste = QComboBox(self)
            self.act7_paste.addItem('0')
            self.act7_paste.addItem('1')
            self.act7_paste.addItem('2')
            self.act7_paste.addItem('3')
            self.act7_paste.addItem('4')
            self.act7_paste.addItem('5')
            self.act7_paste.addItem('6')
            self.act7_paste.addItem('7')
            self.act7_paste.addItem('8')
            self.act7_paste.setGeometry(220, 290 ,100,30) # x , y , w , h    
            self.act7_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act7_wait = QLineEdit(self)     
            self.act7_wait.setStyleSheet( self._lb_style )
            self.act7_wait.setText('0.5')
            self.act7_wait.setGeometry(670, 290 ,40,30) # x , y , w , h       
            # act7-끝       

            # act8 - 시작
            self.act8_lb = QLabel('3. act8',self)
            self.act8_lb.setGeometry(10, 325 ,100,30) # x , y , w , h
            
            self.act8_yn = QComboBox(self)
            self.act8_yn.addItem('N')
            self.act8_yn.addItem('Y')
            self.act8_yn.setGeometry(110, 325 ,40,30) # x , y , w , h       

            self.act8_select = QComboBox(self)
            self.act8_select.addItem('클릭')
            self.act8_select.addItem('방향키')
            self.act8_select.addItem('붙여넣기')
            self.act8_select.setGeometry(150, 325 ,70,30) # x , y , w , h    
            self.act8_select.activated[str].connect( self.fn_act8_select )
            
            # 클릭 - 시작
            self.act8_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps8_x , self.__gps8_y ) , self )
            self.act8_gps.setStyleSheet( self._lb_style )
            self.act8_gps.setGeometry( 220, 325 ,350,30 ) # x , y , w , h     
            self.act8_gps.setVisible( True )

            self.act8_gps_btn = QPushButton('좌표지정',self)
            self.act8_gps_btn.clicked.connect(    self.fn_act8_gps   )  
            
            self.act8_gps_btn.setGeometry( 570, 325 ,100,30 ) # x , y , w , h 
            self.act8_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act8_direct = QComboBox(self)
            self.act8_direct.addItem('상')
            self.act8_direct.addItem('하')
            self.act8_direct.addItem('좌')
            self.act8_direct.addItem('우')
            self.act8_direct.setGeometry(220, 325 ,100,30) # x , y , w , h    
            self.act8_direct.setVisible( False )
            
            self.act8_direct_cnt = QLineEdit(self)
            self.act8_direct_cnt.setStyleSheet( self._lb_style )
            self.act8_direct_cnt.setText('1')
            self.act8_direct_cnt.setGeometry(320, 325 ,100,30) # x , y , w , h
            self.act8_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act8_paste = QComboBox(self)
            self.act8_paste.addItem('0')
            self.act8_paste.addItem('1')
            self.act8_paste.addItem('2')
            self.act8_paste.addItem('3')
            self.act8_paste.addItem('4')
            self.act8_paste.addItem('5')
            self.act8_paste.addItem('6')
            self.act8_paste.addItem('7')
            self.act8_paste.addItem('8')
            self.act8_paste.setGeometry(220, 325 ,100,30) # x , y , w , h    
            self.act8_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act8_wait = QLineEdit(self)     
            self.act8_wait.setStyleSheet( self._lb_style )
            self.act8_wait.setText('0.5')
            self.act8_wait.setGeometry(670, 325 ,40,30) # x , y , w , h       
            # act8-끝      

            # act9 - 시작
            self.act9_lb = QLabel('3. act9',self)
            self.act9_lb.setGeometry(10, 360 ,100,30) # x , y , w , h
            
            self.act9_yn = QComboBox(self)
            self.act9_yn.addItem('N')
            self.act9_yn.addItem('Y')
            self.act9_yn.setGeometry(110, 360 ,40,30) # x , y , w , h       

            self.act9_select = QComboBox(self)
            self.act9_select.addItem('클릭')
            self.act9_select.addItem('방향키')
            self.act9_select.addItem('붙여넣기')
            self.act9_select.setGeometry(150, 360 ,70,30) # x , y , w , h    
            self.act9_select.activated[str].connect( self.fn_act9_select )
            
            # 클릭 - 시작
            self.act9_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps9_x , self.__gps9_y ) , self )
            self.act9_gps.setStyleSheet( self._lb_style )
            self.act9_gps.setGeometry( 220, 360 ,350,30 ) # x , y , w , h     
            self.act9_gps.setVisible( True )

            self.act9_gps_btn = QPushButton('좌표지정',self)
            self.act9_gps_btn.clicked.connect(    self.fn_act9_gps   )  
            
            self.act9_gps_btn.setGeometry( 570, 360 ,100,30 ) # x , y , w , h 
            self.act9_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act9_direct = QComboBox(self)
            self.act9_direct.addItem('상')
            self.act9_direct.addItem('하')
            self.act9_direct.addItem('좌')
            self.act9_direct.addItem('우')
            self.act9_direct.setGeometry(220, 360 ,100,30) # x , y , w , h    
            self.act9_direct.setVisible( False )
            
            self.act9_direct_cnt = QLineEdit(self)
            self.act9_direct_cnt.setStyleSheet( self._lb_style )
            self.act9_direct_cnt.setText('1')
            self.act9_direct_cnt.setGeometry(320, 360 ,100,30) # x , y , w , h
            self.act9_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act9_paste = QComboBox(self)
            self.act9_paste.addItem('0')
            self.act9_paste.addItem('1')
            self.act9_paste.addItem('2')
            self.act9_paste.addItem('3')
            self.act9_paste.addItem('4')
            self.act9_paste.addItem('5')
            self.act9_paste.addItem('6')
            self.act9_paste.addItem('7')
            self.act9_paste.addItem('8')
            self.act9_paste.setGeometry(220, 360 ,100,30) # x , y , w , h    
            self.act9_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act9_wait = QLineEdit(self)     
            self.act9_wait.setStyleSheet( self._lb_style )
            self.act9_wait.setText('0.5')
            self.act9_wait.setGeometry(670, 360 ,40,30) # x , y , w , h       
            # act9-끝            

            # act10 - 시작
            self.act10_lb = QLabel('3. act10',self)
            self.act10_lb.setGeometry(10, 395 ,100,30) # x , y , w , h
            
            self.act10_yn = QComboBox(self)
            self.act10_yn.addItem('N')
            self.act10_yn.addItem('Y')
            self.act10_yn.setGeometry(110, 395 ,40,30) # x , y , w , h       

            self.act10_select = QComboBox(self)
            self.act10_select.addItem('클릭')
            self.act10_select.addItem('방향키')
            self.act10_select.addItem('붙여넣기')
            self.act10_select.setGeometry(150, 395 ,70,30) # x , y , w , h    
            self.act10_select.activated[str].connect( self.fn_act10_select )
            
            # 클릭 - 시작
            self.act10_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps10_x , self.__gps10_y ) , self )
            self.act10_gps.setStyleSheet( self._lb_style )
            self.act10_gps.setGeometry( 220, 395 ,350,30 ) # x , y , w , h     
            self.act10_gps.setVisible( True )

            self.act10_gps_btn = QPushButton('좌표지정',self)
            self.act10_gps_btn.clicked.connect(    self.fn_act10_gps   )  
            
            self.act10_gps_btn.setGeometry( 570, 395 ,100,30 ) # x , y , w , h 
            self.act10_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act10_direct = QComboBox(self)
            self.act10_direct.addItem('상')
            self.act10_direct.addItem('하')
            self.act10_direct.addItem('좌')
            self.act10_direct.addItem('우')
            self.act10_direct.setGeometry(220, 395 ,100,30) # x , y , w , h    
            self.act10_direct.setVisible( False )
            
            self.act10_direct_cnt = QLineEdit(self)
            self.act10_direct_cnt.setStyleSheet( self._lb_style )
            self.act10_direct_cnt.setText('1')
            self.act10_direct_cnt.setGeometry(320, 395 ,100,30) # x , y , w , h
            self.act10_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act10_paste = QComboBox(self)
            self.act10_paste.addItem('0')
            self.act10_paste.addItem('1')
            self.act10_paste.addItem('2')
            self.act10_paste.addItem('3')
            self.act10_paste.addItem('4')
            self.act10_paste.addItem('5')
            self.act10_paste.addItem('6')
            self.act10_paste.addItem('7')
            self.act10_paste.addItem('8')
            self.act10_paste.setGeometry(220, 395 ,100,30) # x , y , w , h    
            self.act10_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act10_wait = QLineEdit(self)     
            self.act10_wait.setStyleSheet( self._lb_style )
            self.act10_wait.setText('0.5')
            self.act10_wait.setGeometry(670, 395 ,40,30) # x , y , w , h       
            # act10-끝       

            # act11 - 시작
            self.act11_lb = QLabel('3. act11',self)
            self.act11_lb.setGeometry(10, 430 ,100,30) # x , y , w , h
            
            self.act11_yn = QComboBox(self)
            self.act11_yn.addItem('N')
            self.act11_yn.addItem('Y')
            self.act11_yn.setGeometry(110, 430 ,40,30) # x , y , w , h       

            self.act11_select = QComboBox(self)
            self.act11_select.addItem('클릭')
            self.act11_select.addItem('방향키')
            self.act11_select.addItem('붙여넣기')
            self.act11_select.setGeometry(150, 430 ,70,30) # x , y , w , h    
            self.act11_select.activated[str].connect( self.fn_act11_select )
            
            # 클릭 - 시작
            self.act11_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps11_x , self.__gps11_y ) , self )
            self.act11_gps.setStyleSheet( self._lb_style )
            self.act11_gps.setGeometry( 220, 430 ,350,30 ) # x , y , w , h     
            self.act11_gps.setVisible( True )

            self.act11_gps_btn = QPushButton('좌표지정',self)
            self.act11_gps_btn.clicked.connect(    self.fn_act11_gps   )  
            
            self.act11_gps_btn.setGeometry( 570, 430 ,100,30 ) # x , y , w , h 
            self.act11_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act11_direct = QComboBox(self)
            self.act11_direct.addItem('상')
            self.act11_direct.addItem('하')
            self.act11_direct.addItem('좌')
            self.act11_direct.addItem('우')
            self.act11_direct.setGeometry(220, 430 ,100,30) # x , y , w , h    
            self.act11_direct.setVisible( False )
            
            self.act11_direct_cnt = QLineEdit(self)
            self.act11_direct_cnt.setStyleSheet( self._lb_style )
            self.act11_direct_cnt.setText('1')
            self.act11_direct_cnt.setGeometry(320, 430 ,100,30) # x , y , w , h
            self.act11_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act11_paste = QComboBox(self)
            self.act11_paste.addItem('0')
            self.act11_paste.addItem('1')
            self.act11_paste.addItem('2')
            self.act11_paste.addItem('3')
            self.act11_paste.addItem('4')
            self.act11_paste.addItem('5')
            self.act11_paste.addItem('6')
            self.act11_paste.addItem('7')
            self.act11_paste.addItem('8')
            self.act11_paste.setGeometry(220, 430 ,100,30) # x , y , w , h    
            self.act11_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act11_wait = QLineEdit(self)     
            self.act11_wait.setStyleSheet( self._lb_style )
            self.act11_wait.setText('0.5')
            self.act11_wait.setGeometry(670, 430 ,40,30) # x , y , w , h       
            # act11-끝                            

            # act12 - 시작
            self.act12_lb = QLabel('3. act12',self)
            self.act12_lb.setGeometry(10, 465 ,100,30) # x , y , w , h
            
            self.act12_yn = QComboBox(self)
            self.act12_yn.addItem('N')
            self.act12_yn.addItem('Y')
            self.act12_yn.setGeometry(110, 465 ,40,30) # x , y , w , h       

            self.act12_select = QComboBox(self)
            self.act12_select.addItem('클릭')
            self.act12_select.addItem('방향키')
            self.act12_select.addItem('붙여넣기')
            self.act12_select.setGeometry(150, 465 ,70,30) # x , y , w , h    
            self.act12_select.activated[str].connect( self.fn_act12_select )
            
            # 클릭 - 시작
            self.act12_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps12_x , self.__gps12_y ) , self )
            self.act12_gps.setStyleSheet( self._lb_style )
            self.act12_gps.setGeometry( 220, 465 ,350,30 ) # x , y , w , h     
            self.act12_gps.setVisible( True )

            self.act12_gps_btn = QPushButton('좌표지정',self)
            self.act12_gps_btn.clicked.connect(    self.fn_act12_gps   )  
            
            self.act12_gps_btn.setGeometry( 570, 465 ,100,30 ) # x , y , w , h 
            self.act12_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act12_direct = QComboBox(self)
            self.act12_direct.addItem('상')
            self.act12_direct.addItem('하')
            self.act12_direct.addItem('좌')
            self.act12_direct.addItem('우')
            self.act12_direct.setGeometry(220, 465 ,100,30) # x , y , w , h    
            self.act12_direct.setVisible( False )
            
            self.act12_direct_cnt = QLineEdit(self)
            self.act12_direct_cnt.setStyleSheet( self._lb_style )
            self.act12_direct_cnt.setText('1')
            self.act12_direct_cnt.setGeometry(320, 465 ,100,30) # x , y , w , h
            self.act12_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act12_paste = QComboBox(self)
            self.act12_paste.addItem('0')
            self.act12_paste.addItem('1')
            self.act12_paste.addItem('2')
            self.act12_paste.addItem('3')
            self.act12_paste.addItem('4')
            self.act12_paste.addItem('5')
            self.act12_paste.addItem('6')
            self.act12_paste.addItem('7')
            self.act12_paste.addItem('8')
            self.act12_paste.setGeometry(220, 465 ,100,30) # x , y , w , h    
            self.act12_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act12_wait = QLineEdit(self)     
            self.act12_wait.setStyleSheet( self._lb_style )
            self.act12_wait.setText('0.5')
            self.act12_wait.setGeometry(670, 465 ,40,30) # x , y , w , h       
            # act12-끝

            # act13 - 시작
            self.act13_lb = QLabel('3. act13',self)
            self.act13_lb.setGeometry(10, 500 ,100,30) # x , y , w , h
            
            self.act13_yn = QComboBox(self)
            self.act13_yn.addItem('N')
            self.act13_yn.addItem('Y')
            self.act13_yn.setGeometry(110, 500 ,40,30) # x , y , w , h       

            self.act13_select = QComboBox(self)
            self.act13_select.addItem('클릭')
            self.act13_select.addItem('방향키')
            self.act13_select.addItem('붙여넣기')
            self.act13_select.setGeometry(150, 500 ,70,30) # x , y , w , h    
            self.act13_select.activated[str].connect( self.fn_act13_select )
            
            # 클릭 - 시작
            self.act13_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps13_x , self.__gps13_y ) , self )
            self.act13_gps.setStyleSheet( self._lb_style )
            self.act13_gps.setGeometry( 220, 500 ,350,30 ) # x , y , w , h     
            self.act13_gps.setVisible( True )

            self.act13_gps_btn = QPushButton('좌표지정',self)
            self.act13_gps_btn.clicked.connect(    self.fn_act13_gps   )  
            
            self.act13_gps_btn.setGeometry( 570, 500 ,100,30 ) # x , y , w , h 
            self.act13_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act13_direct = QComboBox(self)
            self.act13_direct.addItem('상')
            self.act13_direct.addItem('하')
            self.act13_direct.addItem('좌')
            self.act13_direct.addItem('우')
            self.act13_direct.setGeometry(220, 500 ,100,30) # x , y , w , h    
            self.act13_direct.setVisible( False )
            
            self.act13_direct_cnt = QLineEdit(self)
            self.act13_direct_cnt.setStyleSheet( self._lb_style )
            self.act13_direct_cnt.setText('1')
            self.act13_direct_cnt.setGeometry(320, 500 ,100,30) # x , y , w , h
            self.act13_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act13_paste = QComboBox(self)
            self.act13_paste.addItem('0')
            self.act13_paste.addItem('1')
            self.act13_paste.addItem('2')
            self.act13_paste.addItem('3')
            self.act13_paste.addItem('4')
            self.act13_paste.addItem('5')
            self.act13_paste.addItem('6')
            self.act13_paste.addItem('7')
            self.act13_paste.addItem('8')
            self.act13_paste.setGeometry(220, 500 ,100,30) # x , y , w , h    
            self.act13_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act13_wait = QLineEdit(self)     
            self.act13_wait.setStyleSheet( self._lb_style )
            self.act13_wait.setText('0.5')
            self.act13_wait.setGeometry(670, 500 ,40,30) # x , y , w , h       
            # act13-끝

            # act14 - 시작
            self.act14_lb = QLabel('3. act14',self)
            self.act14_lb.setGeometry(10, 535 ,100,30) # x , y , w , h
            
            self.act14_yn = QComboBox(self)
            self.act14_yn.addItem('N')
            self.act14_yn.addItem('Y')
            self.act14_yn.setGeometry(110, 535 ,40,30) # x , y , w , h       

            self.act14_select = QComboBox(self)
            self.act14_select.addItem('클릭')
            self.act14_select.addItem('방향키')
            self.act14_select.addItem('붙여넣기')
            self.act14_select.setGeometry(150, 535 ,70,30) # x , y , w , h    
            self.act14_select.activated[str].connect( self.fn_act14_select )
            
            # 클릭 - 시작
            self.act14_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps14_x , self.__gps14_y ) , self )
            self.act14_gps.setStyleSheet( self._lb_style )
            self.act14_gps.setGeometry( 220, 535 ,350,30 ) # x , y , w , h     
            self.act14_gps.setVisible( True )

            self.act14_gps_btn = QPushButton('좌표지정',self)
            self.act14_gps_btn.clicked.connect(    self.fn_act14_gps   )  
            
            self.act14_gps_btn.setGeometry( 570, 535 ,100,30 ) # x , y , w , h 
            self.act14_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act14_direct = QComboBox(self)
            self.act14_direct.addItem('상')
            self.act14_direct.addItem('하')
            self.act14_direct.addItem('좌')
            self.act14_direct.addItem('우')
            self.act14_direct.setGeometry(220, 535 ,100,30) # x , y , w , h    
            self.act14_direct.setVisible( False )
            
            self.act14_direct_cnt = QLineEdit(self)
            self.act14_direct_cnt.setStyleSheet( self._lb_style )
            self.act14_direct_cnt.setText('1')
            self.act14_direct_cnt.setGeometry(320, 535 ,100,30) # x , y , w , h
            self.act14_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act14_paste = QComboBox(self)
            self.act14_paste.addItem('0')
            self.act14_paste.addItem('1')
            self.act14_paste.addItem('2')
            self.act14_paste.addItem('3')
            self.act14_paste.addItem('4')
            self.act14_paste.addItem('5')
            self.act14_paste.addItem('6')
            self.act14_paste.addItem('7')
            self.act14_paste.addItem('8')
            self.act14_paste.setGeometry(220, 535 ,100,30) # x , y , w , h    
            self.act14_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act14_wait = QLineEdit(self)     
            self.act14_wait.setStyleSheet( self._lb_style )
            self.act14_wait.setText('0.5')
            self.act14_wait.setGeometry(670, 535 ,40,30) # x , y , w , h       
            # act14-끝

            # act15 - 시작
            self.act15_lb = QLabel('3. act15',self)
            self.act15_lb.setGeometry(10, 570 ,100,30) # x , y , w , h
            
            self.act15_yn = QComboBox(self)
            self.act15_yn.addItem('N')
            self.act15_yn.addItem('Y')
            self.act15_yn.setGeometry(110, 570 ,40,30) # x , y , w , h       

            self.act15_select = QComboBox(self)
            self.act15_select.addItem('클릭')
            self.act15_select.addItem('방향키')
            self.act15_select.addItem('붙여넣기')
            self.act15_select.setGeometry(150, 570 ,70,30) # x , y , w , h    
            self.act15_select.activated[str].connect( self.fn_act15_select )
            
            # 클릭 - 시작
            self.act15_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps15_x , self.__gps15_y ) , self )
            self.act15_gps.setStyleSheet( self._lb_style )
            self.act15_gps.setGeometry( 220, 570 ,350,30 ) # x , y , w , h     
            self.act15_gps.setVisible( True )

            self.act15_gps_btn = QPushButton('좌표지정',self)
            self.act15_gps_btn.clicked.connect(    self.fn_act15_gps   )  
            
            self.act15_gps_btn.setGeometry( 570, 570 ,100,30 ) # x , y , w , h 
            self.act15_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act15_direct = QComboBox(self)
            self.act15_direct.addItem('상')
            self.act15_direct.addItem('하')
            self.act15_direct.addItem('좌')
            self.act15_direct.addItem('우')
            self.act15_direct.setGeometry(220, 570 ,100,30) # x , y , w , h    
            self.act15_direct.setVisible( False )
            
            self.act15_direct_cnt = QLineEdit(self)
            self.act15_direct_cnt.setStyleSheet( self._lb_style )
            self.act15_direct_cnt.setText('1')
            self.act15_direct_cnt.setGeometry(320, 570 ,100,30) # x , y , w , h
            self.act15_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act15_paste = QComboBox(self)
            self.act15_paste.addItem('0')
            self.act15_paste.addItem('1')
            self.act15_paste.addItem('2')
            self.act15_paste.addItem('3')
            self.act15_paste.addItem('4')
            self.act15_paste.addItem('5')
            self.act15_paste.addItem('6')
            self.act15_paste.addItem('7')
            self.act15_paste.addItem('8')
            self.act15_paste.setGeometry(220, 570 ,100,30) # x , y , w , h    
            self.act15_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act15_wait = QLineEdit(self)     
            self.act15_wait.setStyleSheet( self._lb_style )
            self.act15_wait.setText('0.5')
            self.act15_wait.setGeometry(670, 570 ,40,30) # x , y , w , h       
            # act15-끝

            # act16 - 시작
            self.act16_lb = QLabel('3. act16',self)
            self.act16_lb.setGeometry(10, 605 ,100,30) # x , y , w , h
            
            self.act16_yn = QComboBox(self)
            self.act16_yn.addItem('N')
            self.act16_yn.addItem('Y')
            self.act16_yn.setGeometry(110, 605 ,40,30) # x , y , w , h       

            self.act16_select = QComboBox(self)
            self.act16_select.addItem('클릭')
            self.act16_select.addItem('방향키')
            self.act16_select.addItem('붙여넣기')
            self.act16_select.setGeometry(150, 605 ,70,30) # x , y , w , h    
            self.act16_select.activated[str].connect( self.fn_act16_select )
            
            # 클릭 - 시작
            self.act16_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps16_x , self.__gps16_y ) , self )
            self.act16_gps.setStyleSheet( self._lb_style )
            self.act16_gps.setGeometry( 220, 605 ,350,30 ) # x , y , w , h     
            self.act16_gps.setVisible( True )

            self.act16_gps_btn = QPushButton('좌표지정',self)
            self.act16_gps_btn.clicked.connect(    self.fn_act16_gps   )  
            
            self.act16_gps_btn.setGeometry( 570, 605 ,100,30 ) # x , y , w , h 
            self.act16_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act16_direct = QComboBox(self)
            self.act16_direct.addItem('상')
            self.act16_direct.addItem('하')
            self.act16_direct.addItem('좌')
            self.act16_direct.addItem('우')
            self.act16_direct.setGeometry(220, 605 ,100,30) # x , y , w , h    
            self.act16_direct.setVisible( False )
            
            self.act16_direct_cnt = QLineEdit(self)
            self.act16_direct_cnt.setStyleSheet( self._lb_style )
            self.act16_direct_cnt.setText('1')
            self.act16_direct_cnt.setGeometry(320, 605 ,100,30) # x , y , w , h
            self.act16_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act16_paste = QComboBox(self)
            self.act16_paste.addItem('0')
            self.act16_paste.addItem('1')
            self.act16_paste.addItem('2')
            self.act16_paste.addItem('3')
            self.act16_paste.addItem('4')
            self.act16_paste.addItem('5')
            self.act16_paste.addItem('6')
            self.act16_paste.addItem('7')
            self.act16_paste.addItem('8')
            self.act16_paste.setGeometry(220, 605 ,100,30) # x , y , w , h    
            self.act16_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act16_wait = QLineEdit(self)     
            self.act16_wait.setStyleSheet( self._lb_style )
            self.act16_wait.setText('0.5')
            self.act16_wait.setGeometry(670, 605 ,40,30) # x , y , w , h       
            # act16-끝

            # act17 - 시작
            self.act17_lb = QLabel('3. act17',self)
            self.act17_lb.setGeometry(10, 640 ,100,30) # x , y , w , h
            
            self.act17_yn = QComboBox(self)
            self.act17_yn.addItem('N')
            self.act17_yn.addItem('Y')
            self.act17_yn.setGeometry(110, 640 ,40,30) # x , y , w , h       

            self.act17_select = QComboBox(self)
            self.act17_select.addItem('클릭')
            self.act17_select.addItem('방향키')
            self.act17_select.addItem('붙여넣기')
            self.act17_select.setGeometry(150, 640 ,70,30) # x , y , w , h    
            self.act17_select.activated[str].connect( self.fn_act17_select )
            
            # 클릭 - 시작
            self.act17_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps17_x , self.__gps17_y ) , self )
            self.act17_gps.setStyleSheet( self._lb_style )
            self.act17_gps.setGeometry( 220, 640 ,350,30 ) # x , y , w , h     
            self.act17_gps.setVisible( True )

            self.act17_gps_btn = QPushButton('좌표지정',self)
            self.act17_gps_btn.clicked.connect(    self.fn_act17_gps   )  
            
            self.act17_gps_btn.setGeometry( 570, 640 ,100,30 ) # x , y , w , h 
            self.act17_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act17_direct = QComboBox(self)
            self.act17_direct.addItem('상')
            self.act17_direct.addItem('하')
            self.act17_direct.addItem('좌')
            self.act17_direct.addItem('우')
            self.act17_direct.setGeometry(220, 640 ,100,30) # x , y , w , h    
            self.act17_direct.setVisible( False )
            
            self.act17_direct_cnt = QLineEdit(self)
            self.act17_direct_cnt.setStyleSheet( self._lb_style )
            self.act17_direct_cnt.setText('1')
            self.act17_direct_cnt.setGeometry(640, 605 ,100,30) # x , y , w , h
            self.act17_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act17_paste = QComboBox(self)
            self.act17_paste.addItem('0')
            self.act17_paste.addItem('1')
            self.act17_paste.addItem('2')
            self.act17_paste.addItem('3')
            self.act17_paste.addItem('4')
            self.act17_paste.addItem('5')
            self.act17_paste.addItem('6')
            self.act17_paste.addItem('7')
            self.act17_paste.addItem('8')
            self.act17_paste.setGeometry(220, 640 ,100,30) # x , y , w , h    
            self.act17_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act17_wait = QLineEdit(self)     
            self.act17_wait.setStyleSheet( self._lb_style )
            self.act17_wait.setText('0.5')
            self.act17_wait.setGeometry(670, 640 ,40,30) # x , y , w , h       
            # act17-끝

            # act18 - 시작
            self.act18_lb = QLabel('3. act18',self)
            self.act18_lb.setGeometry(10, 675 ,100,30) # x , y , w , h
            
            self.act18_yn = QComboBox(self)
            self.act18_yn.addItem('N')
            self.act18_yn.addItem('Y')
            self.act18_yn.setGeometry(110, 675 ,40,30) # x , y , w , h       

            self.act18_select = QComboBox(self)
            self.act18_select.addItem('클릭')
            self.act18_select.addItem('방향키')
            self.act18_select.addItem('붙여넣기')
            self.act18_select.setGeometry(150, 675 ,70,30) # x , y , w , h    
            self.act18_select.activated[str].connect( self.fn_act18_select )
            
            # 클릭 - 시작
            self.act18_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps18_x , self.__gps18_y ) , self )
            self.act18_gps.setStyleSheet( self._lb_style )
            self.act18_gps.setGeometry( 220, 675 ,350,30 ) # x , y , w , h     
            self.act18_gps.setVisible( True )

            self.act18_gps_btn = QPushButton('좌표지정',self)
            self.act18_gps_btn.clicked.connect(    self.fn_act18_gps   )  
            
            self.act18_gps_btn.setGeometry( 570, 675 ,100,30 ) # x , y , w , h 
            self.act18_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act18_direct = QComboBox(self)
            self.act18_direct.addItem('상')
            self.act18_direct.addItem('하')
            self.act18_direct.addItem('좌')
            self.act18_direct.addItem('우')
            self.act18_direct.setGeometry(220, 675 ,100,30) # x , y , w , h    
            self.act18_direct.setVisible( False )
            
            self.act18_direct_cnt = QLineEdit(self)
            self.act18_direct_cnt.setStyleSheet( self._lb_style )
            self.act18_direct_cnt.setText('1')
            self.act18_direct_cnt.setGeometry(640, 675 ,100,30) # x , y , w , h
            self.act18_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act18_paste = QComboBox(self)
            self.act18_paste.addItem('0')
            self.act18_paste.addItem('1')
            self.act18_paste.addItem('2')
            self.act18_paste.addItem('3')
            self.act18_paste.addItem('4')
            self.act18_paste.addItem('5')
            self.act18_paste.addItem('6')
            self.act18_paste.addItem('7')
            self.act18_paste.addItem('8')
            self.act18_paste.setGeometry(220, 675 ,100,30) # x , y , w , h    
            self.act18_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act18_wait = QLineEdit(self)     
            self.act18_wait.setStyleSheet( self._lb_style )
            self.act18_wait.setText('0.5')
            self.act18_wait.setGeometry(670, 675 ,40,30) # x , y , w , h       
            # act18-끝

            # act19 - 시작
            self.act19_lb = QLabel('3. act19',self)
            self.act19_lb.setGeometry(10, 710 ,100,30) # x , y , w , h
            
            self.act19_yn = QComboBox(self)
            self.act19_yn.addItem('N')
            self.act19_yn.addItem('Y')
            self.act19_yn.setGeometry(110, 710 ,40,30) # x , y , w , h       

            self.act19_select = QComboBox(self)
            self.act19_select.addItem('클릭')
            self.act19_select.addItem('방향키')
            self.act19_select.addItem('붙여넣기')
            self.act19_select.setGeometry(150, 710 ,70,30) # x , y , w , h    
            self.act19_select.activated[str].connect( self.fn_act19_select )
            
            # 클릭 - 시작
            self.act19_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps19_x , self.__gps19_y ) , self )
            self.act19_gps.setStyleSheet( self._lb_style )
            self.act19_gps.setGeometry( 220, 710 ,350,30 ) # x , y , w , h     
            self.act19_gps.setVisible( True )

            self.act19_gps_btn = QPushButton('좌표지정',self)
            self.act19_gps_btn.clicked.connect(    self.fn_act19_gps   )  
            
            self.act19_gps_btn.setGeometry( 570, 710 ,100,30 ) # x , y , w , h 
            self.act19_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act19_direct = QComboBox(self)
            self.act19_direct.addItem('상')
            self.act19_direct.addItem('하')
            self.act19_direct.addItem('좌')
            self.act19_direct.addItem('우')
            self.act19_direct.setGeometry(220, 710 ,100,30) # x , y , w , h    
            self.act19_direct.setVisible( False )
            
            self.act19_direct_cnt = QLineEdit(self)
            self.act19_direct_cnt.setStyleSheet( self._lb_style )
            self.act19_direct_cnt.setText('1')
            self.act19_direct_cnt.setGeometry(640, 710 ,100,30) # x , y , w , h
            self.act19_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act19_paste = QComboBox(self)
            self.act19_paste.addItem('0')
            self.act19_paste.addItem('1')
            self.act19_paste.addItem('2')
            self.act19_paste.addItem('3')
            self.act19_paste.addItem('4')
            self.act19_paste.addItem('5')
            self.act19_paste.addItem('6')
            self.act19_paste.addItem('7')
            self.act19_paste.addItem('8')
            self.act19_paste.setGeometry(220, 710 ,100,30) # x , y , w , h    
            self.act19_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act19_wait = QLineEdit(self)     
            self.act19_wait.setStyleSheet( self._lb_style )
            self.act19_wait.setText('0.5')
            self.act19_wait.setGeometry(670, 710 ,40,30) # x , y , w , h       
            # act19-끝

            # act20 - 시작
            self.act20_lb = QLabel('3. act20',self)
            self.act20_lb.setGeometry(10, 745 ,100,30) # x , y , w , h
            
            self.act20_yn = QComboBox(self)
            self.act20_yn.addItem('N')
            self.act20_yn.addItem('Y')
            self.act20_yn.setGeometry(110, 745 ,40,30) # x , y , w , h       

            self.act20_select = QComboBox(self)
            self.act20_select.addItem('클릭')
            self.act20_select.addItem('방향키')
            self.act20_select.addItem('붙여넣기')
            self.act20_select.setGeometry(150, 745 ,70,30) # x , y , w , h    
            self.act20_select.activated[str].connect( self.fn_act20_select )
            
            # 클릭 - 시작
            self.act20_gps = QLabel('( x : {0} , y : {1} )'.format( self.__gps20_x , self.__gps20_y ) , self )
            self.act20_gps.setStyleSheet( self._lb_style )
            self.act20_gps.setGeometry( 220, 745 ,350,30 ) # x , y , w , h     
            self.act20_gps.setVisible( True )

            self.act20_gps_btn = QPushButton('좌표지정',self)
            self.act20_gps_btn.clicked.connect(    self.fn_act20_gps   )  
            
            self.act20_gps_btn.setGeometry( 570, 745 ,100,30 ) # x , y , w , h 
            self.act20_gps_btn.setVisible( True )
            # 클릭 - 끝
            
            # 방향키 - 시작
            self.act20_direct = QComboBox(self)
            self.act20_direct.addItem('상')
            self.act20_direct.addItem('하')
            self.act20_direct.addItem('좌')
            self.act20_direct.addItem('우')
            self.act20_direct.setGeometry(220, 745 ,100,30) # x , y , w , h    
            self.act20_direct.setVisible( False )
            
            self.act20_direct_cnt = QLineEdit(self)
            self.act20_direct_cnt.setStyleSheet( self._lb_style )
            self.act20_direct_cnt.setText('1')
            self.act20_direct_cnt.setGeometry(640, 745 ,100,30) # x , y , w , h
            self.act20_direct_cnt.setVisible( False )
            # 방향키 - 끝

            # 붙여넣기 - 시작
            self.act20_paste = QComboBox(self)
            self.act20_paste.addItem('0')
            self.act20_paste.addItem('1')
            self.act20_paste.addItem('2')
            self.act20_paste.addItem('3')
            self.act20_paste.addItem('4')
            self.act20_paste.addItem('5')
            self.act20_paste.addItem('6')
            self.act20_paste.addItem('7')
            self.act20_paste.addItem('8')
            self.act20_paste.setGeometry(220, 745 ,100,30) # x , y , w , h    
            self.act20_paste.setVisible( False )            
            # 붙여넣기 - 끝

            self.act20_wait = QLineEdit(self)     
            self.act20_wait.setStyleSheet( self._lb_style )
            self.act20_wait.setText('0.5')
            self.act20_wait.setGeometry(670, 745 ,40,30) # x , y , w , h       
            # act20-끝


            self.save_btn = QPushButton('Save',self)
            self.save_btn.clicked.connect(    self.fn_save   )  
            self.save_btn.setGeometry(10, 780 ,260,30) # x , y , w , h    

            self.load_btn = QPushButton('Load',self)
            self.load_btn.clicked.connect(    self.fn_load   )  
            self.load_btn.setGeometry(275, 780 ,260,30) # x , y , w , h    

            self.start_btn = QPushButton('Start/Stop',self)
            self.start_btn.clicked.connect(    self.fn_start_stop   )  
            self.start_btn.setGeometry(540, 780 ,100,30) # x , y , w , h   

            self.close_btn = QPushButton('Close',self)
            self.close_btn.clicked.connect(    self.fn_close   )  
            self.close_btn.setGeometry(645, 780 ,50,30) # x , y , w , h   

            self.save_lb = QLabel('저장파일 : ' , self )
            self.save_lb.setGeometry(10, 815 ,60,30) # x , y , w , h       
            
            self.save_file_nm = QLineEdit(self)     
            self.save_file_nm.setStyleSheet( self._lb_style )
            self.save_file_nm.setGeometry(75, 815 ,195,30) # x , y , w , h       

            self.load_lb = QLabel('로드파일 : ' , self )
            self.load_lb.setGeometry(275, 815 ,60,30) # x , y , w , h       
            
            
            file_list = self.getfolelist()
            self.load_cb = QComboBox(self)
            #self.load_cb.addItem('0')
            for i in file_list:
                self.load_cb.addItem(i)
            
            # 파일로드
            self.load_cb.setGeometry(340, 815 ,195,30) # x , y , w , h    


            self.setMouseTracking(True) # 마우스 이벤트        
            self.setWindowTitle('MACRO')
            self.setGeometry(1000, 50, 712, 900)
            self.show()
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F:
            if self.__gps_info != '':
                xy = pyautogui.position()
                if self.__gps_info == '1':
                    self.__gps1_x , self.__gps1_y = xy.x , xy.y
                    self.act1_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps1_x , self.__gps1_y) )
                elif self.__gps_info == '2':
                    self.__gps2_x , self.__gps2_y = xy.x , xy.y
                    self.act2_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps2_x , self.__gps2_y) )                    
                elif self.__gps_info == '3':
                    self.__gps3_x , self.__gps3_y = xy.x , xy.y
                    self.act3_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps3_x , self.__gps3_y) )                    
                elif self.__gps_info == '4':
                    self.__gps4_x , self.__gps4_y = xy.x , xy.y
                    self.act4_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps4_x , self.__gps4_y) )                    
                elif self.__gps_info == '5':
                    self.__gps5_x , self.__gps5_y = xy.x , xy.y
                    self.act5_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps5_x , self.__gps5_y) )                    
                elif self.__gps_info == '6':
                    self.__gps6_x , self.__gps6_y = xy.x , xy.y
                    self.act6_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps6_x , self.__gps6_y) )                    
                elif self.__gps_info == '7':
                    self.__gps7_x , self.__gps7_y = xy.x , xy.y
                    self.act7_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps7_x , self.__gps7_y) )                    
                elif self.__gps_info == '8':
                    self.__gps8_x , self.__gps8_y = xy.x , xy.y
                    self.act8_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps8_x , self.__gps8_y) )                    
                elif self.__gps_info == '9':
                    self.__gps9_x , self.__gps9_y = xy.x , xy.y
                    self.act9_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps9_x , self.__gps9_y) )                    
                elif self.__gps_info == '10':
                    self.__gps10_x , self.__gps10_y = xy.x , xy.y
                    self.act10_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps10_x , self.__gps10_y) )                    
                elif self.__gps_info == '11':
                    self.__gps11_x , self.__gps11_y = xy.x , xy.y
                    self.act11_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps11_x , self.__gps11_y) )                    
                elif self.__gps_info == '12':
                    self.__gps12_x , self.__gps12_y = xy.x , xy.y
                    self.act12_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps12_x , self.__gps12_y) )                    
                elif self.__gps_info == '13':
                    self.__gps13_x , self.__gps13_y = xy.x , xy.y
                    self.act13_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps13_x , self.__gps13_y) )                    
                elif self.__gps_info == '14':
                    self.__gps14_x , self.__gps14_y = xy.x , xy.y
                    self.act14_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps14_x , self.__gps14_y) )                    
                elif self.__gps_info == '15':
                    self.__gps15_x , self.__gps15_y = xy.x , xy.y
                    self.act15_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps15_x , self.__gps15_y) )                    
                elif self.__gps_info == '16':
                    self.__gps16_x , self.__gps16_y = xy.x , xy.y
                    self.act16_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps16_x , self.__gps16_y) )                    
                elif self.__gps_info == '17':
                    self.__gps17_x , self.__gps17_y = xy.x , xy.y
                    self.act17_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps17_x , self.__gps17_y) )                    
                elif self.__gps_info == '18':
                    self.__gps18_x , self.__gps18_y = xy.x , xy.y
                    self.act18_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps18_x , self.__gps18_y) )                                                                                
                elif self.__gps_info == '19':
                    self.__gps19_x , self.__gps19_y = xy.x , xy.y
                    self.act19_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps19_x , self.__gps19_y) )                    
                elif self.__gps_info == '20':
                    self.__gps20_x , self.__gps20_y = xy.x , xy.y
                    self.act20_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps20_x , self.__gps20_y) )                                                            


                self.__gps_info =''

  

    def fn_act1_gps(self):
        self.__gps_info='1'
    def fn_act2_gps(self):
        self.__gps_info='2'
    def fn_act3_gps(self):
        self.__gps_info='3'
    def fn_act4_gps(self):
        self.__gps_info='4'
    def fn_act5_gps(self):
        self.__gps_info='5'
    def fn_act6_gps(self):
        self.__gps_info='6'
    def fn_act7_gps(self):
        self.__gps_info='7'
    def fn_act8_gps(self):
        self.__gps_info='8'        
    def fn_act9_gps(self):
        self.__gps_info='9'
    def fn_act10_gps(self):
        self.__gps_info='10'
    def fn_act11_gps(self):
        self.__gps_info='11'
    def fn_act12_gps(self):
        self.__gps_info='12'
    def fn_act13_gps(self):
        self.__gps_info='13'
    def fn_act14_gps(self):
        self.__gps_info='14'
    def fn_act15_gps(self):
        self.__gps_info='15'
    def fn_act16_gps(self):
        self.__gps_info='16'
    def fn_act17_gps(self):
        self.__gps_info='17'
    def fn_act18_gps(self):
        self.__gps_info='18'
    def fn_act19_gps(self):
        self.__gps_info='19'
    def fn_act20_gps(self):
        self.__gps_info='20'
    

    def fn_act1_select(self,text):
        if text == '클릭':
            self.act1_gps.setVisible( True )
            self.act1_gps_btn.setVisible( True ) 
            self.act1_direct.setVisible( False )            
            self.act1_direct_cnt.setVisible(False)   
            self.act1_paste.setVisible( False ) 
        elif text == '방향키':
            self.act1_gps.setVisible( False )
            self.act1_gps_btn.setVisible( False ) 
            self.act1_direct.setVisible( True )            
            self.act1_direct_cnt.setVisible(True)   
            self.act1_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act1_gps.setVisible( False )
            self.act1_gps_btn.setVisible( False ) 
            self.act1_direct.setVisible( False )            
            self.act1_direct_cnt.setVisible(False)   
            self.act1_paste.setVisible( True )     
    def fn_act2_select(self,text):
        if text == '클릭':
            self.act2_gps.setVisible( True )
            self.act2_gps_btn.setVisible( True ) 
            self.act2_direct.setVisible( False )            
            self.act2_direct_cnt.setVisible(False)   
            self.act2_paste.setVisible( False ) 
        elif text == '방향키':
            self.act2_gps.setVisible( False )
            self.act2_gps_btn.setVisible( False ) 
            self.act2_direct.setVisible( True )            
            self.act2_direct_cnt.setVisible(True)   
            self.act2_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act2_gps.setVisible( False )
            self.act2_gps_btn.setVisible( False ) 
            self.act2_direct.setVisible( False )            
            self.act2_direct_cnt.setVisible(False)   
            self.act2_paste.setVisible( True )
    def fn_act3_select(self,text):
        if text == '클릭':
            self.act3_gps.setVisible( True )
            self.act3_gps_btn.setVisible( True ) 
            self.act3_direct.setVisible( False )            
            self.act3_direct_cnt.setVisible(False)   
            self.act3_paste.setVisible( False ) 
        elif text == '방향키':
            self.act3_gps.setVisible( False )
            self.act3_gps_btn.setVisible( False ) 
            self.act3_direct.setVisible( True )            
            self.act3_direct_cnt.setVisible(True)   
            self.act3_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act3_gps.setVisible( False )
            self.act3_gps_btn.setVisible( False ) 
            self.act3_direct.setVisible( False )            
            self.act3_direct_cnt.setVisible(False)   
            self.act3_paste.setVisible( True )
    def fn_act4_select(self,text):
        if text == '클릭':
            self.act4_gps.setVisible( True )
            self.act4_gps_btn.setVisible( True ) 
            self.act4_direct.setVisible( False )            
            self.act4_direct_cnt.setVisible(False)   
            self.act4_paste.setVisible( False ) 
        elif text == '방향키':
            self.act4_gps.setVisible( False )
            self.act4_gps_btn.setVisible( False ) 
            self.act4_direct.setVisible( True )            
            self.act4_direct_cnt.setVisible(True)   
            self.act4_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act4_gps.setVisible( False )
            self.act4_gps_btn.setVisible( False ) 
            self.act4_direct.setVisible( False )            
            self.act4_direct_cnt.setVisible(False)   
            self.act4_paste.setVisible( True )
    def fn_act5_select(self,text):
        if text == '클릭':
            self.act5_gps.setVisible( True )
            self.act5_gps_btn.setVisible( True ) 
            self.act5_direct.setVisible( False )            
            self.act5_direct_cnt.setVisible(False)   
            self.act5_paste.setVisible( False ) 
        elif text == '방향키':
            self.act5_gps.setVisible( False )
            self.act5_gps_btn.setVisible( False ) 
            self.act5_direct.setVisible( True )            
            self.act5_direct_cnt.setVisible(True)   
            self.act5_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act5_gps.setVisible( False )
            self.act5_gps_btn.setVisible( False ) 
            self.act5_direct.setVisible( False )            
            self.act5_direct_cnt.setVisible(False)   
            self.act5_paste.setVisible( True )
    def fn_act6_select(self,text):
        if text == '클릭':
            self.act6_gps.setVisible( True )
            self.act6_gps_btn.setVisible( True ) 
            self.act6_direct.setVisible( False )            
            self.act6_direct_cnt.setVisible(False)   
            self.act6_paste.setVisible( False ) 
        elif text == '방향키':
            self.act6_gps.setVisible( False )
            self.act6_gps_btn.setVisible( False ) 
            self.act6_direct.setVisible( True )            
            self.act6_direct_cnt.setVisible(True)   
            self.act6_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act6_gps.setVisible( False )
            self.act6_gps_btn.setVisible( False ) 
            self.act6_direct.setVisible( False )            
            self.act6_direct_cnt.setVisible(False)   
            self.act6_paste.setVisible( True )    
    def fn_act7_select(self,text):
        if text == '클릭':
            self.act7_gps.setVisible( True )
            self.act7_gps_btn.setVisible( True ) 
            self.act7_direct.setVisible( False )            
            self.act7_direct_cnt.setVisible(False)   
            self.act7_paste.setVisible( False ) 
        elif text == '방향키':
            self.act7_gps.setVisible( False )
            self.act7_gps_btn.setVisible( False ) 
            self.act7_direct.setVisible( True )            
            self.act7_direct_cnt.setVisible(True)   
            self.act7_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act7_gps.setVisible( False )
            self.act7_gps_btn.setVisible( False ) 
            self.act7_direct.setVisible( False )            
            self.act7_direct_cnt.setVisible(False)   
            self.act7_paste.setVisible( True )    
    def fn_act8_select(self,text):
        if text == '클릭':
            self.act8_gps.setVisible( True )
            self.act8_gps_btn.setVisible( True ) 
            self.act8_direct.setVisible( False )            
            self.act8_direct_cnt.setVisible(False)   
            self.act8_paste.setVisible( False ) 
        elif text == '방향키':
            self.act8_gps.setVisible( False )
            self.act8_gps_btn.setVisible( False ) 
            self.act8_direct.setVisible( True )            
            self.act8_direct_cnt.setVisible(True)   
            self.act8_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act8_gps.setVisible( False )
            self.act8_gps_btn.setVisible( False ) 
            self.act8_direct.setVisible( False )            
            self.act8_direct_cnt.setVisible(False)   
            self.act8_paste.setVisible( True )    
    def fn_act9_select(self,text):
        if text == '클릭':
            self.act9_gps.setVisible( True )
            self.act9_gps_btn.setVisible( True ) 
            self.act9_direct.setVisible( False )            
            self.act9_direct_cnt.setVisible(False)   
            self.act9_paste.setVisible( False ) 
        elif text == '방향키':
            self.act9_gps.setVisible( False )
            self.act9_gps_btn.setVisible( False ) 
            self.act9_direct.setVisible( True )            
            self.act9_direct_cnt.setVisible(True)   
            self.act9_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act9_gps.setVisible( False )
            self.act9_gps_btn.setVisible( False ) 
            self.act9_direct.setVisible( False )            
            self.act9_direct_cnt.setVisible(False)   
            self.act9_paste.setVisible( True )
    def fn_act10_select(self,text):
        if text == '클릭':
            self.act10_gps.setVisible( True )
            self.act10_gps_btn.setVisible( True ) 
            self.act10_direct.setVisible( False )            
            self.act10_direct_cnt.setVisible(False)   
            self.act10_paste.setVisible( False ) 
        elif text == '방향키':
            self.act10_gps.setVisible( False )
            self.act10_gps_btn.setVisible( False ) 
            self.act10_direct.setVisible( True )            
            self.act10_direct_cnt.setVisible(True)   
            self.act10_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act10_gps.setVisible( False )
            self.act10_gps_btn.setVisible( False ) 
            self.act10_direct.setVisible( False )            
            self.act10_direct_cnt.setVisible(False)   
            self.act10_direct_cnt.setVisible(False)   
            self.act10_paste.setVisible( True )
    def fn_act11_select(self,text):
        if text == '클릭':
            self.act11_gps.setVisible( True )
            self.act11_gps_btn.setVisible( True ) 
            self.act11_direct.setVisible( False )            
            self.act11_direct_cnt.setVisible(False)   
            self.act11_paste.setVisible( False ) 
        elif text == '방향키':
            self.act11_gps.setVisible( False )
            self.act11_gps_btn.setVisible( False ) 
            self.act11_direct.setVisible( True )            
            self.act11_direct_cnt.setVisible(True)   
            self.act11_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act11_gps.setVisible( False )
            self.act11_gps_btn.setVisible( False ) 
            self.act11_direct.setVisible( False )            
            self.act11_direct_cnt.setVisible(False)   
            self.act11_direct_cnt.setVisible(False)   
            self.act11_paste.setVisible( True )    
    def fn_act12_select(self,text):
        if text == '클릭':
            self.act12_gps.setVisible( True )
            self.act12_gps_btn.setVisible( True ) 
            self.act12_direct.setVisible( False )            
            self.act12_direct_cnt.setVisible(False)   
            self.act12_paste.setVisible( False ) 
        elif text == '방향키':
            self.act12_gps.setVisible( False )
            self.act12_gps_btn.setVisible( False ) 
            self.act12_direct.setVisible( True )            
            self.act12_direct_cnt.setVisible(True)   
            self.act12_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act12_gps.setVisible( False )
            self.act12_gps_btn.setVisible( False ) 
            self.act12_direct.setVisible( False )            
            self.act12_direct_cnt.setVisible(False)   
            self.act12_direct_cnt.setVisible(False)   
            self.act12_paste.setVisible( True )
    def fn_act13_select(self,text):
        if text == '클릭':
            self.act13_gps.setVisible( True )
            self.act13_gps_btn.setVisible( True ) 
            self.act13_direct.setVisible( False )            
            self.act13_direct_cnt.setVisible(False)   
            self.act13_paste.setVisible( False ) 
        elif text == '방향키':
            self.act13_gps.setVisible( False )
            self.act13_gps_btn.setVisible( False ) 
            self.act13_direct.setVisible( True )            
            self.act13_direct_cnt.setVisible(True)   
            self.act13_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act13_gps.setVisible( False )
            self.act13_gps_btn.setVisible( False ) 
            self.act13_direct.setVisible( False )            
            self.act13_direct_cnt.setVisible(False)   
            self.act13_direct_cnt.setVisible(False)   
            self.act13_paste.setVisible( True )
    def fn_act14_select(self,text):
        if text == '클릭':
            self.act14_gps.setVisible( True )
            self.act14_gps_btn.setVisible( True ) 
            self.act14_direct.setVisible( False )            
            self.act14_direct_cnt.setVisible(False)   
            self.act14_paste.setVisible( False ) 
        elif text == '방향키':
            self.act14_gps.setVisible( False )
            self.act14_gps_btn.setVisible( False ) 
            self.act14_direct.setVisible( True )            
            self.act14_direct_cnt.setVisible(True)   
            self.act14_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act14_gps.setVisible( False )
            self.act14_gps_btn.setVisible( False ) 
            self.act14_direct.setVisible( False )            
            self.act14_direct_cnt.setVisible(False)   
            self.act14_direct_cnt.setVisible(False)   
            self.act14_paste.setVisible( True )
    def fn_act15_select(self,text):
        if text == '클릭':
            self.act15_gps.setVisible( True )
            self.act15_gps_btn.setVisible( True ) 
            self.act15_direct.setVisible( False )            
            self.act15_direct_cnt.setVisible(False)   
            self.act15_paste.setVisible( False ) 
        elif text == '방향키':
            self.act15_gps.setVisible( False )
            self.act15_gps_btn.setVisible( False ) 
            self.act15_direct.setVisible( True )            
            self.act15_direct_cnt.setVisible(True)   
            self.act15_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act15_gps.setVisible( False )
            self.act15_gps_btn.setVisible( False ) 
            self.act15_direct.setVisible( False )            
            self.act15_direct_cnt.setVisible(False)   
            self.act15_direct_cnt.setVisible(False)   
            self.act15_paste.setVisible( True )
    def fn_act16_select(self,text):
        if text == '클릭':
            self.act16_gps.setVisible( True )
            self.act16_gps_btn.setVisible( True ) 
            self.act16_direct.setVisible( False )            
            self.act16_direct_cnt.setVisible(False)   
            self.act16_paste.setVisible( False ) 
        elif text == '방향키':
            self.act16_gps.setVisible( False )
            self.act16_gps_btn.setVisible( False ) 
            self.act16_direct.setVisible( True )            
            self.act16_direct_cnt.setVisible(True)   
            self.act16_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act16_gps.setVisible( False )
            self.act16_gps_btn.setVisible( False ) 
            self.act16_direct.setVisible( False )            
            self.act16_direct_cnt.setVisible(False)   
            self.act16_direct_cnt.setVisible(False)   
            self.act16_paste.setVisible( True )
    def fn_act17_select(self,text):
        if text == '클릭':
            self.act17_gps.setVisible( True )
            self.act17_gps_btn.setVisible( True ) 
            self.act17_direct.setVisible( False )            
            self.act17_direct_cnt.setVisible(False)   
            self.act17_paste.setVisible( False ) 
        elif text == '방향키':
            self.act17_gps.setVisible( False )
            self.act17_gps_btn.setVisible( False ) 
            self.act17_direct.setVisible( True )            
            self.act17_direct_cnt.setVisible(True)   
            self.act17_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act17_gps.setVisible( False )
            self.act17_gps_btn.setVisible( False ) 
            self.act17_direct.setVisible( False )            
            self.act17_direct_cnt.setVisible(False)   
            self.act17_direct_cnt.setVisible(False)   
            self.act17_paste.setVisible( True )
    def fn_act18_select(self,text):
        if text == '클릭':
            self.act18_gps.setVisible( True )
            self.act18_gps_btn.setVisible( True ) 
            self.act18_direct.setVisible( False )            
            self.act18_direct_cnt.setVisible(False)   
            self.act18_paste.setVisible( False ) 
        elif text == '방향키':
            self.act18_gps.setVisible( False )
            self.act18_gps_btn.setVisible( False ) 
            self.act18_direct.setVisible( True )            
            self.act18_direct_cnt.setVisible(True)   
            self.act18_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act18_gps.setVisible( False )
            self.act18_gps_btn.setVisible( False ) 
            self.act18_direct.setVisible( False )            
            self.act18_direct_cnt.setVisible(False)   
            self.act18_direct_cnt.setVisible(False)   
            self.act18_paste.setVisible( True )
    def fn_act19_select(self,text):
        if text == '클릭':
            self.act19_gps.setVisible( True )
            self.act19_gps_btn.setVisible( True ) 
            self.act19_direct.setVisible( False )            
            self.act19_direct_cnt.setVisible(False)   
            self.act19_paste.setVisible( False ) 
        elif text == '방향키':
            self.act19_gps.setVisible( False )
            self.act19_gps_btn.setVisible( False ) 
            self.act19_direct.setVisible( True )            
            self.act19_direct_cnt.setVisible(True)   
            self.act19_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act19_gps.setVisible( False )
            self.act19_gps_btn.setVisible( False ) 
            self.act19_direct.setVisible( False )            
            self.act19_direct_cnt.setVisible(False)   
            self.act19_direct_cnt.setVisible(False)   
            self.act19_paste.setVisible( True )
    def fn_act20_select(self,text):
        if text == '클릭':
            self.act20_gps.setVisible( True )
            self.act20_gps_btn.setVisible( True ) 
            self.act20_direct.setVisible( False )            
            self.act20_direct_cnt.setVisible(False)   
            self.act20_paste.setVisible( False ) 
        elif text == '방향키':
            self.act20_gps.setVisible( False )
            self.act20_gps_btn.setVisible( False ) 
            self.act20_direct.setVisible( True )            
            self.act20_direct_cnt.setVisible(True)   
            self.act20_paste.setVisible( False )              
        elif text == '붙여넣기':
            self.act20_gps.setVisible( False )
            self.act20_gps_btn.setVisible( False ) 
            self.act20_direct.setVisible( False )            
            self.act20_direct_cnt.setVisible(False)   
            self.act20_direct_cnt.setVisible(False)   
            self.act20_paste.setVisible( True )

    def fn_save(self):
        '''저장'''
        save_text = []
        save_text.append(
            {'div'      : 'act0' 
             , 'url'    : self.__url
             , 'file'   : self.__file_path
            }
        )        
        save_text.append(
            {'div'      : 'act1' 
             , 'yn'     : self.act1_yn.currentText()        # 사용여부
             , 'select' : self.act1_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps1_x                     # 클릭 x
             , 'y'      : self.__gps1_y                     # 클릭 y
             , 'dir'    : self.act1_direct.currentText()    # 방향
             , 'dir_cnt': self.act1_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act1_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act1_wait.text()             # 수행후 대기시간
            }
        )
        save_text.append(
            {'div'      : 'act2' 
             , 'yn'     : self.act2_yn.currentText()        # 사용여부
             , 'select' : self.act2_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps2_x                     # 클릭 x
             , 'y'      : self.__gps2_y                     # 클릭 y
             , 'dir'    : self.act2_direct.currentText()    # 방향
             , 'dir_cnt': self.act2_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act2_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act2_wait.text()             # 수행후 대기시간
            }
        )
        save_text.append(
            {'div'      : 'act3' 
             , 'yn'     : self.act3_yn.currentText()        # 사용여부
             , 'select' : self.act3_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps3_x                     # 클릭 x
             , 'y'      : self.__gps3_y                     # 클릭 y
             , 'dir'    : self.act3_direct.currentText()    # 방향
             , 'dir_cnt': self.act3_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act3_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act3_wait.text()             # 수행후 대기시간
            }
        )     
        save_text.append(
            {'div'      : 'act4' 
             , 'yn'     : self.act4_yn.currentText()        # 사용여부
             , 'select' : self.act4_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps4_x                     # 클릭 x
             , 'y'      : self.__gps4_y                     # 클릭 y
             , 'dir'    : self.act4_direct.currentText()    # 방향
             , 'dir_cnt': self.act4_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act4_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act4_wait.text()             # 수행후 대기시간
            }
        ) 
        save_text.append(
            {'div'      : 'act5' 
             , 'yn'     : self.act5_yn.currentText()        # 사용여부
             , 'select' : self.act5_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps5_x                     # 클릭 x
             , 'y'      : self.__gps5_y                     # 클릭 y
             , 'dir'    : self.act5_direct.currentText()    # 방향
             , 'dir_cnt': self.act5_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act5_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act5_wait.text()             # 수행후 대기시간
            }
        )         
        save_text.append(
            {'div'      : 'act6' 
             , 'yn'     : self.act6_yn.currentText()        # 사용여부
             , 'select' : self.act6_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps6_x                     # 클릭 x
             , 'y'      : self.__gps6_y                     # 클릭 y
             , 'dir'    : self.act6_direct.currentText()    # 방향
             , 'dir_cnt': self.act6_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act6_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act6_wait.text()             # 수행후 대기시간
            }
        )   
        save_text.append(
            {'div'      : 'act7' 
             , 'yn'     : self.act7_yn.currentText()        # 사용여부
             , 'select' : self.act7_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps7_x                     # 클릭 x
             , 'y'      : self.__gps7_y                     # 클릭 y
             , 'dir'    : self.act7_direct.currentText()    # 방향
             , 'dir_cnt': self.act7_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act7_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act7_wait.text()             # 수행후 대기시간
            }
        ) 
        save_text.append(
            {'div'      : 'act8' 
             , 'yn'     : self.act8_yn.currentText()        # 사용여부
             , 'select' : self.act8_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps8_x                     # 클릭 x
             , 'y'      : self.__gps8_y                     # 클릭 y
             , 'dir'    : self.act8_direct.currentText()    # 방향
             , 'dir_cnt': self.act8_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act8_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act8_wait.text()             # 수행후 대기시간
            }
        )
        save_text.append(
            {'div'      : 'act9' 
             , 'yn'     : self.act9_yn.currentText()        # 사용여부
             , 'select' : self.act9_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps9_x                     # 클릭 x
             , 'y'      : self.__gps9_y                     # 클릭 y
             , 'dir'    : self.act9_direct.currentText()    # 방향
             , 'dir_cnt': self.act9_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act9_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act9_wait.text()             # 수행후 대기시간
            }
        )
        save_text.append(
            {'div'      : 'act10' 
             , 'yn'     : self.act10_yn.currentText()        # 사용여부
             , 'select' : self.act10_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps10_x                     # 클릭 x
             , 'y'      : self.__gps10_y                     # 클릭 y
             , 'dir'    : self.act10_direct.currentText()    # 방향
             , 'dir_cnt': self.act10_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act10_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act10_wait.text()             # 수행후 대기시간
            }
        )   
        save_text.append(
            {'div'      : 'act11' 
             , 'yn'     : self.act11_yn.currentText()        # 사용여부
             , 'select' : self.act11_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps11_x                     # 클릭 x
             , 'y'      : self.__gps11_y                     # 클릭 y
             , 'dir'    : self.act11_direct.currentText()    # 방향
             , 'dir_cnt': self.act11_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act11_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act11_wait.text()             # 수행후 대기시간
            }
        )                                              
        save_text.append(
            {'div'      : 'act12' 
             , 'yn'     : self.act12_yn.currentText()        # 사용여부
             , 'select' : self.act12_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps12_x                     # 클릭 x
             , 'y'      : self.__gps12_y                     # 클릭 y
             , 'dir'    : self.act12_direct.currentText()    # 방향
             , 'dir_cnt': self.act12_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act12_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act12_wait.text()             # 수행후 대기시간
            }
        ) 
        save_text.append(
            {'div'      : 'act13' 
             , 'yn'     : self.act13_yn.currentText()        # 사용여부
             , 'select' : self.act13_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps13_x                     # 클릭 x
             , 'y'      : self.__gps13_y                     # 클릭 y
             , 'dir'    : self.act13_direct.currentText()    # 방향
             , 'dir_cnt': self.act13_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act13_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act13_wait.text()             # 수행후 대기시간
            }
        )     
        save_text.append(
            {'div'      : 'act14' 
             , 'yn'     : self.act14_yn.currentText()        # 사용여부
             , 'select' : self.act14_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps14_x                     # 클릭 x
             , 'y'      : self.__gps14_y                     # 클릭 y
             , 'dir'    : self.act14_direct.currentText()    # 방향
             , 'dir_cnt': self.act14_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act14_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act14_wait.text()             # 수행후 대기시간
            }
        )            
        save_text.append(
            {'div'      : 'act15' 
             , 'yn'     : self.act15_yn.currentText()        # 사용여부
             , 'select' : self.act15_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps15_x                     # 클릭 x
             , 'y'      : self.__gps15_y                     # 클릭 y
             , 'dir'    : self.act15_direct.currentText()    # 방향
             , 'dir_cnt': self.act15_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act15_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act15_wait.text()             # 수행후 대기시간
            }
        )        
        save_text.append(
            {'div'      : 'act16' 
             , 'yn'     : self.act16_yn.currentText()        # 사용여부
             , 'select' : self.act16_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps16_x                     # 클릭 x
             , 'y'      : self.__gps16_y                     # 클릭 y
             , 'dir'    : self.act16_direct.currentText()    # 방향
             , 'dir_cnt': self.act16_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act16_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act16_wait.text()             # 수행후 대기시간
            }
        ) 
        save_text.append(
            {'div'      : 'act17' 
             , 'yn'     : self.act17_yn.currentText()        # 사용여부
             , 'select' : self.act17_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps17_x                     # 클릭 x
             , 'y'      : self.__gps17_y                     # 클릭 y
             , 'dir'    : self.act17_direct.currentText()    # 방향
             , 'dir_cnt': self.act17_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act17_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act17_wait.text()             # 수행후 대기시간
            }
        ) 
        save_text.append(
            {'div'      : 'act18' 
             , 'yn'     : self.act18_yn.currentText()        # 사용여부
             , 'select' : self.act18_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps18_x                     # 클릭 x
             , 'y'      : self.__gps18_y                     # 클릭 y
             , 'dir'    : self.act18_direct.currentText()    # 방향
             , 'dir_cnt': self.act18_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act18_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act18_wait.text()             # 수행후 대기시간
            }
        )             
        save_text.append(
            {'div'      : 'act19' 
             , 'yn'     : self.act19_yn.currentText()        # 사용여부
             , 'select' : self.act19_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps19_x                     # 클릭 x
             , 'y'      : self.__gps19_y                     # 클릭 y
             , 'dir'    : self.act19_direct.currentText()    # 방향
             , 'dir_cnt': self.act19_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act19_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act19_wait.text()             # 수행후 대기시간
            }
        )    
        save_text.append(
            {'div'      : 'act20' 
             , 'yn'     : self.act20_yn.currentText()        # 사용여부
             , 'select' : self.act20_select.currentText()    # 행동 (클릭 , 방향 , 붙여)
             , 'x'      : self.__gps20_x                     # 클릭 x
             , 'y'      : self.__gps20_y                     # 클릭 y
             , 'dir'    : self.act20_direct.currentText()    # 방향
             , 'dir_cnt': self.act20_direct_cnt.text()       # 방향 횟수
             , 'paste'  : self.act20_paste.currentText()     #붙여넣기 행번호
             , 'wait'   : self.act20_wait.text()             # 수행후 대기시간
            }
        )                           
        # 메인 데이터 생성
        self.__load_date = save_text

        file_name = self.save_file_nm.text().replace(' ','')
        if file_name == '':
            QMessageBox.about(self,'About Title','파일이름이 없습니다. ')
        else :
            QMessageBox.about(self,'About Title','파일명 "{0}" 저장합니다. '.format( file_name ) )
            with open('c:\\ncnc_class\\'+file_name+'.pickle',"wb") as f:
                pickle.dump(save_text, f) # 위에서 생성한 리스트를 list.pickle로 저장  
            

    
    def fn_load(self):
        '''피클 파일 불러오기'''
        file_nm = self.load_cb.currentText()  
        file_path = 'C:\\ncnc_class\\{}{}'.format( file_nm ,'.pickle')
        self.save_file_nm.setText( file_nm )

        _load_data = []
        with open(file_path, 'rb') as f:
            _load_data = pickle.load(f)
        
        self.__load_date = _load_data

        for i in self.__load_date :
            print( i )
            if i['div'] =='act0':
                '''url 및 파일 정보.'''
                self.url_qe.setText( i['url'] )
                self.__url = self.url_qe.text() 
                self.__driver.get( self.__url )       

                self.__file_path = i['file']
                self.file_lb.setText( self.__file_path )                     
            elif i['div'] =='act1':
                self.act1_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act1_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act1_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act1_select.setCurrentIndex( 2 )  
                self.fn_act1_select( i['select'] )              
                self.__gps1_x = i['x']
                self.__gps1_y = i['y']
                self.act1_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps1_x , self.__gps1_y) )
                if i['dir'] == '상':
                    self.act1_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act1_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act1_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act1_direct.setCurrentIndex( 3 )
                
                self.act1_direct_cnt.setText( i['dir_cnt'] )                
                self.act1_paste.setCurrentIndex( int(i['paste']) )
                self.act1_wait.setText( i['wait'] )
            elif i['div'] =='act2':
                self.act2_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act2_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act2_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act2_select.setCurrentIndex( 2 )  
                self.fn_act2_select( i['select'] )              
                self.__gps2_x = i['x']
                self.__gps2_y = i['y']
                self.act2_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps2_x , self.__gps2_y) )
                if i['dir'] == '상':
                    self.act2_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act2_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act2_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act2_direct.setCurrentIndex( 3 )
                
                self.act2_direct_cnt.setText( i['dir_cnt'] )                
                self.act2_paste.setCurrentIndex( int(i['paste']) )
                self.act2_wait.setText( i['wait'] )      
            elif i['div'] =='act3':
                self.act3_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act3_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act3_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act3_select.setCurrentIndex( 2 )  
                self.fn_act3_select( i['select'] )              
                self.__gps3_x = i['x']
                self.__gps3_y = i['y']
                self.act3_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps3_x , self.__gps3_y) )
                if i['dir'] == '상':
                    self.act3_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act3_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act3_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act3_direct.setCurrentIndex( 3 )
                
                self.act3_direct_cnt.setText( i['dir_cnt'] )                
                self.act3_paste.setCurrentIndex( int(i['paste']) )
                self.act3_wait.setText( i['wait'] )                          
            elif i['div'] =='act4':
                self.act4_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act4_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act4_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act4_select.setCurrentIndex( 2 )  
                self.fn_act4_select( i['select'] )              
                self.__gps4_x = i['x']
                self.__gps4_y = i['y']
                self.act4_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps4_x , self.__gps4_y) )
                if i['dir'] == '상':
                    self.act4_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act4_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act4_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act4_direct.setCurrentIndex( 3 )
                
                self.act4_direct_cnt.setText( i['dir_cnt'] )                
                self.act4_paste.setCurrentIndex( int(i['paste']) )
                self.act4_wait.setText( i['wait'] )                
            elif i['div'] =='act5':
                self.act5_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act5_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act5_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act5_select.setCurrentIndex( 2 )  
                self.fn_act5_select( i['select'] )              
                self.__gps5_x = i['x']
                self.__gps5_y = i['y']
                self.act5_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps5_x , self.__gps5_y) )
                if i['dir'] == '상':
                    self.act5_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act5_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act5_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act5_direct.setCurrentIndex( 3 )
                
                self.act5_direct_cnt.setText( i['dir_cnt'] )                
                self.act5_paste.setCurrentIndex( int(i['paste']) )
                self.act5_wait.setText( i['wait'] )
            elif i['div'] =='act6':
                self.act6_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act6_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act6_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act6_select.setCurrentIndex( 2 )  
                self.fn_act6_select( i['select'] )              
                self.__gps6_x = i['x']
                self.__gps6_y = i['y']
                self.act6_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps6_x , self.__gps6_y) )
                if i['dir'] == '상':
                    self.act6_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act6_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act6_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act6_direct.setCurrentIndex( 3 )
                
                self.act6_direct_cnt.setText( i['dir_cnt'] )                
                self.act6_paste.setCurrentIndex( int(i['paste']) )
                self.act6_wait.setText( i['wait'] )                
            elif i['div'] =='act7':
                self.act7_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act7_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act7_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act7_select.setCurrentIndex( 2 )  
                self.fn_act7_select( i['select'] )              
                self.__gps7_x = i['x']
                self.__gps7_y = i['y']
                self.act7_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps7_x , self.__gps7_y) )
                if i['dir'] == '상':
                    self.act7_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act7_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act7_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act7_direct.setCurrentIndex( 3 )
                
                self.act7_direct_cnt.setText( i['dir_cnt'] )                
                self.act7_paste.setCurrentIndex( int(i['paste']) )
                self.act7_wait.setText( i['wait'] )
            elif i['div'] =='act8':
                self.act8_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act8_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act8_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act8_select.setCurrentIndex( 2 )  
                self.fn_act8_select( i['select'] )              
                self.__gps8_x = i['x']
                self.__gps8_y = i['y']
                self.act8_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps8_x , self.__gps8_y) )
                if i['dir'] == '상':
                    self.act8_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act8_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act8_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act8_direct.setCurrentIndex( 3 )
                
                self.act8_direct_cnt.setText( i['dir_cnt'] )                
                self.act8_paste.setCurrentIndex( int(i['paste']) )
                self.act8_wait.setText( i['wait'] )
            elif i['div'] =='act9':
                self.act9_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act9_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act9_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act9_select.setCurrentIndex( 2 )  
                self.fn_act9_select( i['select'] )              
                self.__gps9_x = i['x']
                self.__gps9_y = i['y']
                self.act9_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps9_x , self.__gps9_y) )
                if i['dir'] == '상':
                    self.act9_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act9_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act9_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act9_direct.setCurrentIndex( 3 )
                
                self.act9_direct_cnt.setText( i['dir_cnt'] )                
                self.act9_paste.setCurrentIndex( int(i['paste']) )
                self.act9_wait.setText( i['wait'] )                
            elif i['div'] =='act10':
                self.act10_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act10_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act10_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act10_select.setCurrentIndex( 2 )  
                self.fn_act10_select( i['select'] )              
                self.__gps10_x = i['x']
                self.__gps10_y = i['y']
                self.act10_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps10_x , self.__gps10_y) )
                if i['dir'] == '상':
                    self.act10_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act10_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act10_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act10_direct.setCurrentIndex( 3 )
                
                self.act10_direct_cnt.setText( i['dir_cnt'] )                
                self.act10_paste.setCurrentIndex( int(i['paste']) )
                self.act10_wait.setText( i['wait'] )
            elif i['div'] =='act11':
                self.act11_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act11_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act11_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act11_select.setCurrentIndex( 2 )  
                self.fn_act11_select( i['select'] )              
                self.__gps11_x = i['x']
                self.__gps11_y = i['y']
                self.act11_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps11_x , self.__gps11_y) )
                if i['dir'] == '상':
                    self.act11_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act11_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act11_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act11_direct.setCurrentIndex( 3 )
                
                self.act11_direct_cnt.setText( i['dir_cnt'] )                
                self.act11_paste.setCurrentIndex( int(i['paste']) )
                self.act11_wait.setText( i['wait'] )
            elif i['div'] =='act12':
                self.act12_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act12_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act12_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act12_select.setCurrentIndex( 2 )  
                self.fn_act12_select( i['select'] )              
                self.__gps12_x = i['x']
                self.__gps12_y = i['y']
                self.act12_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps12_x , self.__gps12_y) )
                if i['dir'] == '상':
                    self.act12_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act12_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act12_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act12_direct.setCurrentIndex( 3 )
                
                self.act12_direct_cnt.setText( i['dir_cnt'] )                
                self.act12_paste.setCurrentIndex( int(i['paste']) )
                self.act12_wait.setText( i['wait'] )
            elif i['div'] =='act13':
                self.act13_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act13_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act13_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act13_select.setCurrentIndex( 2 )  
                self.fn_act13_select( i['select'] )              
                self.__gps13_x = i['x']
                self.__gps13_y = i['y']
                self.act13_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps13_x , self.__gps13_y) )
                if i['dir'] == '상':
                    self.act13_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act13_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act13_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act13_direct.setCurrentIndex( 3 )
                
                self.act13_direct_cnt.setText( i['dir_cnt'] )                
                self.act13_paste.setCurrentIndex( int(i['paste']) )
                self.act13_wait.setText( i['wait'] )                
            elif i['div'] =='act14':
                self.act14_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act14_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act14_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act14_select.setCurrentIndex( 2 )  
                self.fn_act14_select( i['select'] )              
                self.__gps14_x = i['x']
                self.__gps14_y = i['y']
                self.act14_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps14_x , self.__gps14_y) )
                if i['dir'] == '상':
                    self.act14_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act14_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act14_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act14_direct.setCurrentIndex( 3 )
                
                self.act14_direct_cnt.setText( i['dir_cnt'] )                
                self.act14_paste.setCurrentIndex( int(i['paste']) )
                self.act14_wait.setText( i['wait'] )        
            elif i['div'] =='act15':
                self.act15_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act15_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act15_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act15_select.setCurrentIndex( 2 )  
                self.fn_act15_select( i['select'] )              
                self.__gps15_x = i['x']
                self.__gps15_y = i['y']
                self.act15_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps15_x , self.__gps15_y) )
                if i['dir'] == '상':
                    self.act15_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act15_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act15_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act15_direct.setCurrentIndex( 3 )
                
                self.act15_direct_cnt.setText( i['dir_cnt'] )                
                self.act15_paste.setCurrentIndex( int(i['paste']) )
                self.act15_wait.setText( i['wait'] )        
            elif i['div'] =='act16':
                self.act16_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act16_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act16_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act16_select.setCurrentIndex( 2 )  
                self.fn_act16_select( i['select'] )              
                self.__gps16_x = i['x']
                self.__gps16_y = i['y']
                self.act16_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps16_x , self.__gps16_y) )
                if i['dir'] == '상':
                    self.act16_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act16_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act16_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act16_direct.setCurrentIndex( 3 )
                
                self.act16_direct_cnt.setText( i['dir_cnt'] )                
                self.act16_paste.setCurrentIndex( int(i['paste']) )
                self.act16_wait.setText( i['wait'] )
            elif i['div'] =='act17':
                self.act17_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act17_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act17_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act17_select.setCurrentIndex( 2 )  
                self.fn_act17_select( i['select'] )              
                self.__gps17_x = i['x']
                self.__gps17_y = i['y']
                self.act17_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps17_x , self.__gps17_y) )
                if i['dir'] == '상':
                    self.act17_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act17_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act17_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act17_direct.setCurrentIndex( 3 )
                
                self.act17_direct_cnt.setText( i['dir_cnt'] )                
                self.act17_paste.setCurrentIndex( int(i['paste']) )
                self.act17_wait.setText( i['wait'] )
            elif i['div'] =='act18':
                self.act18_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act18_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act18_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act18_select.setCurrentIndex( 2 )  
                self.fn_act18_select( i['select'] )              
                self.__gps18_x = i['x']
                self.__gps18_y = i['y']
                self.act18_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps18_x , self.__gps18_y) )
                if i['dir'] == '상':
                    self.act18_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act18_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act18_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act18_direct.setCurrentIndex( 3 )
                
                self.act18_direct_cnt.setText( i['dir_cnt'] )                
                self.act18_paste.setCurrentIndex( int(i['paste']) )
                self.act18_wait.setText( i['wait'] )
            elif i['div'] =='act19':
                self.act19_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act19_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act19_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act19_select.setCurrentIndex( 2 )  
                self.fn_act19_select( i['select'] )              
                self.__gps19_x = i['x']
                self.__gps19_y = i['y']
                self.act19_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps19_x , self.__gps19_y) )
                if i['dir'] == '상':
                    self.act19_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act19_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act19_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act19_direct.setCurrentIndex( 3 )
                
                self.act19_direct_cnt.setText( i['dir_cnt'] )                
                self.act19_paste.setCurrentIndex( int(i['paste']) )
                self.act19_wait.setText( i['wait'] )                
            elif i['div'] =='act20':
                self.act20_yn.setCurrentIndex( 1 if i['yn'] == 'Y' else 0 )
                if i['select'] == '클릭':                    
                    self.act20_select.setCurrentIndex( 0 )
                elif i['select'] == '방향키':                    
                    self.act20_select.setCurrentIndex( 1 )
                elif i['select'] == '붙여넣기':                    
                    self.act20_select.setCurrentIndex( 2 )  
                self.fn_act20_select( i['select'] )              
                self.__gps20_x = i['x']
                self.__gps20_y = i['y']
                self.act20_gps.setText( '( x : {0} , y : {1} )'.format(self.__gps20_x , self.__gps20_y) )
                if i['dir'] == '상':
                    self.act20_direct.setCurrentIndex( 0 )
                elif i['dir'] == '하':
                    self.act20_direct.setCurrentIndex( 1 )
                elif i['dir'] == '좌':
                    self.act20_direct.setCurrentIndex( 2 )
                elif i['dir'] == '우':
                    self.act20_direct.setCurrentIndex( 3 )
                
                self.act20_direct_cnt.setText( i['dir_cnt'] )                
                self.act20_paste.setCurrentIndex( int(i['paste']) )
                self.act20_wait.setText( i['wait'] )

        

    def getfolelist(self):    
        '''덤프 파일 정보 가져오기.'''
        _path = 'C:\\ncnc_class\\'
        __list = os.listdir( _path )    
        list = []
        for i in __list:
            if i.find( 'pickle' ) != -1 :
                list.append(i.replace('.pickle',''))
        return list

    
    def fn_start_stop(self):
        '''시작/정지'''
        csv_data = self.readfile( self.__file_path )

        if self.__start_stop == 'stop' :
            self.__start_stop = 'start'
            self.__work = Work()
            self.__work.fn_param( self.__load_date , csv_data , self.__url )
            self.__work.start()
            self.__driver.close()
        else:
            re = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?", QMessageBox.Yes|QMessageBox.No)
            if re == QMessageBox.Yes:
                self.__start_stop = 'stop'
                self.__work.stop()
                self.setBr()
                self.setURL()
                



                        

    
    def fn_close(self):
        super().close()

    def fileopen(self):
        '''CSV로드'''
        try:        
            fname = QFileDialog.getOpenFileName(self)
            _nm = fname[0]            
            self.__file_path = _nm
            self.file_lb.setText( self.__file_path )
        except Exception as e:
            print('def fileopen',e)   

    def readfile(self , path):
        '''파일 읽기'''
        _rt = []
        f = open(path , 'r', encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            _rt.append( line )
        f.close()    
        return _rt  
    
    def setURL(self):
        '''url 로드하기'''
        self.__url = self.url_qe.text() 
        self.__driver.get( self.__url )

    def setBr(self):
        '''브라우저 초기화'''
        chrome_options = Options()
        chrome_options.add_argument('window-size=512x1080')
        chrome_options.add_argument('--incognito')
        self.__driver = webdriver.Chrome( options= chrome_options )



if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = mk_macro()
   sys.exit(app.exec_())
