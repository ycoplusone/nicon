'''
pip install paddlepaddle 
pip install paddleocr
'''

from paddleocr import PaddleOCR
import os
import re
import shutil
from datetime import datetime
import time
from pytz import timezone
from multiprocessing import Pool

base_root = 'c:\\ncnc_class'  
def now():
    '''시간'''
    return datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')

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

def getText( _ocr ,  _url  ):
    '''paddleocr lib로 텍스트 가져오기 '''
    _fin_txt = []
    _rt = []
    result = _ocr.ocr( _url , cls=False) 
    ocr_result = result[0]
    for i in ocr_result:
        _txt = i[1][0]        
        _txt = _txt.lower()
        _txt = _txt.replace(' ','') #공백제거
        _txt = re.sub( '[^A-Za-z0-9가-힣\s]', "", _txt) # 한글 숫자 영문만 사용 나머지 제거
        if _txt != '':
            if len(re.sub('[^0-9]' ,'' , _txt)) <= 5:
                _rt.append( _txt )

    # 숫자만 , 숫자원 단어는 뒷자리 제외 , 순수한글일경우 4글자만 사용
    for txt in _rt:        
        if( '기간' in  txt or '사용' in  txt or '유효' in txt ):
            break
        elif ( len(txt) <=1 ):
            print('제외',txt)        
        elif ( '교환' in txt or '제휴' in txt or '수량' in txt):
            print('제외',txt)        
        elif ( len( re.findall( '\d+만' ,txt ) ) >=1 ):
            _str = re.findall( '\d+만' ,txt )[0]
            _fin_txt.append( txt[0: _str.find(_str)+len(_str) ] )
        elif ( len( re.findall( '\d+원' ,txt ) ) >=1 ):
            _str = re.findall( '\d+원' ,txt )[0]
            _fin_txt.append( txt[0: _str.find(_str)+len(_str) ] )            
        elif len(re.sub( '[a-z0-9]','', txt )) >2:
            if ('만' in txt or '원'  in txt) :
                _fin_txt.append(txt)
            elif len(txt) >= 5:
                _fin_txt.append( txt[1:-1] )           
            else :
                _fin_txt.append(txt)
    return _fin_txt
    




def image_classification( _files ):
    '''인식'''
    try:
        __ocr = PaddleOCR(lang="korean" )               
        files = _files
        for file in files:
            i = base_root+'\\'+file
            text = getText( __ocr , i)
            fold_nm = '_'.join(text)      
            print('파일정보 : ', i ,' , ', fold_nm)
            if len(fold_nm) > 5:
                mk_fold( fold_nm ) # 폴더 생성
                mv_file( file , fold_nm )          

    except Exception as e:
        print('image_classification ==> ', e)



def main():
    rootlist = os.listdir(base_root)        
    files = [X for X in rootlist if os.path.isfile(base_root+'\\'+X)]
    n = int( round(len(files) / 4,0) )
    list_chunked = [files[i:i+n] for i in range(0, len(files), n)]    

    start = int(time.time())
    num_cores = 4
    pool = Pool(num_cores)
    print(pool.map( image_classification ,list_chunked ))
    print("***run time(sec) :", int(time.time()) - start)

  

if __name__ == "__main__":
    main()


