# -*- coding: utf-8 -*-

import lib.dbcon as dbcon
import lib.util as w2ji
from tqdm import tqdm
import time
from datetime import datetime , timedelta
from pytz import timezone
from apify_client import ApifyClient
import re
import requests
from PIL import Image
from io import BytesIO
import os
import numpy as np
import pytesseract
import cv2
from pyzbar.pyzbar import decode
from urllib.parse import urlparse, parse_qs , unquote 
from playwright.sync_api import sync_playwright
import random
import holidays
import sys
import logging
import pandas as pd
import easyocr
import json
from datetime import datetime
import urllib.request
import urllib.error


class Search():
    ''''''
    __dbconn    = None
    __log       = None
    
    def __init__(self):
        self.__dbconn = dbcon.DbConn() #db연결      
        self.__log = self.setup_logger() #로그파일 연결
    
    def setup_logger(self , log_filename=r'D:\python_workspace\nicon\finditem.log'):
        """로그 설정을 초기화하고 로그용 함수를 반환합니다."""
        # 1. 로거 생성
        logger = logging.getLogger("MyLogger")
        logger.setLevel(logging.INFO)
        
        # 중복 등록 방지
        if not logger.handlers:
            # 2. 파일 저장 핸들러 설정 (utf-8 인코딩으로 한글 깨짐 방지)
            file_handler = logging.FileHandler(log_filename, encoding="utf-8")
            
            # 3. 로그 포맷 설정 (시간 [로그레벨] 메시지)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y%m%d %H:%M')
            file_handler.setFormatter(formatter)
            
            # 4. 로거에 핸들러 추가
            logger.addHandler(file_handler)
            
            # (선택사항) 터미널 콘솔창에도 동시에 print하고 싶다면 아래 주석을 해제하세요.
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)            
        return logger.info

    def getGeminiProcess(self , event_text: str , max_retries: int = 4) -> str:
        # 1. API 키 확인
        api_key = os.environ.get('google_gemini_api_key')

        # 3. 오늘 날짜 및 프롬프트 구성
        today_str = datetime.now().strftime("%Y년 %m월 %d일")
        prompt = f"""당신은 이벤트 및 리서치 공고 분석 전문가입니다.
                    제공된 [이벤트 텍스트]를 면밀히 분석하여 아래 3가지 핵심 조건의 충족 여부를 판별하고 지정된 서식에 맞춰 답변해 주세요.

                    ---

                    ### [기준 시점]
                    * 오늘 날짜: {today_str}

                    ---

                    ### [분석할 이벤트 텍스트]
                    {event_text}

                    ---

                    ### [판별 기준]
                    1. **증정품 유무**: 기프티콘, 상품권, 리워드 등 참여 완료 시 제공하는 실질적 혜택이 존재하는지 확인합니다.
                    2. **대상자 요건 (선착순 50명 이상 또는 전원)**:
                    - 참여 요건을 갖춘 '참여자 전원'에게 지급하는지 확인합니다.
                    - '선착순' 지급인 경우, 인원이 '50명 이상'인지 확인합니다.
                    - 추첨 방식이거나 선착순 50명 미만인 경우 '미충족'으로 분류합니다.
                    3. **기간 만료 유무**:
                    - [기준 시점]의 오늘 날짜를 기준으로 모집/참여 기간이 남아 있는지 확인합니다.
                    - 텍스트 내에 연도 표기가 생략된 경우 올해를 기준으로 판단합니다.

                    ---

                    ### [출력 형식]
                    반드시 다른 설명 없이 아래 형식만 출력하세요:
                    * **증정품 유무**: [있음 / 없음] - (증정품 명칭 기재)
                    * **지급 대상 요건**: [충족 / 미충족] - (전원 지급 / 선착순 00명 / 추첨 / 선착순 50명 미만 등 구체적 사유 기재)
                    * **기간 만료 여부**: [진행중 / 만료 / 불가] - (안내된 일정 및 만료 사유 기재)
                    * **최종 판정**: [True / False]
                    """

        # 4. HTTP 요청 페이로드 설정
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "has_reward": {
                            "type": "STRING", 
                            "enum": ["있음", "없음"],
                            "description": "증정품 유무"
                        },
                        "reward_name": {
                            "type": "STRING",
                            "description": "증정품 명칭 (없으면 '없음')"
                        },
                        "target_status": {
                            "type": "STRING", 
                            "enum": ["충족", "미충족"],
                            "description": "지급 대상 요건 충족 여부"
                        },
                        "target_reason": {
                            "type": "STRING",
                            "description": "전원 지급, 선착순 N명, 추첨 등 구체적 사유"
                        },
                        "period_status": {
                            "type": "STRING", 
                            "enum": ["진행중", "만료", "불가"],
                            "description": "기간 진행 여부"
                        },
                        "period_reason": {
                            "type": "STRING",
                            "description": "안내된 일정 및 만료 사유"
                        },
                        "final_verdict": {
                            "type": "BOOLEAN",
                            "description": "최종 통과 여부"
                        }
                    },
                    "required": [
                        "has_reward", "reward_name", 
                        "target_status", "target_reason", 
                        "period_status", "period_reason", 
                        "final_verdict"
                    ]
                }
            }
        }

        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}

        candidate_models = ["gemini-3.1-flash-lite","gemini-flash-latest"]
        detail_ai       = 0  # 판단 1/0
        detail_comment  = '' # 판단 근거    
        for model_name in candidate_models:     
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

            for attempt in range(1, max_retries + 1):
                req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                try:
                    with urllib.request.urlopen(req) as response:
                        res_json = json.loads(response.read().decode("utf-8"))
                        result_str = res_json["candidates"][0]["content"]["parts"][0]["text"]
                        #return json.loads(result_str)
                        json_data       = json.loads(result_str)
                        detail_ai       = 1 if json_data["final_verdict"] else 0 # 최종 판정 True/False를 1/0으로 변환
                        detail_comment  = f"{json_data['reward_name']}|{json_data['target_reason']}|{json_data['period_reason']}"                       
                        break                   

                except urllib.error.HTTPError as e:
                    # 503(과부하) 또는 429(속도제한) 발생 시 재시도
                    print(f" 발생오류 {e.code } {e.reason }")
                    if e.code in (503, 429):
                        wait_time = attempt * 2  # 대기 시간을 1초씩 증가 최대 4초쯤됨.
                        print(f"[{model_name}] 서버 혼잡 (HTTP {e.code}). {wait_time}초 후 재시도 ({attempt}/{max_retries})...")
                        time.sleep(wait_time)
                    else:
                        error_body = e.read().decode("utf-8")
                        raise RuntimeError(f"API 호출 실패 (HTTP {e.code}): {error_body}")
            if detail_comment != '': # 최종 판정이 True이면 더 이상 다른 모델을 시도하지 않음
                break

        return detail_ai, detail_comment

    def getWeekGroup(self):
        ''' ver4 사용
        현재 날짜를 기준으로 해당 월의 평일을 4일 단위로 그룹화하고, 현재 날짜가 속한 그룹 번호를 반환하는 함수'''
        # 해당 월의 모든 날짜 생성
        year    = datetime.now(timezone('Asia/Seoul')).year
        month   = datetime.now(timezone('Asia/Seoul')).month
        today   = datetime.now(timezone('Asia/Seoul')).date()    
        #today   = datetime(2026, 8, 17, 14, 30, 0, tzinfo=timezone('Asia/Seoul')).date()  # 테스트용으로 특정 날짜 설정
        dates   = pd.date_range(f'{year}-{month:02d}-01', periods=pd.Period(f'{year}-{month:02d}').days_in_month, freq='D')               
        weekdays = dates[dates.dayofweek < 5] # 평일만 필터링
        groups = [weekdays[i:i+4].tolist() for i in range(0, len(weekdays), 4)] # 4일마다 그룹화
        group_number = None
        for idx, group in enumerate(groups, 0):
            if any(date.date() == today for date in group):
                group_number = idx
                break        
        return group_number    
    
    def get_month_week_simple(self , date_str):
        ''' ver4 사용'''
        target_date = datetime.strptime(date_str, "%Y%m%d")
        
        # 해당 월의 1일 날짜와 요일 구하기
        first_day = target_date.replace(day=1)
        
        # 일요일=0, 월요일=1, ..., 토요일=6으로 변환 (target_date.weekday()는 월요일이 0임)
        # 일요일 시작 기준으로 맞추기 위해 계산을 조정합니다.
        first_day_weekday = (first_day.weekday() + 1) % 7
        
        # (현재 날짜 + 1일의 요일 index - 1) // 7 + 1
        week_of_month = (target_date.day + first_day_weekday - 1) // 7 + 1
        
        return week_of_month

    def get_date_info(self , date_str):
        """ ver4 사용
        "yyyymmdd" 형식의 날짜를 입력받아 휴일 여부, 전일 휴일 여부, 주차 정보를 반환합니다.
        """
        # 1. 날짜 문자열을 datetime 객체로 변환
        target_date = datetime.strptime(date_str, "%Y%m%d")
        
        # 2. 한국 공휴일 지정 (지정하지 않으면 기본적으로 해당 연도의 공휴일 생성)
        kr_holidays = holidays.KR(years=target_date.year)
        
        # 전일(하루 전) 날짜 계산
        prev_date = target_date - timedelta(days=1)
        # 전일의 연도가 다를 수 있으므로 전일 연도의 공휴일도 함께 고려
        if prev_date.year != target_date.year:
            kr_holidays.update(holidays.KR(years=prev_date.year))

        # 3. 휴일 여부 판단 함수 (주말이거나 공휴일이면 True)
        def is_holiday_or_weekend(dt):
            # dt.weekday() -> 5: 토요일, 6: 일요일
            is_weekend = dt.weekday() in [5, 6]
            is_public_holiday = dt in kr_holidays
            return is_weekend or is_public_holiday

        # 4. 결과값 계산
        is_target_holiday = is_holiday_or_weekend(target_date)
        is_prev_holiday = is_holiday_or_weekend(prev_date)
        
        # 주차 계산 (ISO 주차 기준: dt.isocalendar()[1])
        # 만약 '해당 월의 몇 번째 주'인지 구하고 싶다면 다른 계산이 필요합니다. 여기서는 '연 기준 주차'입니다.
        week_of_year = self.get_month_week_simple(date_str)

        # 5. 결과 반환
        return {
            "today": is_target_holiday,
            "yesterday": is_prev_holiday,
            "week_cnt": week_of_year
        }

    def get_image_from_url(self, url):
        '''ver4 이미지 url를 통해 이미지 객체를 반환함'''
        try:
            print(url)
            # 1. stream=True로 설정하여 헤더만 먼저 가져옴 (네트워크 비용 절약)
            response = requests.get(url, stream=True, allow_redirects=True, timeout=5)
            
            # 상태 코드 확인
            if response.status_code != 200:
                print(f"요청 실패 (Status Code: {response.status_code})")
                return ''
                
            content_type = response.headers.get('Content-Type', '')         
            
            # CloudFront 등이 application/octet-stream을 줄 경우를 대비해
            # 확장자가 .jpg, .png 등인지도 함께 체크해주면 더 안전합니다.
            is_image_type = content_type.startswith('image/') or any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp'])
            
            if not is_image_type:
                print(f"이미지 URL이 아닙니다. (Content-Type: {content_type})")
                return ''        
                
            # 2. 이미지임이 확인되면 실제 데이터(바디) 다운로드
            image_data = Image.open(BytesIO(response.content))
            return image_data
                    
        except Exception as e:
            print(f"에러 발생: {e}")
            return ''    
        
    def detect_qr_logic(self , image_obj):
        """ ver4
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

    def getImgText2(self , image_obj):
        ''' ver4
        이미지에서 텍스트를 추출하는 함수
        '''
        img = cv2.cvtColor(np.array(image_obj), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 노이즈 제거 및 이진화
        processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]        
        
        reader      = easyocr.Reader(['ko', 'en'])
        results     = reader.readtext( processed_img  )
        full_text   = ""
        for detection in results:
            text = detection[1]
            confidence = detection[2]
            #print(f"{text} (확률: {confidence:.2%})")    
            full_text += text
        full_text   = full_text.replace(" ", "").replace("\n", "")        
        return full_text                

    def check_target_words(self , clean_text , targets , except_word ):
        """ ver4 에서도 사용
        이미지 객체에서 targets 단어가 포함되어 있는지 판별함
        , 이미지 객체에 except_word 가 포함되어 있는지 판별.
        """        
        # 3. 특정 단어 포함 여부 확인 공백과 줄바꿈을 제거해서 검색 정확도를 높여
        found_words = [word for word in targets if word in clean_text]
        found_except_words = [word for word in except_word if word in clean_text]
        if found_words and not found_except_words:            
            return True  #print(f"✅ 단어 검출 성공: {found_words}")
        else:            
            return False  #print("❌ 대상 단어를 찾지 못했습니다.")

    def getURLCapture(self , url , save_path="screenshot.png"):
        '''ver4 url 캡쳐         '''
        with sync_playwright() as p:
            # 브라우저 실행 (좌표를 눈으로 확인하기 위해 headless=False 추천)
            browser         = p.chromium.launch(headless=True)
            
            # 뷰포트(화면 크기)를 고정해야 좌표가 틀어지지 않습니다.
            window_width    = 1024
            window_height   = 1536
            context         = browser.new_context( viewport={"width" : window_width , "height" : window_height } )
            page            = context.new_page()

            print(f"{url} 페이지로 이동 중...")
            page.goto(url)
            
            # 페이지 로드 및 팝업 애니메이션 대기
            page.wait_for_load_state("networkidle")
            time.sleep(2.5) 

            # [핵심 로직] URL에 instagram이 포함되어 있으면 지정한 좌표 클릭
            if "instagram" in url.lower():
                # 💡 모니터나 브라우저 크기에 맞게 닫기 버튼 위치(좌표)를 입력하세요.
                # 예시: 가로 900 픽셀, 세로 200 픽셀 위치 클릭
                click_x = 1 
                click_y = 1                
                try:
                    # 해당 좌표를 마우스로 직접 클릭
                    page.mouse.click(click_x, click_y)
                    print("좌표 클릭 완료.")
                    time.sleep(1) # 클릭 후 팝업이 닫히는 시간 대기
                except Exception as e:
                    print(f"좌표 클릭 중 오류 발생: {e}")

            page.screenshot(path=save_path, full_page=False)
            browser.close()   

    def getImgQr(self,save_path="screenshot.png"):
        ''' ver4 이미지에서 Qr코드 여부롤 검출함     '''
        chk_qr = False # QR코드 식별
        try :            
            img = Image.open(save_path)    # 3. 이미지 로드
            
            qr_results = decode(img)  # 5. QR 코드 추출
            #print("\n--- [추출된 QR 코드 정보] ---")
            if qr_results:
                for qr in qr_results:                    
                    chk_qr = True # QR코드 식별
            return chk_qr
        except Exception as e:
            print(f"QR 코드 검출 중 오류 발생: {e}")
            return False

    def getImgTxt(self,save_path="screenshot.png"):
        ''' ver4이미지에서 텍스트 추출        '''
        reader      = easyocr.Reader(['ko', 'en'])
        results     = reader.readtext(save_path)
        full_text   = ""
        for detection in results:
            text = detection[1]
            confidence = detection[2]
            #print(f"{text} (확률: {confidence:.2%})")    
            full_text += text
        full_text   = full_text.replace(" ", "").replace("\n", "")        
        return full_text

    def getTextAnalysis(self,text_data , targets , except_word):
        ''' ver4 텍스트 분석 단어가 검출되면 True 반환        '''
        chk_txt             = False
        found_words         = [word for word in targets if word in text_data]            
        found_except_words  = [word for word in except_word if word in text_data]                        
        if( found_words and not found_except_words ):
            chk_txt = True
        return chk_txt       

    def getApifyData(self , api_key , holiyyesterday , keyword:str ):
        ''' ver4 damilo/google-images-scraper 액터를 사용하여 구글 이미지 검색 결과를 가져오는 함수 '''
        results     = [] # 반환 함수
        APIFY_TOKEN = api_key # 1. 본인의 Apify API 토큰 입력               
        client      = ApifyClient(APIFY_TOKEN) # 클라이언트 초기화

        # 2. damilo/google-images-scraper 가 요구하는 입력값 설정
        run_input = {
            "country"       : "kr",
            "date_range"    : holiyyesterday , # w 일주일 , d 하루
            "language"      : "ko",
            "max_pages"     : 1,
            "num"           : "100",
            "query"         : keyword           # 검색어
        }
        try:            
            run = client.actor("damilo/google-images-scraper").call(run_input=run_input)    # 3. damilo의 구글 이미지 스크래퍼 액터 실행
            dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items      # 4. 결과가 저장된 데이터셋(Dataset)에서 데이터 가져오기            
            self.__log( f"[{keyword}] 키워드로 구글 이미지 검색하여 총{len(dataset_items)}개의 이미지를 찾았습니다.") # 5. 수집된 결과 출력 및 가공
            
            for  item in tqdm(dataset_items , desc='\추출중.......'):
                # 대개 구글 이미지 스크래퍼는 imageUrl, altText, title 등의 Key를 반환합니다.            
                title           = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', item.get("title", '') )
                img_url         = item.get("imageUrl",'')
                thumbnailUrl    = item.get('thumbnailUrl','')
                link            = unquote( item.get('link','') ) # unquote 한글 처리 한다.
                __temp_data     = { 'title' : title , 'url' : link , 'img_url' : img_url , 'thumbnail_url' : thumbnailUrl }
                results.append( __temp_data )            
            time.sleep(0.5)            
        except Exception as e:
            self.__log( f" 크롤링 중 오류가 발생했습니다: {e}" )   
        return results       

    def getDataProcess(self , results , keyword:str , target_keywords = [] , except_word = [] ):
        ''' ver4 수집된 결과를 처리하는 함수 '''
        totproc = 0 # 처리건수
        totsucc = 0 # 성공건수
        totfail = 0 # 실패건수
        try:
            for result in tqdm( results , desc=f'처리중 => ' , leave=False):
                url             = result['url']
                img_src         = result['img_url']
                thumbnail_src   = result['thumbnail_url']
                alt_text        = result['title']
                alt_text_chk    = alt_text.replace(' ','').replace("\n", "") # 공백제거한 내용 데이터 검출을 위한 내용
                url_chk         = self.__dbconn.get_nicon_survey_url_chk( {'url':url} ) # 미등록 0 등록 1 0만 처리한다.

                # url 에서 확장자 추출
                _, ext      = os.path.splitext(url)
                ext         = ext.lower()

                # 3. 확장자 그룹 정의
                extension_map = {'.pdf': 'PDF 문서','.txt': '텍스트 파일','.xlsx': '엑셀(Excel) 파일','.xls': '엑셀(Excel) 파일','.csv': '엑셀(CSV) 파일','.hwp': '한글(HWP) 파일','.hwpx': '한글(HWPX) 파일','.pptx': '파워포인트(PPT) 파일','.ppt': '파워포인트(PPT) 파일'}

                url_pdf     = True if ext in extension_map else False # 이상 확장자 검출
                
                img         = "" if img_src == "" else self.get_image_from_url(img_src) # 이미지 생성
                if img == '':
                    img = self.get_image_from_url(thumbnail_src)

                qr0         = False  if img == "" else self.detect_qr_logic(img)    # 이미지내 qr 검출
                clear_text  = self.getImgText2(img) if img != "" else "" # 이미지내 텍스트 추출
                tx1         = False if clear_text == "" else self.check_target_words( clear_text , target_keywords , except_word ) # 이미지내 단어 검출
                txt         = [word for word in target_keywords if word in alt_text_chk] #설명단어 정리
                tx2         = True if txt else False # 설명문에 단어 검출                
                __temp = {'url' : url , 'description':alt_text[0:128] , 'has_qr':qr0 , 'has_text_survey':tx1 , 'has_text_satisfaction':tx2 , 'words':keyword}            
                
                self.__log( f" {'*' * 40} " )
                self.__log( f" url : {url}" )

                if( url_chk >= 9 ):                    
                    self.__dbconn.upsert_nicon_survey_collection(__temp) # 검색어만 업데이트 한다.  
                    self.__log( f'※ 이미등록건[ url_chk:{url_chk} ]' )
                elif( (url_pdf == True) or any(word in alt_text_chk for word in except_word) ): # PDF 파일이면 제외한다.                    
                    totfail += 1 # 실패 건수 등록
                    self.__dbconn.upsert_nicon_survey_worst_url_list(param=__temp) # 제외 url에 넣는다.
                    self.__log( f'※ url 이상건 & 설명에 금지단어 검출 [url_pdf:{url_pdf} , alt_text_chk:{any(word in alt_text_chk for word in except_word)}]' )
                else:
                    chk_qr      = False
                    chk_txt     = False
                    detail_ai   = 0
                    detail_comment  = ''
                    try:
                        self.getURLCapture(url=url , save_path="screenshot.png") # url 캡쳐
                        chk_qr      = self.getImgQr(save_path="screenshot.png") # 캡쳐된 이미지에서 qr 검출
                        full_text   = self.getImgTxt(save_path="screenshot.png") # 캡쳐된 이미지에서 텍스트 추출
                        chk_txt     = self.getTextAnalysis(text_data=full_text , targets=target_keywords , except_word=except_word ) # 캡쳐된 이미지에서 텍스트 분석
                        detail_ai , detail_comment = self.getGeminiProcess(full_text) # 캡쳐된 이미지에서 텍스트 분석 AI 판단
                        self.__log( f" {full_text} " ) # 캡쳐된 이미지에서 텍스트 출력
                    except Exception as e:
                        self.__log( f"※ 2단계 처리중 오류발생 : {e}" )
                    if (chk_qr or chk_txt or detail_ai == 1): # QR코드 검출 or 텍스트 검출 or AI 판단이 True이면 등록
                        totsucc += 1 # 성공건수 등록             
                        self.__dbconn.upsert_nicon_survey_collection( __temp ) # 등록
                        __tempdd = {'url' : url , 'chk_qr' : chk_qr , 'chk_txt' : chk_txt , 'detail_ai' : detail_ai , 'detail_comment' : detail_comment } # 상세 등록
                        self.__dbconn.upsert_nicon_survey_detail( param=__tempdd )                            
                        self.__log( f"※ 성공 등록2 [ qr:{qr0} , 썸네일:{tx1} , 설명:{tx2} , 상세qr:{chk_qr} , 상세txt:{chk_txt} , ai:{detail_ai} , 추론근거:{detail_comment} ]" )
                    else:
                        totfail += 1 # 실패 건수 등록
                        self.__dbconn.upsert_nicon_survey_worst_url_list(param=__temp) # 제외 url에 넣는다. 
                        self.__log( f"※ 2단계 아무것도 검출안됨[chk_qr:{chk_qr} , chk_txt:{chk_txt} , ai:{detail_ai} , 추론근거:{detail_comment} ]" )
                    

            return totproc , totsucc , totfail
        except Exception as e:
            print(f'추출데이터 처리:{e}')
    

    def get_db_words(self,table,where):
        '''db에서 데이터 배열 가져오기'''
        return self.__dbconn.get_db_word_list(table,where)


    def exec(self):
        ''' 메인 실행 부분'''
        try:
            api_keys = [os.environ.get('apify0') , 
                        os.environ.get('apify1') ,
                        os.environ.get('apify2') ,
                        os.environ.get('apify3') ,
                        os.environ.get('apify4') ,
                        os.environ.get('apify9') 
                        ] # 향후 3~4개 키워드 검색후 다른 api를 이용하도록 수정한다.
            today   = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
            
            self.__log( f" Begin - {'='*30}  " )

            chk_day             = self.get_date_info(today)
            today_holi_flag     = chk_day.get('today',False)        #당일 휴일 여부
            yesterday_holi_flag = 'qdr:w' if chk_day.get('yesterday',False) == True  else 'qdr:d'    #어제 휴일 여부
            today_week          = self.getWeekGroup() #chk_day.get('week_cnt',1)-1        #주차 
            keywords_list       = self.get_db_words('nicon_search_keywords','keyword') # 검색할 키워드 리스트 반드시 "" 안에 문자를 넣어야 한다. 검색리스트    
            target_keywords     = self.get_db_words('nicon_target_words','word') # 이미지 혹은 이미지의 설명에 해당 단어가 포함되는지 확인        
            except_word         = self.get_db_words('nicon_survey_exception_list','word') # 제외 단어 리스트
            
            
            if today_holi_flag == False:
                for word in tqdm(keywords_list , desc='검색중.......'):   
                    try:
                        apikey = api_keys[today_week]            
                        self.__log( f" [{word}] 검색 시작------------------------------------[{apikey}]" )
                        results = self.getApifyData( api_key=apikey , holiyyesterday=yesterday_holi_flag , keyword=word )
                        __proc , __succ , __fail = self.getDataProcess( results=results , keyword=word , target_keywords=target_keywords , except_word=except_word )                        
                        if word != keywords_list[-1]: # 마지막 검색어가 아니면 대기처리
                            wait_time = random.randint(10, 60)
                            self.__log( f" {datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')} || 다음 단어 검색까지 {wait_time // 60}분 {wait_time % 60}초 대기합니다." )
                            time.sleep(wait_time)        
                    except Exception as e:
                        self.__log( f"exec loop : {e}" )            

            self.__log( f" End - {'='*30}  " )
            w2ji.sendTelegramMsg(f' {keywords_list} 검색완료')
        except Exception as e :
            self.__log( f"exec error : {e}" )

    def test(self):
        ''' 메인 실행 부분'''
        try:           
            api_keys = os.environ.get('apify9')
                        
            today                = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')            
            chk_day              = self.get_date_info(today)
            today_holi_flag      = chk_day.get('today',False)        #당일 휴일 여부
            yesterday_holi_flag  = 'qdr:w' if chk_day.get('yesterday',False) == True  else 'qdr:d'    #어제 휴일 여부
            today_week           = self.getWeekGroup() #chk_day.get('week_cnt',1)-1        #주차 
            keywords_list        = self.get_db_words('nicon_search_keywords','keyword') # 검색할 키워드 리스트 반드시 "" 안에 문자를 넣어야 한다. 검색리스트    
            target_keywords      = self.get_db_words('nicon_target_words','word') # 이미지 혹은 이미지의 설명에 해당 단어가 포함되는지 확인        
            except_word          = self.get_db_words('nicon_survey_exception_list','word') # 제외 단어 리스트
            
            word = '쿠폰증정' #keywords_list[random.randint(0, 4)]
            apikey = api_keys
            self.__log('테스트 시작')
            self.__log(f" [{word}] 검색 시작~~~~~~~~~~~[{apikey}]")
            results = self.getApifyData( api_key=apikey , holiyyesterday=yesterday_holi_flag , keyword=word )
            __proc , __succ , __fail = self.getDataProcess( results=results , keyword=word , target_keywords=target_keywords , except_word=except_word )

            wait_time = random.randint(10, 100)
            self.__log( f"{datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')} |||| 다음 단어 검색까지 {wait_time // 60}분 {wait_time % 60}초 대기합니다..." ) 
            time.sleep(wait_time)        
            self.__log( f"{__proc} , {__succ} , {__fail} " )    
        except Exception as e :
            print(f"exec error : {e}")            



if __name__ == "__main__":   
    '''apify API 를 이용한 데이터 스크립핑 자동화.
    - api key 5개를 매달 1~5주차 까지 특정 주차에 하나의 키를 가지고 데이터를 수집한다.
    - 테스트는 5주차 계정으로 진행한다.
    - 

    '''
    search = Search()
    search.exec()   # 데이터 처리.
    #search.test()  # 테스트
    '''
    target_keywords = search.get_db_words('nicon_target_words','word') # 이미지 혹은 이미지의 설명에 해당 단어가 포함되는지 확인        
    except_word     = search.get_db_words('nicon_survey_exception_list','word') # 제외 단어 리스트 
    img = search.get_image_from_url( 'https://dqwc99gnfppi1.cloudfront.net/media/board/promotion_post/2026-05-30/143701_uBB4SOJuB4.jpg' )    
    qr0             = search.detect_qr_logic(img)    # 이미지내 qr 검출
    start_time = time.time()
    txt_tess        = search.getImgText(img) # 이미지내 텍스트 추출
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"실행 시간 tess : {elapsed_time:.4f}초")    
    start_time = time.time()
    txt_easy        = search.getImgText2(img) # 이미지내 텍스트 추출  
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"실행 시간 easy : {elapsed_time:.4f}초")        
    #tx1             = search.check_target_words( img , target_keywords , except_word ) # 이미지내 단어 검출    

    print(f"qr : {qr0}")
    print('*'*40)
    print(f"txt_tess : {txt_tess}")
    print('*'*40)
    print(f"txt_easy : {txt_easy}")
    '''

    '''
    target_keywords = search.get_db_words('nicon_target_words','word') # 이미지 혹은 이미지의 설명에 해당 단어가 포함되는지 확인        
    except_word     = search.get_db_words('nicon_survey_exception_list','word') # 제외 단어 리스트    

    
    img = search.get_image_from_url( 'https://dqwc99gnfppi1.cloudfront.net/media/board/promotion_post/2026-05-30/143701_uBB4SOJuB4.jpg' )
    #    print(type(img) , img,'||')

    qr0         = search.detect_qr_logic(img)    # 이미지내 qr 검출
    print(qr0)
    tx1             = search.check_target_words( img , target_keywords , except_word ) # 이미지내 단어 검출    
    aa ,bb          = search.extract_data_from_url(url='https://phdkim.net/board/promotion/512?from=home_recent' ,targets=target_keywords,except_word=except_word)
    print(aa)
    print(bb)
    
    today = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
    ss = search.get_date_info(today)
    print(ss.get('today',False) , ss.get('yesterday',False) , ss.get('week_cnt',1)-1 )
    print( 'w' if ss.get('yesterday',False) == True else 'd' )
    '''
    
    
