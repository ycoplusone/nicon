from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import csv

import cv2
import numpy as np
from PIL import Image
import pytesseract
from io import BytesIO
import os
import re
import shutil
import pandas as pd


class urlsprint():
    chrome_options = Options()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=512x1080')
    driver = webdriver.Chrome( options= chrome_options )
    base_path = 'C:\\ncnc_class\\data20240515\\'
    input_path = 'C:\\ncnc_class\\data20240515\\data.csv'
    output_path = 'C:\\ncnc_class\\data20240515\\img\\'
    result_path = 'C:\\ncnc_class\\data20240515\\result.csv'

    # 생성된 이미지 텍스트 분석하기.
    def getFiles(self):
        '''이미지 정보 가져오기'''
        try:
            rootlist = os.listdir( self.output_path )
            _files = [X for X in rootlist if os.path.isfile(self.output_path+'\\'+X)]    
            return _files
        except Exception as e:
            print( 'getFiles' , e )    
    
    def getTest(self,_file):
        try:
            _url = ( self.output_path+_file)
            _url2 = ( self.base_path+'temp.jpg' )
            #print(_url)
            img2 = cv2.imread( _url , cv2.IMREAD_COLOR )        
            img3 = img2[375 : 484 , 174 : 460 ]
            #img3.save(self.base_path+'temp.jpg')
            cv2.imwrite( _url2 , img3 )
                        
            img_arry = np.fromfile( _url2 , np.uint8 )
            img = cv2.imdecode( img_arry , cv2.IMREAD_GRAYSCALE )
            #cv2.imshow( 'aaa',img )
            #cv2.waitKey()
            #cv2.destroyAllWindows()
            

            #  opencv api를 이용한 정규화
            img_norm2 = cv2.normalize( img , None , 0 , 255 , cv2.NORM_MINMAX )
            img_norm2 = cv2.medianBlur(img_norm2 ,1 )
            #cv2.imshow( 'aaa',img_norm2 )
            #cv2.waitKey()
            #cv2.destroyAllWindows()
            
            config = ('-l kor') #config = ('-l kor+eng --oem 3 --psm 3')
            _t = pytesseract.image_to_string( img_norm2 , config=config)        
            #print('_t',_t)
            _t = _t.lower()
            _t = _t.replace(' ','') # 공백제거
            _t = re.sub( '[^A-Za-z0-9가-힣\s]', "", _t) #한글
            _temp_arr = _t.split('\n')        
            
            _fin_txt = []
            for i in range(0,len(_temp_arr)):                
                _fin_txt.append( _temp_arr[i] )                            
        
            #print(_file ,'\t' , _fin_txt   )
            return _fin_txt[0] 
        except Exception as e:
            print( 'getText_tesseract' , e ) 


    def getImgText(self) :
        '''이미지 텍스트'''
        files = self.getFiles()
        
        __result = []
        for i in files:            
            file = (i.split('.')[0])
            tt = self.getTest(i)
            print( [file , tt] )
            __result.append( [file , tt] )
        
        f = open(self.base_path+'result.csv', 'w' , newline='', encoding='utf-8')
        writer = csv.writer(f)
        writer.writerows(__result)
        f.close()
    

    # 결과 부분 merge하여 결과를 출력한다.
    def fin_read(self):
        i_txt = self.readfile(self.input_path) 
        r_txt = self.readfile(self.result_path)
        _fin_result = [] 
        for i in i_txt:
            name = i[0]
            url = i[1]
            key1 = url.split('num=')[1]    
            #print(name , url , key1)
            for j in r_txt:
                key2 = j[0]
                state = j[1]
                if key1 == key2:
                    _fin_result.append( [ name , url , state ] )
                    break
        
        _fin_result.sort(key=lambda x:(x[2], x[0]), reverse=False)

        #for i in _fin_result:
        #    print(  i )

        f = open(self.base_path+'zz_result.csv', 'w' , newline='', encoding='utf-8')
        writer = csv.writer(f)
        writer.writerows(_fin_result)
        f.close()


    # 이미지 생성 부분
    def main(self, url , file_nm ):
        try:
            self.driver.get( url )
            # 스크린샷 전에 시간 두기(로딩이 느릴수도 있으니)
            time.sleep(2)
            # 창 최대화
            self.driver.maximize_window()
            # 스크린샷 찍기
            self.driver.save_screenshot(self.output_path+file_nm+".png")
            # 종료 (모든 탭 종료)
            #driver.quit()
            print("### capture complete \t", file_nm)
        except Exception as e:
            print('### error msg :: ', e)
            self.driver.quit()

    def readfile(self , path):
        '''파일 읽기'''
        _rt = []
        f = open(path , 'r', encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            _rt.append( line )
        f.close()    
        return _rt    

    def exec(self):
        '''활성화 부분'''        
        list = self.readfile(self.input_path)
        for i in list:
            name = i[0]
            url = i[1]
            file_nm = url.split('num=')[1]    
            #print(name , url , file_nm)
            self.main( url , file_nm )


if __name__ == '__main__':
    # 프로그램. 실행 부분.
    ob = urlsprint()
    ob.exec() #이미지 생성하기
    ob.getImgText() #이미지 텍스트 분석
    ob.fin_read() # 결과 결합
    
    
    