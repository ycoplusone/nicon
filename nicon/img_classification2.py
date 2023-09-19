# pip install scikit-learn
# pip install cdifflib

import cv2
import numpy as np
from PIL import Image
import pytesseract
from io import BytesIO
import os
import re
import shutil

# 텍스트 유사도 분석
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity

import difflib

import lib.util as w2ji


_base_root = 'c:\\ncnc_class'  

def compare_images(_hist1, _hist2):    
    ''' cv2.calcHist([re_img], [0], None, [256], [0, 256]) 값 두개를 비교한다. '''

    # 히스토그램 비교
    similarity = cv2.compareHist(_hist1, _hist2, cv2.HISTCMP_CORREL)
    return similarity


def getText_tesseract( _file ):
    '''테서렉트 문자열 가져오기'''    
    
    try:        
        _url = (_base_root+'\\'+_file)

        img_arry = np.fromfile( _url , np.uint8 )
        img = cv2.imdecode( img_arry , cv2.IMREAD_GRAYSCALE )
        
        re_img = cv2.resize(img, (300, 300))
        re_img_hist = cv2.calcHist([re_img], [0], None, [256], [0, 256])



        #  opencv api를 이용한 정규화
        img_norm2 = cv2.normalize( img , None , 0 , 255 , cv2.NORM_MINMAX )
        img_norm2 = cv2.medianBlur(img_norm2 ,1 )
        
        config = ('-l kor+eng ') #config = ('-l kor+eng --oem 3 --psm 3')
        _t = pytesseract.image_to_string( img_norm2 , config=config)        
        _t = _t.lower()
        _t = _t.replace(' ','') # 공백제거
        _t = re.sub( '[^A-Za-z0-9가-힣\s]', "", _t) #한글
        _temp_arr = _t.split('\n')        

        _fin_txt = []
        for i in range(0,len(_temp_arr)):                
            if len(_temp_arr[i]) > 2 :
                if( '기간' in  _temp_arr[i] or '사용' in  _temp_arr[i] or '유효' in  _temp_arr[i]  ):
                    break
                else :
                    if (  _temp_arr[i] != '나의두번째선물하기'  ):
                        if len(re.sub( '[0-9]','', _temp_arr[i] )) >=1:
                            _fin_txt.append( _temp_arr[i] )                    

                #if len(re.sub( '[a-z0-9]','', _temp_arr[i] )) >2:                 
                    '''
                    if( '기간' in  _temp_arr[i] or '사용' in  _temp_arr[i] or '유효' in  _temp_arr[i] ):
                        break
                    else :
                        if (  _temp_arr[i]!='나의두번째선물하기'  ):
                            _fin_txt.append( _temp_arr[i] )
                    '''
        #_fold_nm = '_'.join(_fin_txt)           
        print('_'.join(_fin_txt)           )
        return _fin_txt , re_img_hist
    except Exception as e:
        print( 'getText_tesseract' , e ) 

def getFiles():
    '''파일 리스트 가져오기'''
    try:
        rootlist = os.listdir( _base_root )
        _files = [X for X in rootlist if os.path.isfile(_base_root+'\\'+X)]    
        return _files
    except Exception as e:
        print( 'getFiles' , e ) 


def mk_fold( _str ):
    '''폴더 생성'''
    try :
        tt = os.path.isdir( _base_root+'\\'+_str)
        if tt:
            print('폴더 : ',_str)
        else :
            os.mkdir( _base_root+'\\'+_str )
    except Exception as e:
        print( 'base_fold_create' , e ) 

def mv_file( _file_nm , _fold_nm ):
    ''''''
    _file = _base_root+'\\'+_file_nm
    _fold = _base_root+'\\'+_fold_nm
    shutil.move( _file , _fold )



files = getFiles()
__lists = []
for file in files:
    print('진행 : ',file)
    param = {} # param['file_nm'] = '파일명'
    param['file_nm'] = file
    _fold_nm , _hist = getText_tesseract(file)
    param['fold_nm']  = _fold_nm
    param['main_fold'] = '_'.join( _fold_nm ) 
    param['mail_file'] = file
    param['img_hist'] = _hist
    param['txt_similar'] = 0.0
    param['img_similar'] = 0.0
    __lists.append( param )


for i in range(0 , len(__lists)):
    org_file_nm = __lists[i]['file_nm']
    org_similar = __lists[i]['txt_similar']
    org_txt     =  __lists[i]['main_fold']
    org_txt_by  = bytes(org_txt, 'utf-8')
    org_bytes_list = list(org_txt_by)

    # 텍스트 유사도 분석 자료 txtsimilar가 1.0 와 0.0인 자료는 이미지 분석 하지 않는다. 0.0은 폴더 정의 하지 않는다. 1.0는 그대로 사용한다.
    for j in range(0 , len(__lists)):
        com_file_nm = __lists[j]['file_nm']
        if org_file_nm != com_file_nm :
            com_txt = __lists[j]['main_fold']
            com_txt_by  = bytes(com_txt, 'utf-8')
            com_bytes_list = list(com_txt_by)
            sm = difflib.SequenceMatcher(None, org_bytes_list, com_bytes_list)
            similar = sm.ratio()            
            #print(org_txt , com_txt , similar)
            if org_similar <= similar and similar >= 0.61 :                
                if __lists[i]['txt_similar'] <= 0.90 or similar == 1.0 :
                    __lists[i]['main_fold']     = com_txt
                    __lists[i]['mail_file']     = com_file_nm                    
                    __lists[i]['txt_similar']   = similar    
                    org_similar = similar
  
# 료는 정리한다.
__lists_fin = [] # 완전 완료
__lists_progress = [] # 이미지 유사도 처리해야 하는 자료
for i in __lists:
    if i['txt_similar'] == 1.0 or i['txt_similar'] == 0.0:
        __lists_fin.append( i )
    else :
        __lists_progress.append( i )


for i in range(0 , len(__lists_progress)):
    org_main_file   = __lists_progress[i]['mail_file']
    org_img_hist    = __lists_progress[i]['img_hist']
    for j in __lists:
        if org_main_file == j['file_nm']:
            com_img_hist = j['img_hist']
            hist_info = compare_images(org_img_hist , com_img_hist)
            __lists_progress[i]['img_similar'] = hist_info


print('완벽텍스트 이동','-'*100)
for i in __lists_fin:    
    print( i['file_nm'],' : ' ,i['fold_nm'],' : ' ,i['main_fold'],' : ' ,i['txt_similar'],' : ' ,i['img_similar'] )
    if (i['txt_similar'] == 1.0 and i['main_fold'] != ''  ):
        mk_fold( i['main_fold'] ) # 폴더 생성
        mv_file( i['file_nm'] , i['main_fold'] )


print('이미진 유사도 99.95 이동','-'*100)
for i in __lists_progress:
    print( i['file_nm'],' : ' ,i['fold_nm'],' : ' ,i['main_fold'],' : ' ,i['txt_similar'],' : ' ,i['img_similar'] )
    if (i['img_similar'] >= 0.9995 and i['main_fold'] != '' ):
        mk_fold( i['main_fold'] ) # 폴더 생성
        mv_file( i['file_nm'] , i['main_fold'] ) #이동


    


