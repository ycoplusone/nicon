# https://github.com/UB-Mannheim/tesseract/wiki 프로그램 설치 
# 한글팩 도 같이 설치 후 path 를 잡아야 한다.


from PIL import Image
import pytesseract
from io import BytesIO
import cv2
import os
import re
import shutil
import numpy as np

import lib.util as w2ji


base_root = 'c:\\ncnc_class'  
def mk_fold( _str ):
    '''폴더 생성'''
    try :
        tt = os.path.isdir( base_root+'\\'+_str)
        if tt:
            print('폴더 : ',_str)
        else :
            os.mkdir( base_root+'\\'+_str )
    except Exception as e:
        print( 'base_fold_create' , e ) 

def mv_file( _file_nm , _fold_nm ):
    ''''''
    _file = base_root+'\\'+_file_nm
    _fold = base_root+'\\'+_fold_nm
    shutil.move( _file , _fold )

def getText_tesseract(_url):
    _t = ''
    try:        
        #print( '_url.shape : ',_url.shape )
        img = cv2.imread( _url )
        img_gray = cv2.cvtColor( img , cv2.COLOR_BGR2GRAY   )

        #  opencv api를 이용한 정규화
        img_norm2 = cv2.normalize( img_gray , None , 0 , 255 , cv2.NORM_MINMAX )
        img_norm2 = cv2.medianBlur(img_norm2 ,1 )
        

        '''
        img2 = np.array( Image.open( _url ) )
        norm_img = np.zeros( (img2.shape[0] , img2.shape[1]) )
        img3 = cv2.normalize( img2 , norm_img , 0 , 255 , cv2.NORM_MINMAX )
        img3 = cv2.threshold( img3 , 100, 255 , cv2.THRESH_BINARY )[1]
        img3 = cv2.GaussianBlur( img3 , (1,1) , 0 )
        '''


        
        config = ('-l kor+eng ') #config = ('-l kor+eng --oem 3 --psm 3')
        _t = pytesseract.image_to_string( img_norm2 , config=config)        
        _t = _t.lower()
        return _t
    except Exception as e:
        print( 'getText_tesseract' , e ) 

'''
def getText_easyocr(_url):
    _t = ''
    try:
        reader = easyocr.Reader(['ko','en'] , gpu=False)
        img = cv2.imread( _url )
        _t = reader.readtext( img , detail=0 )
        print(_t)
        return _t
    except Exception as e:
        print( 'getText_tesseract' , e ) 
'''


def image_classification():
    ''''''
    try:                
        rootlist = os.listdir(base_root)        
        files = [X for X in rootlist if os.path.isfile(base_root+'\\'+X)]
        for file in files:
            print('진행 : ',w2ji.getNow() , file)
            i = base_root+'\\'+file

            text = getText_tesseract(i)
            text = text.replace(' ','') # 공백제거
            text = re.sub( '[^A-Za-z0-9가-힣\s]', "", text) #한글
            temp_arr = text.split('\n')
            

            fin_txt = []
            for i in range(0,len(temp_arr)):                
                if len(temp_arr[i]) > 2 :
                    if len(re.sub( '[a-z0-9]','', temp_arr[i] )) >2:
                        if( '기간' in  temp_arr[i] or '사용' in  temp_arr[i] or '유효' in  temp_arr[i] ):
                            break
                        else :
                            if (  temp_arr[i]!='나의두번째선물하기'  ):
                                fin_txt.append( temp_arr[i] )
            fold_nm = '_'.join(fin_txt)            
            print('진행 : ',w2ji.getNow(), ' : ' , file ,' : ' , fin_txt)
            if len(fold_nm) > 5:
                mk_fold( fold_nm ) # 폴더 생성
                mv_file( file , fold_nm )
            

 
    except Exception as e :
        print('into_rename_barcode : ',e)


print('시작 : ',w2ji.getNow() )
image_classification()
print('종료 : ',w2ji.getNow() )
