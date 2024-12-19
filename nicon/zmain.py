import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtTest import *
import time
from datetime import datetime
from pytz import timezone
import subprocess

'''
1.0.0 zmain 프로그램 생성
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
        #os.popen( self.__msg )
        subprocess.call( self.__msg )
        nt = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        print(f'{nt}','='*50)

class MyApp(QWidget):    
    __version   = '1.0.0'
    __title_nm  = 'Main UI'    

    __lb_style  = 'border-radius: 5px;border: 1px solid gray;'
    __lb_style2 = 'border-radius: 5px;border: 1px solid red;'
    __btn_style = 'QPushButton { height: 30px; }'

    __x         = 1024      # ui 시작 좌표

    
    # 전역변수 - begin
    __workcmd       = '' # 쓰레드
    __processes     = []
    # 전역변수 - end    
    
    # UI - BEGIN
    __btnUI              = {} #버튼

    # UI - END

    # Init 시작 부분 ##################################################
    def __init__(self):
        super().__init__()
        self.init_param() # 전역변수 초기화
        self.initUI()
        self.setMinimumHeight(270)
        self.setMaximumHeight(270)
        self.setGeometry(self.__x, 100, 300, 250)
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
        #self.DisconnectAdbScrcpy()
    
    # Init 종료 부분    ##################################################

    # Ui 시작 부분      ##################################################
    def head0(self):
        ''' 두번째 줄'''
        groupbox    = QGroupBox('Menu')
        box         = QGridLayout()
        box.setSpacing(5)
        self.__btnUI[0] = QPushButton('Soldier')
        self.__btnUI[0].setStyleSheet( self.__btn_style )     
        self.__btnUI[0].clicked.connect( lambda : self.test( 'python mk_macro_ver3.py' )  )

        self.__btnUI[1] = QPushButton('Army')
        self.__btnUI[1].setStyleSheet( self.__btn_style )
        self.__btnUI[1].clicked.connect( lambda : self.test( 'python mk_macro_multi.py' )  )

        self.__btnUI[2] = QPushButton('Mini')
        self.__btnUI[2].setStyleSheet( self.__btn_style )
        self.__btnUI[2].clicked.connect( lambda : self.test( 'python mini.py' )  )
        
        box.addWidget( self.__btnUI[0] , 0,0 )
        box.addWidget( self.__btnUI[1] , 1,0 )
        box.addWidget( self.__btnUI[2] , 2,0 )

        groupbox.setLayout( box )        
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
    def test(self, pg=''):
        ''''''        
        #os.system(f"python {pg}")
        '''
        p = multiprocessing.Process( target= self.run_script , args=(pg,) )
        self.__processes.append( p )
        p.start()

        for process in self.__processes:
            process.join()
        '''
        self.__workcmd.InitParam( pg )
        self.__workcmd.start()     
        time.sleep(5)                                                       


    def ConnectAdbScrcpy(self):
        ''' adb & scrcpy 연결'''

    
    def DisconnectAdbScrcpy(self):
        ''' adb & scrcpy 종료'''        
       
        




    # 기능 함수 종료 부분 ##################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
