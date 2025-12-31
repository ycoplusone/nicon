import re
from datetime import date,datetime
import cv2
import numpy as np
import pytesseract
from  pathlib import Path
import pandas as pd
import os
import shutil
import lib.util as w2ji
import lib.dbcon as dbcon

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_expiry_date_flexible(image_path: str , brand) -> str :
    #img = cv2.imread(image_path)
    data = np.fromfile(image_path, dtype=np.uint8)
    img = cv2.imdecode(data ,  cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
 

    custom_config = r"--oem 3 --psm 6"
    data = pytesseract.image_to_data(th, lang="kor+eng", output_type=pytesseract.Output.DICT , config=custom_config)

    # 전체 텍스트 먼저 파싱 시도
    full_text = " ".join([t for t in data["text"] if t and t.strip()])
    full_text = full_text.replace(' ','')
    matched = [
        word for word in brand
        if word in full_text
    ]    
    return matched



if __name__ == "__main__":
    '''
    Tesseract 설치 파일 경로 : https://github.com/UB-Mannheim/tesseract/wiki
    나머지는 실행하면서 lib를 추가 하자.
    '''   
    __ver = '0.1'
    __comment = '기프티콘 브랜드 분류'
    print(__ver , __comment)
    __brand = ['교보문고','카카오페','농협상품','다이소','올리브영','뚜레쥬르','배스킨라','크리스피','파리바게','배달의민','본죽','메가','스타벅','이디야','컴포즈커','투썸플레','파스쿠찌','폴바셋','CU','GS25','세븐일레','BBQ','BHC','교촌치킨','깐부치킨','롯데리아','맘스터치','멕시카나','버거킹','푸라닭','피자헛','네이버페이']
    __root_path = 'C:\\Users\\DLIVE\\Documents\\카카오톡 받은 파일\\test'

    __list      = os.listdir( __root_path )
    '''
    files = [
        f for f in os.listdir(__root_path)
        if os.path.isfile(os.path.join(__root_path, f))
    ]  
    '''
    files = sorted(
        [
            f for f in os.listdir(__root_path)
            if os.path.isfile(os.path.join(__root_path, f))
        ],
        key=lambda x: x.lower(),
        reverse=False
    )    

    #temp_list   = [ X for X in files if os.path.isdir(__root_path+'\\'+X)]
    for i in files:
        ss = f'{__root_path}\\{i}'        
        aa = extract_expiry_date_flexible(ss , __brand)
        print(ss , aa)
        if len(aa) ==1:
            _path = f'{__root_path}\\{aa[0]}'
            _path2 = f'{__root_path}\\{aa[0]}\\{i}'
            folder_path = Path(_path )
            if not folder_path.exists():
                folder_path.mkdir(parents=True)
                
            shutil.move( ss , _path2 ) # 이동
   