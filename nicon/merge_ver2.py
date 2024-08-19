import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import barcode
from barcode.writer import ImageWriter
from PIL import Image , ImageFont , ImageDraw
import os


class MyApp(QWidget):
    '''
    기존 이미지에 특정 이미지를 합성.    
    '''
    _lb_style = 'border-radius: 5px;border: 1px solid gray;'

    _resize_rate = 1.0
    _size_w = 1.0  
    _size_h = 1.0

    _gps_chk = False
    _gps_x = 0
    _gps_y = 0

    __fold_path = '' # 합성할 폴더 위치
    __file_list = [] # 할성할 폴더의 파일 리스트
    
    _div = '1' # 1 : cvs , 2 : img
    _target_cvs_list = []
    _target_img_list = []


    def __init__(self):
        super().__init__()
        self.initUI()
    
    def gps_acctive(self):
        self._gps_chk = True 

    def mousePressEvent(self, e):
        try:
            x = e.x()-10
            y = e.y()-10
            self._gps_x = int(x * self._resize_rate)
            self._gps_y = int(y * self._resize_rate)
            if self._gps_chk :
                self.gps_lb.setText( '( x:{0} , y:{1})'.format(self._gps_x , self._gps_y) )
                self._gps_chk = False
        except Exception as e:
            print('def mousePressEvent',e)          


    def fold_open(self):
        ''' 폴더 선택창
        폴더를 선택후 해당 폴더의 이미지 하나를 배경에 넣는다.
        '''
        __path =QFileDialog.getExistingDirectory(self)  # QFileDialog.getOpenFileName(self)       
        self.__fold_path = __path 
        self.fold_lb.setText( self.__fold_path )
        self.__file_list = os.listdir( self.__fold_path )                
        
        _aa = QPixmap( self.__fold_path+'\\'+self.__file_list[0] )
        _w = _aa.width() #500
        _h = _aa.height() #750
        _re_size_w = _w / 500
        _re_size_h = _h / 750        
        self._resize_rate = max(_re_size_w , _re_size_h)
        _re_w = int(_w / self._resize_rate)
        _re_h = int(_h / self._resize_rate)
        print( _w , _h , _re_size_w , _re_size_h ,  self._resize_rate , _re_w  , _re_h)
        self.lb.setPixmap( QPixmap( _aa ).scaled( _re_w ,  _re_h ) )          
        


    def fileopen(self):
        try:        
            fname = QFileDialog.getOpenFileName(self)
            _nm = fname[0]
            self.file_lb.setText( _nm )
            
        except Exception as e:
            print('def fileopen',e)   

    def getImgList(self):
        try:        
            fname = QFileDialog.getOpenFileNames(self)
            self._target_img_list = fname[0]
            self.cvs_text2.setText('')	
            for i in self._target_img_list:                
                self.cvs_text2.append( i )
        except Exception as e:
            print('def fileopen',e) 

    def getFold(self):
        try:
            fname = QFileDialog.getExistingDirectory(self,'폴더선택','')
            self.export_fold_lb.setText( fname )
        except Exception as e:
            print('def getFold',e) 

    
    def select_act(self):
        if self.rbtn1.isChecked():
            self._div = '1'
            self.gpbox2_1.setVisible(True)
            self.gpbox2_2.setVisible(False)
        else:
            self._div = '2'
            self.gpbox2_1.setVisible(False)
            self.gpbox2_2.setVisible(True)
    
    def merge_exec(self):
        
        try:
            _chk0 = (False if len(self.fold_lb.text()) > 0 else True)        
            _chk1 = (False if len(self.file_lb.text()) > 0 else True)
            _chk2 = (False if self._gps_x > 0 else True)
            _chk3 = (False if self._gps_y > 0 else True)
            


        
            if _chk0 or _chk1 or _chk2 or _chk3:
                print('adfadsf')
                QMessageBox.about(self,'확인','안됨 이미지 합성 안됨...')
            else :
                self.mk_img3()
                QMessageBox.about(self,'확인','완료.')

        except Exception as e:
            print('merge_exec chk' , e)
        
            
    

    def mk_barcode_img(self , str):
        barcode_num = str
        file_path = self.export_fold_lb.text()+'/temp'
        options = {"module_width":0.51, "module_height":16, "font_size": 10, "text_distance": 4, "quiet_zone": 1}        
        code128 = barcode.get_barcode_class('code128')
        my_ean = code128( barcode_num, writer=ImageWriter())
        file_nm = my_ean.save( file_path , options )
        return file_nm

    def mk_img(self ,  code , ps , ex ):
        '''텍스트 추가하기'''
        pass_word = ('' if ps == '' else '비밀번호 : '+ps)
        ex_date   = '유효기간 : '+ex    
        # export path
        _path = self.export_fold_lb.text()+'/'+code+'.png' #'c:\\ncnc\\'+code+'.png'
        #바코드 이미지 가져오기
        _barcode_img = Image.open( self.mk_barcode_img(code) ) 
               
        _target_img = Image.open( self.file_lb.text() )  #Image.open('./test_img/megabox_bg.png')
        _font = ImageFont.truetype('./test_img/PyeongChang-Regular.ttf', 24)
        out_img = ImageDraw.Draw( _target_img )
        out_img.text(xy=(self._gps_x , self._gps_y+290), text=pass_word , font=_font , fill=(0,0,0) )
        out_img.text(xy=(self._gps_x , self._gps_y+330), text=ex_date   , font=_font , fill=(0,0,0) ) 
        _target_img.paste( _barcode_img, (self._gps_x , self._gps_y) )
        _target_img.save( _path )
    
    def mk_img2(self, file_nm):
        fff = os.path.split(file_nm)[1]
        _path = self.export_fold_lb.text()+'/'+fff
        _barcode_img = Image.open( file_nm ) 
        _target_img = Image.open( self.file_lb.text() )  #Image.open('./test_img/megabox_bg.png')
        _font = ImageFont.truetype('./test_img/PyeongChang-Regular.ttf', 24)
        out_img = ImageDraw.Draw( _target_img )
        _target_img.paste( _barcode_img, (self._gps_x , self._gps_y) )
        _target_img.save( _path )

    def mk_img3(self):
        ''' 이미지 합성3'''
        #__fold_path = '' # 합성할 폴더 위치
        #__file_list = [] # 할성할 폴더의 파일 리스트     
           
        rep_img = Image.open( self.file_lb.text() ) # 반복 사용할 합성 이미지.

        for i in self.__file_list:            
            export_path = self.export_fold_lb.text()+'/'+i # 내보낼 패스.
            base_img = Image.open( self.__fold_path+'/'+i ) # 기반 이미지.
            out_img = ImageDraw.Draw( base_img )
            base_img.paste( rep_img , (self._gps_x , self._gps_y) )
            base_img.save( export_path )
            print( i , '\t',export_path )
        


    def initUI(self):
        pixmap = QPixmap('')
        self.lb = QLabel(self)
        self.lb.setStyleSheet( self._lb_style )
        self.lb.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.lb.setGeometry(10,10,500,750) # x , y , w , h
        self.lb.setPixmap( QPixmap(pixmap) )

        # 0. 파일파일 폴더 지정
        self.fold_btn = QPushButton('0.이미지 폴더',self)
        self.fold_btn.clicked.connect(self.fold_open)
        self.fold_btn.setGeometry(520,10,100,30) # x , y , w , h                    
        
        self.fold_lb = QLabel('',self)
        self.fold_lb.setStyleSheet( self._lb_style )
        self.fold_lb.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        self.fold_lb.setGeometry(620,10,400,30) # x , y , w , h        


        # 1. 파일 로드
        self.filebtn = QPushButton('1.합성 파일 로드',self)
        self.filebtn.clicked.connect(self.fileopen)  
        self.filebtn.setGeometry(520,50,100,30) # x , y , w , h        
        
        self.file_lb = QLabel('',self)
        self.file_lb.setStyleSheet( self._lb_style )
        self.file_lb.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        self.file_lb.setGeometry(620,50,400,30) # x , y , w , h

        # 2. 좌표 구하기
        self.gps_btn = QPushButton('2.시작좌표 지정',self)
        self.gps_btn.clicked.connect(    self.gps_acctive   )  
        self.gps_btn.setGeometry(520,100,100,30) # x , y , w , h  

        self.gps_lb = QLabel('( x:{0} , y:{1})'.format(self._gps_x , self._gps_y),self)
        self.gps_lb.setStyleSheet( self._lb_style )
        self.gps_lb.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        self.gps_lb.setGeometry(620,100,400,30) # x , y , w , h     

       
        # 3. 파일 로드
        self.export_fold = QPushButton('5.추출폴더선택',self)
        self.export_fold.clicked.connect(self.getFold)  
        self.export_fold.setGeometry(520,150,100,30) # x , y , w , h     

        self.export_fold_lb = QLabel('',self)
        self.export_fold_lb.setStyleSheet( self._lb_style )
        self.export_fold_lb.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        self.export_fold_lb.setGeometry(620,150,400,30) # x , y , w , h

        # 4. 합성
        self.submit_bnt = QPushButton('6.합성',self)
        self.submit_bnt.setStyleSheet('QPushButton {	color: rgb(58, 134, 255);	background-color: white;	border: 2px solid rgb(58, 134, 255);	border-radius: 5px;}')
        self.submit_bnt.clicked.connect(self.merge_exec)  
        self.submit_bnt.setGeometry(520,200,500,50) # x , y , w , h   
        
        


        self.setMouseTracking(True) # 마우스 이벤트        
        self.setWindowTitle('이미지 합성')
        self.setGeometry(50, 50, 1024, 768)
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())