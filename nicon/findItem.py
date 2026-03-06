import base64
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
import random
import time
from datetime import datetime
from pytz import timezone
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import pytesseract
from PIL import Image

from tqdm import tqdm
import lib.dbcon as dbcon
import re
import lib.util as w2ji


class Search():
    ''''''
    __dbconn = ''

    def __init__(self):
        self.__dbconn     = dbcon.DbConn() #db연결    
    
    def upscale_and_sharpen(self, img_obj , scale_factor=3):
        """
        이미지를 확대하고 선명하게 보정하는 함수
        """
        # 1. Lanczos 필터를 사용해 고화질 확대 (Pillow 이용)
        width, height = img_obj.size
        new_size = (width * scale_factor, height * scale_factor)
        upscaled_img = img_obj.resize(new_size, Image.LANCZOS)

        # 2. 선명도 보정을 위해 OpenCV 형식으로 변환 (RGB -> BGR)
        #open_cv_img = cv2.cvtColor(np.array(upscaled_img), cv2.COLOR_RGB2BGR)

        # 3. 언샤프 마스크(Unsharp Mask) 적용
        # 이미지를 약간 흐리게 만든 뒤 원본에서 빼서 경계선만 강조하는 방식이야
        #gaussian_blur = cv2.GaussianBlur(open_cv_img, (0, 0), 2.0)
        #sharpened = cv2.addWeighted(open_cv_img, 1.5, gaussian_blur, -0.5, 0)

        # 4. 결과 반환 (OpenCV -> Pillow)
        #final_img = Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))
        return upscaled_img

    def detect_qr_logic(self , image_obj):
        """
        확대 보정된 이미지에서 QR코드를 검출하고 내용을 반환함
        """
        # 1. PIL 객체를 OpenCV 형식으로 변환
        img = cv2.cvtColor(np.array(image_obj), cv2.COLOR_RGB2BGR)
        
        # 2. 그레이스케일 변환 (인식률 향상을 위한 필수 단계)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 3. 이진화(Thresholding) 처리
        # 픽셀을 명확하게 흑과 백으로 나눠 QR 패턴을 도드라지게 함
        _, thr = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        # 4. QR코드 디코딩
        decoded_objects = decode(thr)
        
        if not decoded_objects:
            # 이진화 없이 원본 그레이스케일로 한 번 더 시도 (보험)
            decoded_objects = decode(gray)

        results = False
        for obj in decoded_objects:
            # 데이터 디코딩 (UTF-8)            
            qr_data = obj.data.decode('utf-8')
            qr_type = obj.type
            
            # QR코드의 위치(사각형 좌표)도 함께 추출 가능해
            (x, y, w, h) = obj.rect
            '''
            print(f"✅ 검출 성공! [{qr_type}] 내용: {qr_data}")
            results.append({
                "data": qr_data,
                "location": (x, y, w, h)
            })
            '''
            results = True
            
        return results    

    def check_target_words(self , image_obj , targets ):
        """
        이미지 객체에서 '설문' 또는 '만족' 단어가 포함되어 있는지 판별함
        """
        # 1. OCR 인식률을 높이기 위한 전처리 (OpenCV 활용)
        # 이미지를 흑백으로 바꾸고 대비를 높여 글자를 뚜렷하게 해
        img = cv2.cvtColor(np.array(image_obj), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 노이즈 제거 및 이진화
        processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # 2. Tesseract로 텍스트 추출
        # lang='kor+eng'로 설정해야 한글과 영어를 동시에 인식해
        custom_config = r'--oem 3 --psm 6' # OEM 3: 최신 엔진, PSM 6: 단일 텍스트 블록 가정
        extracted_text = pytesseract.image_to_string(processed_img, lang='kor+eng')
        
        # 3. 특정 단어 포함 여부 확인
        # 공백과 줄바꿈을 제거해서 검색 정확도를 높여
        clean_text = extracted_text.replace(" ", "").replace("\n", "")
        
        
        found_words = [word for word in targets if word in clean_text]

        if found_words:
            #print(f"✅ 단어 검출 성공: {found_words}")
            return True
        else:
            #print("❌ 대상 단어를 찾지 못했습니다.")
            return False
    
    def text2img( self , base64_data:str ):
        '''이미지데이터를 이미지화 시킴'''
        try:
            # 2. 앞부분의 헤더(data:image/jpeg;base64,)를 제거하고 순수 데이터만 추출
            if "," in base64_data:
                base64_str = base64_data.split(",")[1]
            else:
                base64_str = base64_data

            # 3. 디코딩하여 이진 데이터(Bytes)로 변환
            img_bytes = base64.b64decode(base64_str)

            # 4. 메모리 내에서 이미지 객체로 생성
            img = Image.open(BytesIO(img_bytes))

            # 5. 결과 확인 (이미지를 띄워보거나 저장 가능)
            #img.show()
            sharpened_img = self.upscale_and_sharpen(img, scale_factor=4) #확대보정               
            return sharpened_img
        except:
            return ''

    def get_google_images_no_api(self , keyword , target_keywords):
        chrome_options = Options()
        # 차단 방지를 위한 설정
        chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
        chrome_options.add_argument('--headless')       
        driver = webdriver.Chrome(options=chrome_options)        
        
        # 최근 1일(qdr:d) 옵션이 포함된 검색 URL
        search_url = f"https://www.google.com/search?q={keyword}&tbm=isch&tbs=qdr:d"
        driver.get(search_url)
        time.sleep(3) # 로딩 대기
        self.__dbconn     = dbcon.DbConn() #db연결 재연결        
        except_word       = self.__dbconn.get_db_word_list('nicon_survey_exception_list','word') # 제외 url 리스트

        eles = driver.find_elements(By.CSS_SELECTOR, "div.eA0Zlc")
        
        results = []
        print(f"검색어[{keyword}] 총 {len(eles)}개의 항목을 찾았어.")
        cnt = 0
        for i, el in tqdm(enumerate(eles, 1) , desc='데이터 수집중.......'):
            try:
                alt_text = el.find_element(By.TAG_NAME, "img").get_attribute("alt")
                alt_text = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', alt_text)
            except:
                alt_text = ""

            try:
                img_src = el.find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                img_src = ""
            
            try:
                imgurl = el.get_attribute("data-lpage")
            
            except:
                imgurl = ""
            
            img  = "" if img_src == "" else self.text2img(img_src)
            qr0  = False if img == "" else self.detect_qr_logic(img)
            tx1  = False if img == "" else self.check_target_words(img , target_keywords )
            txt  = [word for word in target_keywords if word in alt_text]
            tx2  = True if txt else False
            __temp = {'url' : imgurl , 'description':alt_text[0:128] , 'has_qr':qr0 , 'has_text_survey':tx1 , 'has_text_satisfaction':tx2 , 'words':keyword}            
            if ( qr0 or tx1 or tx2 ):
                if any(word in imgurl for word in except_word):
                    pass
                else:   
                    cnt += 1
                    self.__dbconn.upsert_nicon_survey_collection(__temp)
        print(f"검색어[{keyword}] 의 처리는 {cnt}건 입니다.")

    
if __name__ == "__main__":   
    ''''''
    ss = Search()
    _check_time = w2ji.getNowDate()                   # 현재 시간

    
    while(True):
        _msg_sned_flag = w2ji.get1HourOver( _check_time )
        dd = dbcon.DbConn()
        target_keywords = dd.get_db_word_list('nicon_target_words','word') # 이미지 혹은 이미지의 설명에 해당 단어가 포함되는지 확인
        keywords_list   = dd.get_db_word_list('nicon_search_keywords','keyword') # 검색할 키워드 리스트 반드시 "" 안에 문자를 넣어야 한다.
                
        for word in keywords_list:
            ss.get_google_images_no_api( word , target_keywords )
            wait_time = random.randint(60, 300)
            print(f"{_check_time} |||| 다음 단어 검색까지 {wait_time // 60}분 {wait_time % 60}초 대기합니다...")
            time.sleep(wait_time)

        if ( _msg_sned_flag ):    # 마지막 메세지 발송후 1시간 이상 되면 다시 텔레그램 메세지를 발송한다.
            _check_time = w2ji.getNowDate()         # 메세지 발송 시간을 다시 등록한다.
            w2ji.send_telegram_message(  f'설문 수집 프로그램 정상 동작중 ' )      
        print(f"{datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')} ⏳ 다음 수집까지 2시간 대기합니다...")
        time.sleep(7200)
        