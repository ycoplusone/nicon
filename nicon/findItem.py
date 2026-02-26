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
        # 1. 네가 가져온 'data:image/jpeg;base64,...' 문자열
        #base64_data = "data:image/jpeg;base64,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"

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

        eles = driver.find_elements(By.CSS_SELECTOR, "div.eA0Zlc")
        
        results = []
        print(f"검색어[{keyword}] 총 {len(eles)}개의 항목을 찾았어.")
        '''
        chunk_embeddings_dict = {
            size : rc.ch3_create_embeddings( chunks )
            for size , chunks in tqdm(text_chunks_dict.items() , desc='임베딩생성중')
        }
        '''
        for i, el in tqdm(enumerate(eles, 1)):
            # 1. 태그 사이에 있는 순수 텍스트 추출
            
            # 3. 만약 내부 img 태그의 alt 값을 보고 싶다면
            try:
                alt_text = el.find_element(By.TAG_NAME, "img").get_attribute("alt")
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
            
            img = self.text2img(img_src)
            qr0  = self.detect_qr_logic(img)
            tx1  = self.check_target_words(img , target_keywords )
            txt  = [word for word in target_keywords if word in alt_text]
            tx2  = True if txt else False
            __temp = {'url' : imgurl , 'description':alt_text[0:128] , 'has_qr':qr0 , 'has_text_survey':tx1 , 'has_text_satisfaction':tx2}            
            if ( (qr0 or tx1 or tx2) and "instagram" in imgurl ):
                self.__dbconn.upsert_nicon_survey_collection(__temp)

    
if __name__ == "__main__":   
    ''''''
    ss = Search()
    target_keywords = ["설문", "만족"] # 이미지 혹은 이미지의 설명에 해당 단어가 포함되는지 확인
    
    keywords_list = ['"설문 조사"'] # 검색할 키워드 리스트 반드시 "" 안에 문자를 넣어야 한다.
    while(True):
        for word in keywords_list:
            ss.get_google_images_no_api( word , target_keywords )
            wait_time = random.randint(60, 300)
            print(f"⏳ 다음 단어 검색까지 {wait_time // 60}분 {wait_time % 60}초 대기합니다...")
            time.sleep(wait_time)
        
        print(f"{datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')} ⏳ 다음 수집까지 2시간 대기합니다...")
        time.sleep(7200)

        