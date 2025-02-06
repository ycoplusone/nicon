import time
import csv
import cv2
import numpy as np
import os
import mimetypes
import pyzbar.pyzbar as pyzbar  # pip install pyzbar

'''
1.0.0 바코드 리더 생성
'''

class BarcodeExtraction():
    __root_fold     = 'C:\\ncnc_class\\'        # 기준 폴더
    __target_fold   = 'zzBarcodeExtraction'     # 사용할 폴더 이름
    __files         = []                        # 이미지 파일 리스트


    def __init__(self):
        '''초기화 함수'''               
    
    def main(self):
        self.__files = []
        self.mk_fold() #기본 폴더 생성
        self.exBarcode() #파일 이름 바코드 변경 
        self.mkDataFile()
        print('파일리스트 생성 완료','*'*50)

    def mk_fold( self ):
        '''기본폴더 생성'''
        try :
            os.mkdir( f'{self.__root_fold}{self.__target_fold}')
        except BaseException as e:
            print('폴더가 있음.')
            


    def decode(self , im):
        '''Find barcodes and QR codes
        바코드 탐지하는 엔진 (바코드 및 QR코드 탐지)
        ''' 
        _str = None
        try:
            decodedObjects = pyzbar.decode(im)        
            for obj in decodedObjects:
                _str = obj.data.decode('utf-8') 
                print(_str)       
        except Exception as e:
            print(e)
            return None
        return _str

    def exBarcode(self):
            '''파일 이름 바코드 변경.'''
            str         = f'{self.__root_fold}{self.__target_fold}'
            lists       = os.listdir( str )
            all_files   = [ os.path.join(str, x)  for x in lists ]     # 파일이름에 경로 까지 넣기   
            t1_files    = [ X for X in all_files if os.path.isfile(X)] #대상 파일 리스트
            

            # 이미지만.
            for file in t1_files:
                # MIME 타입 추측
                mime_type, encoding = mimetypes.guess_type(file)
                if 'image' in mime_type:
                    self.__files.append(file)
            
            for file in self.__files:
                try:
                    __sp        = os.path.splitext(file)
                    __exc       = __sp[1] # 확장자
                    __n         = np.fromfile(file, np.uint8)
                    __img       = cv2.imdecode(__n, cv2.IMREAD_COLOR)
                    __barcode   = self.decode(__img)      
                    __rename_file_nm    = f'{str}\\{__barcode}{__exc}'
                    os.rename( file , __rename_file_nm )
                except Exception as e :
                    ''''''
                    #print('into_rename_barcode : ',e)

    def mkDataFile(self):
        '''리스트 생성'''
        with open( f'{self.__root_fold}{self.__target_fold}\\파일리스트.txt' , "w") as f:    
            for file in self.__files:            
                _file_name = os.path.basename(file)
                _sp = str(_file_name).split('.')
                # 파일에 내용 쓰기
                f.write( f'{_sp[0]}\n')        


if __name__ == '__main__':
    # 프로그램. 실행 부분.
    be = BarcodeExtraction()    

    
    
    
    