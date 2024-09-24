import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pyautogui
import pyperclip
import csv
import pickle
import time
import random
from datetime import datetime
from pytz import timezone
from PIL import ImageGrab , Image
import lib.util as w2ji



class Work(QThread):
    __url_xy            = () # url 클릭 좌표
    __url_xy_wait       = 0.5 # 0.5 초 기본 대기 url 클릭후 대기
    __url_path          = '' #url 주소
    __url_path_wait     = 2 # 2초 기본 대기 url 주소 입력후 대기시간
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

    __power = False

    def __init__(self ):
        super().__init__()
        self.__power = True     # run 매소드 루프 플래그

    def fn_param(self , url_xy,url_xy_wait,url_path,url_path_wait,cvs_path,div,click_xy,click_evn,click_rand,click_xy_wait,key0,key0_wait,key1,key1_wait,csv_data ):
        self.__url_xy            = url_xy           # url 클릭 좌표
        self.__url_xy_wait       = url_xy_wait      # 0.5 초 기본 대기 url 클릭후 대기
        self.__url_path          = url_path         #url 주소
        self.__url_path_wait     = url_path_wait    # 2초 기본 대기 url 주소 입력후 대기시간
        self.__cvs_path          = cvs_path         # cvs 파일 위치
        self.__div               = div              #선택값    
        self.__click_xy          = click_xy         #클릭    
        self.__click_evn         = click_evn        #클릭   복사 컬럼 위치 선택후 붙여넣기
        self.__click_rand        = click_rand       #랜덤클릭
        self.__click_xy_wait     = click_xy_wait    #클릭 실행후 대기시간    
        self.__key0              = key0             # 키보드0 단일키 하나
        self.__key0_wait         = key0_wait        # 키보드0 대기
        self.__key1              = key1             # 키보드1 복합키 두개 - hot key 하기
        self.__key1_wait         = key1_wait        # 키보드1 대기 
        self.__csv_data          = csv_data         # 데이터 파일

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
        time.sleep( wait_time )         
    
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
    
    def run(self):
        '''매크로 시작'''
        try:
            for j in self.__csv_data:
                if self.__power == True:
                    self.fnclick( self.__url_xy , self.__url_xy_wait ) #클릭
                    self.fnUrl( self.__url_path , self.__url_path_wait ) #url 처리                    
                    _j = j            
                    print('*'*100)                                
                    print('처리 데이터 : ', _j)
                    print('*'*100)                            
                    for i in self.__div:                         
                        xy          = self.fnArrayGet( self.__click_xy , i )            
                        evn         = self.fnArrayGet( self.__click_evn , i )
                        rand        = self.fnArrayGet( self.__click_rand , i )
                        xy_wait     = self.fnArrayGet( self.__click_xy_wait , i )
                        key0        = self.fnArrayGet( self.__key0 , i )
                        key0_wait   = self.fnArrayGet( self.__key0_wait , i )
                        key1        = self.fnArrayGet( self.__key1 , i )
                        key1_wait   = self.fnArrayGet( self.__key1_wait , i )      
                        print('\t 행번호 : ', i ,' , 작업구분 : ', self.__div.get(i) )                        
                        if (self.__div.get(i) == '끝') :
                            # 스샷찍은후 종료
                            try:
                                base_dttm   = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d_%H%M%S')
                                base_dt     = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
                                try:
                                    os.mkdir('c:\\ncnc_class\\screenshot\\{}'.format(base_dt))
                                except Exception as e:
                                    '''폴더 생성 있으면 넘어간다.'''
                                file_nm     = base_dttm+'_'+str(_j[0])
                                img         = ImageGrab.grab()
                                imgCrop     = img.crop()
                                file_name   = 'c:\\ncnc_class\\screenshot\\{}\\{}{}'.format( base_dt,file_nm ,'.png')
                                imgCrop.save(file_name)
                                print('\t 파일명 : ' , file_nm )
                            except Exception as e:
                                print('mk_image : ',e) 

                            break

                        elif (self.__div.get(i) == '클릭') and ( self.__power == True ):
                            #print(evn , type(evn))                
                            for j in range(0, int(evn)): #반복 실행한다.
                                self.fnclick( xy , 0.5 ) #클릭
                            time.sleep( float(xy_wait) ) #대기
                        elif (self.__div.get(i) == '붙여넣기') and ( self.__power == True ):
                            self.fnclick( xy , 0.5 ) #클릭
                            n = int(evn)                    
                            self.fnpaste( _j[n] ) # 붙여넣기
                            time.sleep( float(xy_wait) ) #대기
                        elif (self.__div.get(i) == '글씨쓰기') and ( self.__power == True ):
                            self.fnclick( xy , 0.5 ) #클릭
                            n = int(evn)                    
                            self.fnwrite( _j[n] ) #타이핑
                            time.sleep( float(xy_wait) ) #대기
                        elif (self.__div.get(i) == '선택하기') and ( self.__power == True ):
                            self.fnclick( xy , 0.5 ) #클릭
                            r = random.randrange(0,3)
                            r0 = rand.get(0)
                            r1 = rand.get(1)
                            r2 = rand.get(2)
                            r3 = rand.get(3)
                            # print( r , r0 , r1 , r2 , r3 )
                            if r == 0:
                                self.fnclick( r0 , 0.5 ) #클릭   
                            elif r == 1:
                                self.fnclick( r1 , 0.5 ) #클릭   
                            elif r == 2:
                                self.fnclick( r2 , 0.5 ) #클릭   
                            elif r == 3:
                                self.fnclick( r3 , 0.5 ) #클릭   
                            time.sleep( float(xy_wait) ) #대기
                        elif (self.__div.get(i) == '중복선택') and ( self.__power == True ):
                            self.fnclick( xy , 0.5 ) #클릭   
                            r0 = rand.get(0)
                            r1 = rand.get(1)
                            r2 = rand.get(2)
                            r3 = rand.get(3)                                            
                            self.fnclick( r0 , 0.5 ) #클릭                           
                            self.fnclick( r1 , 0.5 ) #클릭   
                            self.fnclick( r2 , 0.5 ) #클릭                           
                            self.fnclick( r3 , 0.5 ) #클릭   
                            time.sleep( float(xy_wait) ) #대기 

                        elif (self.__div.get(i) == '방향전환') and ( self.__power == True ):
                            self.fnclick( xy , 0.1 ) #클릭                        
                            self.fnkey( key0 , int(key0_wait) )                        
                            time.sleep( float(xy_wait) ) #대기
                        elif (self.__div.get(i) == '무시') and ( self.__power == True ):
                            '''행동 없음.'''
                        elif (self.__div.get(i) == '캡쳐') and ( self.__power == True ):
                            '''캡쳐'''
                            #print('캡쳐'*10)
                            r11 = rand.get(11)
                            r12 = rand.get(12)
                            capture_width   = r12.x - r11.x
                            capture_height  = r12.y - r11.y
                            #print(r11 , r12)
                            #print(r11.x , r12.y , capture_width , capture_height)

                            base_dttm   = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d_%H%M%S')
                            base_dt     = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
                            try:
                                os.mkdir('c:\\ncnc_class\\capture\\{}'.format(base_dt))
                            except Exception as e:
                                '''폴더 생성 있으면 넘어간다.''' 
                            file_nm     = base_dttm+'_'+str(_j[0])
                            file_name   = r"c:\\ncnc_class\\capture\\{}\\{}{}".format( base_dt,file_nm ,'.png') 
                            pyautogui.screenshot( file_name , region=(r11.x , r11.y , capture_width, capture_height))    
                            time.sleep( float(xy_wait) ) #대기

        except Exception as e:
            print('*'*50)
            print('정지 합니다. error 발생 : ',e)                                        
            self.__power = False
        
        if self.__power == True:
            w2ji.send_telegram_message( 'mk_macro_ver2 가 완료 되었습니다.' )
            pyautogui.alert('완료 되었습니다.')
            
        else :
            pyautogui.alert('정지 되었습니다.')
                    
  
        

    def stop(self):
        # 멀티쓰레드를 종료하는 메소드
        print('stop ','*'*50)
        self.__power = False


