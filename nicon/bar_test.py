
import pyzbar.pyzbar as pyzbar  # pip install pyzbar
import cv2                      # pip install opencv-python
import lib.dbcon as dbcon

import numpy as np
import os

def decode(im):
    '''Find barcodes and QR codes
    # 바코드 탐지하는 엔진 (바코드 및 QR코드 탐지)
    ''' 
    _str = None
    try:
        decodedObjects = pyzbar.decode(im)        
        for obj in decodedObjects:
            _str = obj.data.decode('utf-8')        
    except Exception as e:
        print(e)
        return None
    return _str

def getbarcoderead():
    '''판매가능한 바코드들이 있는지 확인한다'''
    dd = dbcon.DbConn()
    __base = 'c:\\ncnc'    
    __lists = os.listdir( __base )
    for i in __lists:        
        _dirs = os.listdir( __base+'\\'+i )        
        _temp_list = [ X for X in _dirs if os.path.isdir( __base +'\\'+ i +'\\'+ X )]
        _prod_fold = [ X for X in _temp_list if X[-4:-1] != '(완료']
        for j in _prod_fold:
            _img_file_list = os.listdir( __base+'\\'+i+'\\'+j )
            for m in _img_file_list:
                __full_path = __base+'\\'+i+'\\'+j+'\\'+m
                __n = np.fromfile(__full_path, np.uint8)
                __img = cv2.imdecode(__n, cv2.IMREAD_COLOR)
                __barcode = decode(__img)
                # " VALUES('{base_fold}', '{prod_fold}', '{file_nm}', '{barcode}', now()) "
                param = {'base_fold':i , 'prod_fold':j ,'file_nm':m,'barcode': __barcode }
                dd.insert_nicon_barcode(param)


        
    


# 파일명 zbar.jpg의 이미지에서 바코드를 탐지하면 해당 코드를 리턴
# Main
if __name__ == '__main__':
    # Read image
    #im = cv2.imread('./test_img/barcode.jpg')    
    #im = cv2.imread('./nicon/1.png')
    #print( decode(im) )
    getbarcoderead()
    