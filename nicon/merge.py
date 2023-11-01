import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import barcode
from barcode.writer import ImageWriter
from PIL import Image , ImageFont , ImageDraw
import os


class MyApp(QWidget):
    _lb_style = 'border-radius: 5px;border: 1px solid gray;'

    _resize_rate = 1.0
    _size_w = 1.0  
    _size_h = 1.0

    _gps_chk = False
    _gps_x = 0
    _gps_y = 0

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


    def fileopen(self):
        try:        
            fname = QFileDialog.getOpenFileName(self)
            _nm = fname[0]
            _aa = QPixmap( fname[0] )
            _w = _aa.width() #500
            _h = _aa.height() #750
            _re_size_w = _w / 500
            _re_size_h = _h / 750        
            self._resize_rate = max(_re_size_w , _re_size_h)
            _re_w = int(_w / self._resize_rate)
            _re_h = int(_h / self._resize_rate)
            print( _w , _h , _re_size_w , _re_size_h ,  self._resize_rate , _re_w  , _re_h)
            self.file_lb.setText( _nm )
            self.lb.setPixmap( QPixmap( _aa ).scaled( _re_w ,  _re_h ) )  
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
            _chk1 = (False if len(self.file_lb.text()) > 0 else True)
            _chk2 = (False if self._gps_x > 0 else True)
            _chk3 = (False if self._gps_y > 0 else True)
            if self._div == '1':
                _chk4 = (False if len(self.cvs_text.toPlainText()) > 0 else True)
            else :
                _chk4 = (False if len(self.cvs_text2.toPlainText()) > 0 else True)
            _chk5 = (False if len( self.export_fold_lb.text() ) > 0 else True)
            


        
            if _chk1 or _chk2 or _chk3 or _chk4 or _chk5:
                print('adfadsf')
                QMessageBox.about(self,'확인','안됨 이미지 합성 안됨...')
            else :
                if self._div == '1':
                    print('cvs 기준') # self._target_cvs_list
                    self._target_cvs_list = []
                    # self.cvs_text
                    _temp = self.cvs_text.toPlainText()
                    _temp = _temp.split('\n')                                    
                    for i in _temp:
                        ii = i.replace(' ','')
                        self._target_cvs_list.append( ii.split(',') )            
                    for i in self._target_cvs_list:
                        self.mk_img(i[0],i[1],i[2])              
                else:
                    print('이미지 기준')
                    for i in self._target_img_list:
                        self.mk_img2( i )
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

        


    def initUI(self):
        pixmap = QPixmap('')
        self.lb = QLabel(self)
        self.lb.setStyleSheet( self._lb_style )
        self.lb.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.lb.setGeometry(10,10,500,750) # x , y , w , h
        self.lb.setPixmap( QPixmap(pixmap) )

        # 1. 파일 로드
        self.filebtn = QPushButton('1.File Load',self)
        self.filebtn.clicked.connect(self.fileopen)  
        self.filebtn.setGeometry(520,10,100,30) # x , y , w , h        
        
        self.file_lb = QLabel('',self)
        self.file_lb.setStyleSheet( self._lb_style )
        self.file_lb.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        self.file_lb.setGeometry(620,10,400,30) # x , y , w , h

        # 2. 좌표 구하기
        self.gps_btn = QPushButton('2.시작좌표 지정',self)
        self.gps_btn.clicked.connect(    self.gps_acctive   )  
        self.gps_btn.setGeometry(520,40,100,30) # x , y , w , h  

        self.gps_lb = QLabel('( x:{0} , y:{1})'.format(self._gps_x , self._gps_y),self)
        self.gps_lb.setStyleSheet( self._lb_style )
        self.gps_lb.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        self.gps_lb.setGeometry(620,40,400,30) # x , y , w , h     

        # 3. 구분 선택
        self.gpbox = QGroupBox('3.구분 선택',self)
        self.gpbox.setGeometry(520,80,500,50)        
        self.rbtn1 = QRadioButton('텍스트 합성', self.gpbox)
        self.rbtn1.clicked.connect( self.select_act )
        self.rbtn1.move(10 , 20)
        self.rbtn1.setChecked(True)
        self.rbtn2 = QRadioButton('이미지 합성' ,self.gpbox)            
        self.rbtn2.clicked.connect( self.select_act )
        self.rbtn2.move(200 , 20)

        # 4. 합성데이터 1
        self.gpbox2_1 = QGroupBox('4.합성 데이터',self)
        self.gpbox2_1.setGeometry(520,140,500,500)        
        self.cvs_lb = QLabel('예시 [ 바코드,비밀번호,유효기간 ] ',self.gpbox2_1)
        self.cvs_lb.setStyleSheet('QLabel {	background-color: white;	border: 1px solid rgb(131, 56, 236);	border-radius: 5px;}')
        self.cvs_lb.setGeometry( 10 , 25 , 480 , 30 )        

        self.cvs_text = QTextEdit( self.gpbox2_1)
        self.cvs_text.setGeometry( 10 , 60 , 480 , 440 )
        self.cvs_text.setStyleSheet('QTextEdit {	background-color: white;	border: 1px solid rgb(58, 134, 255);	border-radius: 5px;}')
        
        # 4. 합성데이터 2
        self.gpbox2_2 = QGroupBox('4.합성 데이터',self)
        self.gpbox2_2.setGeometry(520,140,500,500)        
        self.merge_img_select = QPushButton('합성이미지선택',self.gpbox2_2)
        self.merge_img_select.setStyleSheet('QPushButton {	background-color: white;	border: 1px solid rgb(131, 56, 236);	border-radius: 5px;}')
        self.merge_img_select.clicked.connect(self.getImgList)  
        self.merge_img_select.setGeometry( 10 , 25 , 480 , 30 )
        self.cvs_text2 = QTextEdit( self.gpbox2_2)
        self.cvs_text2.setReadOnly(True)
        self.cvs_text2.setGeometry( 10 , 60 , 480 , 440 )
        self.cvs_text2.setStyleSheet('QTextEdit {	background-color: white;	border: 1px solid rgb(255, 190, 11);	border-radius: 5px;}')        
        self.gpbox2_2.setVisible(False)


        # 5. 파일 로드
        self.export_fold = QPushButton('5.추출폴더선택',self)
        self.export_fold.clicked.connect(self.getFold)  
        self.export_fold.setGeometry(520,650,100,30) # x , y , w , h     

        self.export_fold_lb = QLabel('',self)
        self.export_fold_lb.setStyleSheet( self._lb_style )
        self.export_fold_lb.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        self.export_fold_lb.setGeometry(620,650,400,30) # x , y , w , h




        # 6. 합성
        self.submit_bnt = QPushButton('6.합성',self)
        self.submit_bnt.setStyleSheet('QPushButton {	color: rgb(58, 134, 255);	background-color: white;	border: 2px solid rgb(58, 134, 255);	border-radius: 5px;}')
        self.submit_bnt.clicked.connect(self.merge_exec)  
        self.submit_bnt.setGeometry(520,710,500,50) # x , y , w , h   
        
        


        self.setMouseTracking(True) # 마우스 이벤트        
        self.setWindowTitle('이미지 합성')
        self.setGeometry(50, 50, 1024, 768)
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())