class MyApp(QWidget):
    __lb_style = 'border-radius: 5px;border: 1px solid gray;'
    __lb_style2 = 'border-radius: 5px;border: 1px solid red;'
    #__gridlayout = 'padding: 0px;'

    __x         = 1024
    __work      = Work()
    __max_obj   = 451

    
    __url_xy            = () # url 클릭 좌표
    __url_xy_wait       = 0.5 # 0.5 초 기본 대기 url 클릭후 대기
    __url_path          = '' #url 주소
    __url_path_wait     = 2 # 2초 기본 대기 url 주소 입력후 대기시간
    __cvs_path          = '' # cvs 파일 위치
    __div               = {} #선택값        
    __click_xy          = {} #클릭    
    __click_evn         = {} #클릭   복사 컬럼 위치 선택후 붙여넣기

    for i in range(0,__max_obj):
        __div[i]        = '끝'
        __click_evn[i]  = '1'

    __click_rand        = {} #랜덤클릭
    __click_xy_wait     = {} #클릭 실행후 대기시간    
    __key0              = {} # 키보드0 단일키 하나
    __key0_wait         = {} # 키보드0 대기
    __key1              = {} # 키보드1 복합키 두개 - hot key 하기
    __key1_wait         = {} # 키보드1 대기

    # 임시 시작
    __pos               = -1 # 임시 배열번호 
    __sub_pos           = -1 # 임시 배열번호 랜덤 좌표를 위한   
    __temp_rand         = {} # 랜덤 클릭값 4개 저장해야 한다.
    __file_nm           = '' # 파일이름
    # 임시 종료

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMinimumHeight(800)
        self.setGeometry(self.__x, 30, 712, 800)
        self.show()
    
    def fnLoad(self):        
        '''데이터 불러오기시 동작'''         
        super().__init__()
        self.__x += 100
        self.initUI()      
        self.setMinimumHeight(800)
        self.setGeometry(self.__x, 30, 712, 800)
        self.show()
          

    def initUI(self):

        self.pane = QWidget()
        self.view = QScrollArea()
        self.view.setWidget(self.pane)
        self.view.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget( self.head() )
        layout.addWidget( self.foot() )
        layout.addWidget(self.view)
        layout = QVBoxLayout(self.pane)        
        layout.addWidget( self.body() )
        self.setWindowTitle('매크로 version 2')

    def keyPressEvent(self, e):
        '''f 키를 클릭하면 좌표 값 __click_xy에 넣는다'''
        if e.key() == Qt.Key_Escape:
            '''esc 하면 정리'''
            self.__work.stop()
        if e.key() == Qt.Key_F:
            xy = pyautogui.position()
            #print( '*'*50 )
            #print( self.__pos , self.__sub_pos ,  xy )
            #print( '*'*50 )
            if (self.__pos == 999) and (self.__sub_pos == -1) :
                self.__url_xy = xy
                

            elif (self.__pos != -1) and (self.__sub_pos == -1) :                
                self.__click_xy[self.__pos] = xy
            
            if self.__sub_pos != -1:
                
                self.__temp_rand[ self.__sub_pos ] = xy
            
            self.__pos      = -1 # 한번만 할당하도록 설정한다. 
            self.__sub_pos  = -1 # 한번만 할당하도록 설정한다.           
            #print('ffeeff', self.__pos, xy , ' , url_xy : ' , self.__url_xy , ' , click_xy : ' , self.__click_xy)     
        
        

    def head( self ):
        groupbox = QGroupBox('')       
        grid = QGridLayout()
        grid.setSpacing(0)
        
        # URL 지정
        url_lb = QLabel('1. URL')         

        url_xy = QLabel('( x : {0} , y : {1} )'.format( 0 , 0 ) )
        url_xy.setStyleSheet( self.__lb_style  )
        if len(self.__url_xy) != 0:
            url_xy.setText( '(x:{0} , y:{1})'.format(self.__url_xy.x , self.__url_xy.y) )
        

        def fn_geo( ):
            '''좌표할당 행번호 지정'''
            self.__pos = 999


        url_xy_btn = QPushButton('좌표지정')
        url_xy_btn.clicked.connect( fn_geo )
                 

        url_qe = QLineEdit()
        url_qe.setStyleSheet( self.__lb_style )
        url_qe.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        if len(self.__url_path) !=0:
            url_qe.setText( self.__url_path )            

        def fn_cmp():
            '''각 절의 완료 처리'''
            self.__url_path = url_qe.text()
            if len(self.__url_xy) != 0:
                url_xy.setText( '(x:{0} , y:{1})'.format(self.__url_xy.x , self.__url_xy.y) )

        url_btn = QPushButton('적용')
        url_btn.clicked.connect( fn_cmp )  

        grid.addWidget(url_lb  , 0 , 0)
        grid.addWidget( url_xy  , 0 , 1)
        grid.addWidget(url_xy_btn  , 0 , 2)  

        grid.addWidget(url_qe  , 0 , 3)
        grid.addWidget(url_btn , 0 , 4)        
        
        # 1. 파일 로드
        file_lb = QLabel('2. CSV')

        csv_lb = QLabel()
        csv_lb.setStyleSheet( self.__lb_style )
        csv_lb.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)          

        def fileopen():
            '''CSV로드'''
            try:        
                fname = QFileDialog.getOpenFileName()
                _nm = fname[0]            
                self.__cvs_path = _nm
                csv_lb.setText( self.__cvs_path )
            except Exception as e:
                print('def fileopen',e)  
        filebtn = QPushButton('Load')        
        filebtn.clicked.connect( fileopen )  
        if len(self.__cvs_path) != 0:
            csv_lb.setText( self.__cvs_path )

        grid.addWidget(file_lb  , 1 , 0)
        grid.addWidget(csv_lb   , 1 , 1 , 1 , 3)
        grid.addWidget(filebtn  , 1 , 4)     
        groupbox.setFixedHeight(70)
        groupbox.setLayout( grid )  
        return groupbox


    def body(self):               
        groupbox = QGroupBox('')        
        vbox = QVBoxLayout()
        vbox.setSpacing(0)        
        for i in range( 0, self.__max_obj  ): # 0~20까지
            vbox.addWidget(self.exec_obj(i))
        groupbox.setLayout(vbox)
        return groupbox
    
    
    def exec_obj(self , pos ):
        '''반복객체 
            pos : 데이터 배열의 순번
        '''
        def fn_div( str ):
            '''행동 클릭 이벤트'''
            if (str == '끝') or (str == '무시'):                
                geo_btn.setVisible( False )
                col.setVisible( False )
                geo_xy_wait.setVisible( False )
                cmp_btn.setVisible( False )
                ran_btn0.setVisible( False )
                ran_btn1.setVisible( False )
                ran_btn2.setVisible( False )
                ran_btn3.setVisible( False )
                key0.setVisible( False )
                key0_wait.setVisible( False )
                cap_bnt0.setVisible( False )
                cap_bnt1.setVisible( False )
            elif (str == '클릭') or (str == '붙여넣기') or (str == '글씨쓰기'):
                geo_btn.setVisible( True )
                col.setVisible(True)
                ran_btn0.setVisible( False )
                ran_btn1.setVisible( False )
                ran_btn2.setVisible( False )
                ran_btn3.setVisible( False )                
                key0.setVisible( False )
                key0_wait.setVisible( False )
                geo_xy_wait.setVisible( True )
                cmp_btn.setVisible( True )
                cap_bnt0.setVisible( False )
                cap_bnt1.setVisible( False )
            elif (str == '선택하기') or ( str == '중복선택' ):
                geo_btn.setVisible( True )
                col.setVisible(False)
                geo_xy_wait.setVisible( True )                
                ran_btn0.setVisible( True )
                ran_btn1.setVisible( True )
                ran_btn2.setVisible( True )
                ran_btn3.setVisible( True )   
                key0.setVisible( False )
                key0_wait.setVisible( False )
                cmp_btn.setVisible( True )
                cap_bnt0.setVisible( False )
                cap_bnt1.setVisible( False )
            elif str =='방향전환':
                geo_btn.setVisible( True )
                col.setVisible(False)                              
                ran_btn0.setVisible( False )
                ran_btn1.setVisible( False )
                ran_btn2.setVisible( False )
                ran_btn3.setVisible( False )   
                key0.setVisible( True )
                key0_wait.setVisible( True )
                geo_xy_wait.setVisible( True )  
                cmp_btn.setVisible( True )
                cap_bnt0.setVisible( False )
                cap_bnt1.setVisible( False )
            elif str == '캡쳐':
                geo_btn.setVisible( False )
                col.setVisible(False)                              
                ran_btn0.setVisible( False )
                ran_btn1.setVisible( False )
                ran_btn2.setVisible( False )
                ran_btn3.setVisible( False )   
                key0.setVisible( False )
                key0_wait.setVisible( False )
                geo_xy_wait.setVisible( True )  
                cmp_btn.setVisible( True )
                cap_bnt0.setVisible( True )
                cap_bnt1.setVisible( True )
                
            fn_cmp()

        def fn_geo():
             '''좌표할당 행번호 지정'''
             self.__pos = pos

        def fn_geo2( number ):
             '''좌표할당 행번호 지정'''
             self.__pos = pos
             self.__sub_pos = number
             if self.__click_rand.get(pos) != None:
                # 랜던값이 있다면 넣고 시작한다.
                self.__temp_rand = self.__click_rand.get(pos)

        groupbox = QGroupBox('')        
        hbox = QHBoxLayout()
        hbox.setSpacing(0)     

        row_seq = QLabel( str(pos)+' : '   ) 
        hbox.addWidget( row_seq )

        div = QComboBox()
        div.addItems(['끝','클릭','붙여넣기','글씨쓰기','선택하기','중복선택','방향전환','무시','캡쳐' ])      # ,'키보드-1' 추후 수정
        div.activated[str].connect( fn_div )   
        hbox.addWidget( div )

        # 클릭 좌표 설정 버튼
        geo_btn = QPushButton('좌표지정')
        geo_btn.clicked.connect(    fn_geo   )
        geo_btn.setVisible( False )
        hbox.addWidget( geo_btn )

        # 클릭후 이벤트 ( 클릭-0 : 클릭횟수 , 클릭-1 : 복사붙여넣기 컬럼위치 , 클릭-2 : 타이핑 컬럼위치 , 클릭-3 : 랜덤클릭 , 키보드-1  )
        col = QComboBox()
        col.addItems(['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39'])                
        col.setCurrentText('1')
        col.setVisible( False )
        col.setFixedWidth(70)
        hbox.addWidget( col )     

        ran_btn0 = QPushButton('좌표0')
        ran_btn0.clicked.connect(   lambda : fn_geo2(0)   )
        ran_btn0.setVisible( False )
        hbox.addWidget( ran_btn0 )  

        ran_btn1 = QPushButton('좌표1')
        ran_btn1.clicked.connect(    lambda : fn_geo2(1)   )
        ran_btn1.setVisible( False )
        hbox.addWidget( ran_btn1 )                  

        ran_btn2 = QPushButton('좌표2')
        ran_btn2.clicked.connect(    lambda : fn_geo2(2)   )
        ran_btn2.setVisible( False )
        hbox.addWidget( ran_btn2 )                          

        ran_btn3 = QPushButton('좌표3')
        ran_btn3.clicked.connect(    lambda : fn_geo2(3)   )
        ran_btn3.setVisible( False )
        hbox.addWidget( ran_btn3 )      

        key0 = QComboBox()
        key0.addItems(['pagedown','pageup','up','down','left','right','enter', 'del', 'delete','backspace','space'])        
        key0.setVisible( False )
        hbox.addWidget( key0 )  

        #캡쳐의 시작점
        cap_bnt0 = QPushButton('시작점')
        cap_bnt0.clicked.connect(   lambda : fn_geo2(11)   )
        cap_bnt0.setVisible( False )
        hbox.addWidget( cap_bnt0 )  
        #캡쳐의 끝점
        cap_bnt1 = QPushButton('끝점')
        cap_bnt1.clicked.connect(    lambda : fn_geo2(12)   )
        cap_bnt1.setVisible( False )
        hbox.addWidget( cap_bnt1 )  



        # 클릭 의 대기시간
        key0_wait = QLineEdit()     
        key0_wait.setStyleSheet( self.__lb_style2 )
        key0_wait.setText('1')      
        key0_wait.setFixedWidth(50)
        key0_wait.setVisible( False )
        hbox.addWidget( key0_wait )

        # 클릭 의 대기시간
        geo_xy_wait = QLineEdit()     
        geo_xy_wait.setStyleSheet( self.__lb_style )
        geo_xy_wait.setText('1.0')      
        geo_xy_wait.setFixedWidth(50)
        geo_xy_wait.setVisible( False )
        hbox.addWidget( geo_xy_wait )                  



        def fn_cmp():
            '''각 절의 완료 처리'''
            self.__div[pos] = div.currentText()
            #print(self.__div)    

            #print( '??? ',self.__click_rand[pos] )        
            
            if self.__click_xy.get(pos) != None:
                geo_btn.setText( '(x:{0},y:{1})'.format(self.__click_xy[pos].x , self.__click_xy[pos].y) )                           
            
            self.__click_evn[pos] = col.currentText()
            self.__click_xy_wait[pos] = geo_xy_wait.text()
            self.__key0[pos] = key0.currentText()
            self.__key0_wait[pos] = key0_wait.text()
            
            if len( self.__temp_rand ) != 0:
                # 피클로드시 오류 발생
                self.__click_rand[pos]  = self.__temp_rand
                self.__temp_rand = {} #초기화

            if self.__click_rand.get(pos) != None:
                #print('*'*10)
                #print( self.__click_rand[pos] )

                print('*'*10)
                '''랜덤 버튼 정의 값 저장'''
                if self.__click_rand[pos].get(0) != None:                    
                    ran_btn0.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][0].x , self.__click_rand[pos][0].y) )
                if self.__click_rand[pos].get(1) != None:                    
                    ran_btn1.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][1].x , self.__click_rand[pos][1].y) )
                if self.__click_rand[pos].get(2) != None:                    
                    ran_btn2.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][2].x , self.__click_rand[pos][2].y) )
                if self.__click_rand[pos].get(3) != None:                    
                    ran_btn3.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][3].x , self.__click_rand[pos][3].y) )
                
                if self.__click_rand[pos].get(11) != None:
                    cap_bnt0.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][11].x , self.__click_rand[pos][11].y) )
                if self.__click_rand[pos].get(12) != None:
                    cap_bnt1.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][12].x , self.__click_rand[pos][12].y) )                



        cmp_btn = QPushButton('적용')
        cmp_btn.setFixedWidth(100)
        cmp_btn.clicked.connect( fn_cmp )   
        cmp_btn.setVisible( False )                       
        hbox.addWidget( cmp_btn )
        
        if self.__div.get(pos) != None:            
            div.setCurrentText( self.__div[pos] ) # 행동 선택

        # 로드시 선택 적용.
        if self.__click_xy.get(pos) != None:            
            if self.__click_xy.get(pos) != None:
                geo_btn.setText( '(x:{0},y:{1})'.format(self.__click_xy[pos].x , self.__click_xy[pos].y) )   #좌표값.

            col.setCurrentText( self.__click_evn[pos] ) # 클릭후 이벤트 컬럼 혹은 횟수. 행동후 대기사간은 공통 1초이다.
            geo_xy_wait.setText( self.__click_xy_wait[pos] ) #해당행 끝나후 대기 시간.
            key0.setCurrentText( self.__key0[pos] )     # 키입력 이벤트 처리
            key0_wait.setText( self.__key0_wait[pos] )      # 키입력후 대기 시간
            fn_div( self.__div[pos] )   # 활성화부분    
            #print('로드시 : ',pos , self.__click_rand.get(pos) )
            if self.__click_rand.get(pos) != None:
                #랜덤 버튼 정의 값 저장
                if self.__click_rand[pos].get(0) != None:                    
                    ran_btn0.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][0].x , self.__click_rand[pos][0].y) )
                if self.__click_rand[pos].get(1) != None:                    
                    ran_btn1.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][1].x , self.__click_rand[pos][1].y) )
                if self.__click_rand[pos].get(2) != None:                    
                    ran_btn2.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][2].x , self.__click_rand[pos][2].y) )
                if self.__click_rand[pos].get(3) != None:                    
                    ran_btn3.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][3].x , self.__click_rand[pos][3].y) )

                if self.__click_rand[pos].get(11) != None:
                    cap_bnt0.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][11].x , self.__click_rand[pos][11].y) )
                if self.__click_rand[pos].get(12) != None:
                    cap_bnt1.setText( '(x:{0},y:{1})'.format(self.__click_rand[pos][12].x , self.__click_rand[pos][12].y) )                
        
        hbox.addStretch()

        groupbox.setLayout(hbox)
        return groupbox
   

    def foot(self):
        groupbox = QGroupBox('')
        grid = QGridLayout()
        grid.setSpacing(0)

        def fn_save():
            '''파일저장.'''
            save_array = []
            save_array.append(
                {
                      'url_xy'          : self.__url_xy                 # url 클릭 좌표
                    , 'url_xy_wait'     : self.__url_xy_wait            # 0.5 초 기본 대기 url 클릭후 대기
                    , 'url_path'        : self.__url_path               # url 클릭 좌표
                    , 'url_path_wait'   : self.__url_path_wait          # 2초 기본 대기 url 주소 입력후 대기시간
                    , 'cvs_path'        : self.__cvs_path               # cvs 파일 위치
                    , 'div'             : self.__div            #선택값
                    , 'click_xy'        : self.__click_xy       #클릭 
                    , 'click_evn'       : self.__click_evn      #클릭   복사 컬럼 위치 선택후 붙여넣기
                    , 'click_rand'      : self.__click_rand     #랜덤클릭
                    , 'click_xy_wait'   : self.__click_xy_wait  #클릭 실행후 대기시간    
                    , 'key0'            : self.__key0           # 키보드0 단일키 하나
                    , 'key0_wait'       : self.__key0_wait      # 키보드0 대기
                    , 'key1'            : self.__key1           # 키보드1 복합키 두개 - hot key 하기
                    , 'key1_wait'       : self.__key1_wait      # 키보드1 대기                                
                }
            )  
            file_name = save_file_nm.text().replace(' ','')
            if file_name == '':
                QMessageBox.about(self,'About Title','파일이름이 없습니다. ')
            else :
                QMessageBox.about(self,'About Title','파일명 "{0}" 저장합니다. '.format( file_name ) )
                with open('c:\\ncnc_class\\'+file_name+'.pickle',"wb") as f:
                    pickle.dump(save_array, f) # 위에서 생성한 리스트를 list.pickle로 저장              

        save_btn = QPushButton('Save')
        save_btn.clicked.connect(    fn_save   )  
        grid.addWidget( save_btn , 0 , 0 ,1,1)
    
        def fn_load():
            ''' 피클 데이터 로드'''
            self.__file_nm = load_cb.currentText()  
            file_path = 'C:\\ncnc_class\\{}{}'.format( self.__file_nm ,'.pickle')                
            _load_data = []
            with open(file_path, 'rb') as f:
                _load_data = pickle.load(f)  

            self.__url_xy           = _load_data[0]['url_xy']           # url 클릭 좌표
            self.__url_xy_wait      = _load_data[0]['url_xy_wait']      # 0.5 초 기본 대기 url 클릭후 대기
            self.__url_path         = _load_data[0]['url_path']         # url 클릭 좌표
            self.__url_path_wait    = _load_data[0]['url_path_wait']    # 2초 기본 대기 url 주소 입력후 대기시간
            self.__cvs_path         = _load_data[0]['cvs_path']         # cvs 파일 위치
            self.__div              = _load_data[0]['div']              #선택값
            self.__click_xy         = _load_data[0]['click_xy']         #클릭 
            self.__click_evn        = _load_data[0]['click_evn']        #클릭   복사 컬럼 위치 선택후 붙여넣기
            self.__click_rand       = _load_data[0]['click_rand']       #랜덤클릭
            self.__click_xy_wait    = _load_data[0]['click_xy_wait']    #클릭 실행후 대기시간    
            self.__key0             = _load_data[0]['key0']             # 키보드0 단일키 하나
            self.__key0_wait        = _load_data[0]['key0_wait']        # 키보드0 대기
            self.__key1             = _load_data[0]['key1']             # 키보드1 복합키 두개 - hot key 하기
            self.__key1_wait        = _load_data[0]['key1_wait']        # 키보드1 대기  
            #self.__cap1             = _load_data[0]['cap1']                  
            
            # 기존 자료 마이그레이션. 
            for i in self.__div:
                str = self.__div.get(i)
                str = str.replace('클릭-0','클릭').replace('클릭-1','붙여넣기').replace('클릭-2','글씨쓰기').replace('클릭-3','선택하기').replace('클릭-4','중복선택').replace('키보드-0','방향전환')
                self.__div[i] = str


            #print( 'self.__click_rand',self.__click_rand )
            #print( 'self.__click_rand.get(0)',self.__click_rand.get(0) )
            self.fnLoad()

        load_btn = QPushButton('Load')
        load_btn.clicked.connect(    fn_load   )  
        grid.addWidget( load_btn , 0 , 1 ,1,2 )

        def fnStart():
            '''매크로 시작 버튼'''
            start_btn.setEnabled(False)
            csv_data = self.readfile( self.__cvs_path )                        
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
            )
            self.__work.start()
        
        def fnStop():
            '''매크로 종료 버튼'''
            print('fnStop','*'*50)
            #stop_btn.setEnabled(False)
            start_btn.setEnabled(True)            
            self.__work.stop()


        start_btn = QPushButton('Start')
        start_btn.clicked.connect(    fnStart   )  
        grid.addWidget( start_btn , 0 , 3,1,1 )

        stop_btn = QPushButton('Stop')        
        stop_btn.clicked.connect(    fnStop   )  
        grid.addWidget( stop_btn , 0 , 4,1,1 )

        save_lb = QLabel('저장파일 : '   )
        grid.addWidget( save_lb , 1 , 0 ,1,1 )
        
        save_file_nm = QLineEdit()     
        save_file_nm.setStyleSheet( self.__lb_style )
        if self.__file_nm != '':
            save_file_nm.setText( self.__file_nm )
        
        grid.addWidget( save_file_nm , 1 , 1,1,2 )

        load_lb = QLabel('로드파일 : '  )        
        grid.addWidget( load_lb , 1 , 3,1,2 )


        

        def getfolelist():    
            '''덤프 파일 정보 가져오기.'''
            _path = 'C:\\ncnc_class\\'
            __list = os.listdir( _path )    
            list = []
            for i in __list:
                if i.find( 'pickle' ) != -1 :
                    list.append(i.replace('.pickle',''))
            return list        
        file_list = getfolelist()
        load_cb = QComboBox()
        for i in file_list:
            load_cb.addItem(i)
        grid.addWidget( load_cb , 1 , 4,1,2 )
        groupbox.setFixedHeight(70)
        groupbox.setLayout(grid)
        
        return groupbox

    def readfile(self , path):
        '''파일 읽기'''
        _rt = []
        f = open(path , 'r', encoding='utf-8'  )
        rdr = csv.reader(f , delimiter='^')
        for line in rdr:
            _rt.append( line )
        f.close()    
        return _rt      


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
