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
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(formatter)
            
            # 4. 로거에 핸들러 추가
            logger.addHandler(file_handler)
            
            # (선택사항) 터미널 콘솔창에도 동시에 print하고 싶다면 아래 주석을 해제하세요.
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)            
        return logger.info
    
    def get_month_week_simple(self , date_str):
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
        """
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

    def check_target_words(self , image_obj , targets , except_word ):
        """
        이미지 객체에서 targets 단어가 포함되어 있는지 판별함
        , 이미지 객체에 except_word 가 포함되어 있는지 판별.
        """
        pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'
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
        found_except_words = [word for word in except_word if word in clean_text]
        #print('\n','#'*20)
        #print( 'clean_text',clean_text )        
        #print( 'found_words',found_words )        
        #print( 'excpt_words',found_except_words )
        #print( 'condition',found_words and not found_except_words )
        

        if found_words and not found_except_words:
            #print(f"✅ 단어 검출 성공: {found_words}")
            return True
        else:
            #print("❌ 대상 단어를 찾지 못했습니다.")
            return False

    def extract_data_from_url(self, url,  targets , except_word , save_path="screenshot.png" ):
        chk_qr      = False
        chk_txt     = False    
        with sync_playwright() as p:
            try:
                # 브라우저 실행 (좌표를 눈으로 확인하기 위해 headless=False 추천)
                browser         = p.chromium.launch(headless=True)
                
                # 뷰포트(화면 크기)를 고정해야 좌표가 틀어지지 않습니다.
                window_width    = 1024
                window_height   = 1024
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
                    #print(f"인스타그램 감지: 좌표 (X: {click_x}, Y: {click_y})를 클릭합니다.")                
                    try:
                        # 해당 좌표를 마우스로 직접 클릭
                        page.mouse.click(click_x, click_y)
                        print("좌표 클릭 완료.")
                        time.sleep(1) # 클릭 후 팝업이 닫히는 시간 대기
                    except Exception as e:
                        print(f"좌표 클릭 중 오류 발생: {e}")

                page.screenshot(path=save_path, full_page=False)
                browser.close()   
                # 3. 이미지 로드
                img = Image.open(save_path)

                # 4. 텍스트 추출 (OCR)
                # lang='kor+eng' 설정을 통해 한글과 영어를 동시에 인식 가능해
                pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'
                text_data = pytesseract.image_to_string(img, lang='kor+eng')
                #print("\n--- [추출된 텍스트] ---")
                text_data           = text_data.replace(" ", "").replace("\n", "")
                found_words         = [word for word in targets if word in text_data]            
                found_except_words  = [word for word in except_word if word in text_data]                        
                if( found_words and not found_except_words ):
                    chk_txt = True
                else:
                    chk_txt = False

                # 5. QR 코드 추출
                qr_results = decode(img)
                #print("\n--- [추출된 QR 코드 정보] ---")
                if qr_results:
                    for qr in qr_results:
                        #print(f"🔗 QR 데이터: {qr.data.decode('utf-8')}")
                        chk_qr = True # QR코드 식별
                #print( 'qr'  , chk_qr )   
                return chk_qr , chk_txt             
            except Exception as e:
                return chk_qr , chk_txt 
            finally:
                return chk_qr , chk_txt

    def scrape_google_images_by_damilo( self , api_key , holiyyesterday , keyword:str , target_keywords = [] , except_word = [] ):
        results = []
        totproc = 0
        totsucc = 0
        totfail = 0
        cnt = 0


        # 1. 본인의 Apify API 토큰 입력
        APIFY_TOKEN = api_key
        
        # 클라이언트 초기화
        client = ApifyClient(APIFY_TOKEN)

        # 2. damilo/google-images-scraper 가 요구하는 입력값 설정
        run_input = {
            "country"       : "kr",
            "date_range"    : holiyyesterday , # w 일주일 , d 하루
            "language"      : "ko",
            "max_pages"     : 1,
            "num"           : "100",
            "query"         : keyword           # 검색어
        }    

        self.__log( f"'{keyword}' 키워드로 구글 이미지 검색을 시작합니다...")
        #self.__log( f"target_keywords : {target_keywords}")
        #self.__log( f"except_word : {except_word}")

        try:
            # 3. damilo의 구글 이미지 스크래퍼 액터 실행
            # (주의: 액터 이름이 정확히 'damilo/google-images-scraper' 인지 확인해야 합니다)
            run = client.actor("damilo/google-images-scraper").call(run_input=run_input)

            # 4. 결과가 저장된 데이터셋(Dataset)에서 데이터 가져오기            
            dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items

            # 5. 수집된 결과 출력 및 가공
            self.__log( f"총 {len(dataset_items)}개의 이미지를 찾았습니다.\n" )
            
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
            self.__log( f"크롤링 중 오류가 발생했습니다: {e}" )   
        
        try:
            for result in tqdm(results , desc=f'[{keyword}] 처리중 => ' , leave=False):
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
                extension_map = {
                    '.pdf': 'PDF 문서',
                    '.txt': '텍스트 파일',
                    '.xlsx': '엑셀(Excel) 파일',
                    '.xls': '엑셀(Excel) 파일',
                    '.csv': '엑셀(CSV) 파일',
                    '.docx': '워드(Word) 파일',
                    '.doc': '워드(Word) 파일',
                    '.hwp': '한글(HWP) 파일',
                    '.hwpx': '한글(HWPX) 파일',
                    '.pptx': '파워포인트(PPT) 파일',
                    '.ppt': '파워포인트(PPT) 파일'
                }

                # 4. 검출 논리
                if ext in extension_map:
                    url_pdf = True # 확장자 검출
                else:
                    url_pdf = False # 확장자 미검출 
                
                img         = "" if img_src == "" else self.get_image_from_url(img_src) # 이미지 생성
                if img == '':
                    img = self.get_image_from_url(thumbnail_src)

                qr0         = False  if img == "" else self.detect_qr_logic(img)    # 이미지내 qr 검출
                tx1         = False  if img == "" else self.check_target_words( img , target_keywords , except_word ) # 이미지내 단어 검출
                txt         = [word for word in target_keywords if word in alt_text_chk]
                tx2         = True if txt else False # 설명문에 단어 검출                
                __temp = {'url' : url , 'description':alt_text[0:128] , 'has_qr':qr0 , 'has_text_survey':tx1 , 'has_text_satisfaction':tx2 , 'words':keyword}            
                self.__log( f" 처리 url :{url}" )
                if (url_chk == 0 and url_pdf == False):
                    
                    if ( qr0 or tx1 or tx2 ):
                        if any(word in url for word in except_word) or any(word in alt_text_chk for word in except_word) : # url 과 이미지설명에 금지단어 검출                        
                            #print(url, '=>' ,'worst_url 1단계 제외 단어 검출')
                            totfail += 1 # 실패 건수 등록
                            self.__dbconn.upsert_nicon_survey_worst_url_list(param=__temp) # 제외 url에 넣는다.
                            self.__log( f" 실패" )
                        else:                           
                            totsucc += 1 # 성공건수 등록
                            self.__dbconn.upsert_nicon_survey_collection(__temp)
                            chk_qr , chk_txt = self.extract_data_from_url(url=url ,targets=target_keywords,except_word=except_word)
                            __tempdd = {'url' : url , 'chk_qr':chk_qr , 'chk_txt':chk_txt }
                            self.__dbconn.upsert_nicon_survey_detail( param=__tempdd )
                            self.__log( f" 등록1 : {qr0} , {tx1} , {tx2} , {chk_qr} , {chk_txt} " )
                    else: 
                        chk_qr , chk_txt = self.extract_data_from_url(url=url ,targets=target_keywords,except_word=except_word)                        
                        if (chk_qr or chk_txt ):           
                            totsucc += 1 # 성공건수 등록             
                            self.__dbconn.upsert_nicon_survey_collection( __temp ) # 등록
                            __tempdd = {'url' : url , 'chk_qr' : chk_qr , 'chk_txt' : chk_txt } # 상세 등록
                            self.__dbconn.upsert_nicon_survey_detail( param=__tempdd )                            
                            self.__log( f" 등록2 :{qr0} , {tx1} , {tx2} , {chk_qr} ,{chk_txt}" )
                        else :
                            totfail += 1 # 실패 건수 등록
                            self.__dbconn.upsert_nicon_survey_worst_url_list(param=__temp) # 제외 url에 넣는다. 
                            self.__log( f" worst_url 2단계 아무것도 검출안됨" )                   
                elif( url_chk >= 9 ):
                    self.__log( '이미등록건' )
                    self.__dbconn.upsert_nicon_survey_collection(__temp) # 검색어만 업데이트 한다.
                else:
                    # url에 PDF 파일이 포함되어 있다면 검사 없이 넘어간다.
                    totfail += 1 # 실패 건수 등록
                    self.__dbconn.upsert_nicon_survey_worst_url_list(param=__temp) # 제외 url에 넣는다.
                    self.__log( 'url 이상건' )
                
            self.__log( f"검색어[{keyword}] 처리 [성공:{totsucc}, 실패:{totfail}].")
            self.__log( f"{'*'*20}")

            return totproc , totsucc , totfail

        except Exception as e:
            print(f'추출데이터 처리:{e}')

    def get_db_words(self,table,where):
        '''db에서 데이터 배열 가져오기'''
        return self.__dbconn.get_db_word_list(table,where)


    def exec(self):
        ''' 메인 실행 부분'''
        try:
            api_keys = [ os.environ.get('apify0') , 
                        os.environ.get('apify1') ,
                        os.environ.get('apify2') ,
                        os.environ.get('apify3') ,
                        os.environ.get('apify4') 
                        ] # 향후 3~4개 키워드 검색후 다른 api를 이용하도록 수정한다.
            today   = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
            
            self.__log( f" Begin - {'|'*20}  " )

            chk_day = self.get_date_info(today)
            today_holi_flag      = chk_day.get('today',False)        #당일 휴일 여부
            yesterday_holi_flag  = 'qdr:w' if chk_day.get('yesterday',False) == True  else 'qdr:d'    #어제 휴일 여부
            today_week      = chk_day.get('week_cnt',1)-1        #주차 
            keywords_list   = self.get_db_words('nicon_search_keywords','keyword') # 검색할 키워드 리스트 반드시 "" 안에 문자를 넣어야 한다. 검색리스트    
            target_keywords = self.get_db_words('nicon_target_words','word') # 이미지 혹은 이미지의 설명에 해당 단어가 포함되는지 확인        
            except_word     = self.get_db_words('nicon_survey_exception_list','word') # 제외 단어 리스트
            
            
            if today_holi_flag == False:
                for word in tqdm(keywords_list , desc='검색중.......'):   
                    apikey = api_keys[today_week]            
                    self.__log( f" [{word}] 검색 시작~~~~~~~~~~~[{apikey}]" )
                    # __proc , __succ , __fail = self.scrape_google_images_by_damilo( api_key=apikey , holiyyesterday=yesterday_holi_flag , keyword=word , target_keywords=target_keywords , except_word=except_word )
                    if word != keywords_list[-1]: # 마지막 검색어가 아니면 대기처리
                        wait_time = random.randint(10, 100)
                        self.__log( f"{datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')} |||| 다음 단어 검색까지 {wait_time // 60}분 {wait_time % 60}초 대기합니다..." )
                        time.sleep(wait_time)        
                    #print( __proc , __succ , __fail )    
            self.__log( f" End - {'|'*20}  " )
            w2ji.sendTelegramMsg(f'{keywords_list} 검색완료')
        except Exception as e :
            self.__log( f"exec error : {e}" )

    def test(self):
        ''' 메인 실행 부분'''
        try:           
            api_keys = os.environ.get('apify4')
                        
            today   = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')            
            chk_day = self.get_date_info(today)
            today_holi_flag      = chk_day.get('today',False)        #당일 휴일 여부
            yesterday_holi_flag  = 'qdr:w' if chk_day.get('yesterday',False) == True  else 'qdr:d'    #어제 휴일 여부
            today_week      =chk_day.get('week_cnt',1)-1        #주차 
            keywords_list   = self.get_db_words('nicon_search_keywords','keyword') # 검색할 키워드 리스트 반드시 "" 안에 문자를 넣어야 한다. 검색리스트    
            target_keywords = self.get_db_words('nicon_target_words','word') # 이미지 혹은 이미지의 설명에 해당 단어가 포함되는지 확인        
            except_word     = self.get_db_words('nicon_survey_exception_list','word') # 제외 단어 리스트
            
            word = keywords_list[random.randint(0, 4)]
            apikey = api_keys
            self.__log('테스트 시작')
            self.__log(f" [{word}] 검색 시작~~~~~~~~~~~[{apikey}]")
            __proc , __succ , __fail = self.scrape_google_images_by_damilo( api_key=apikey , holiyyesterday=yesterday_holi_flag , keyword=word , target_keywords=target_keywords , except_word=except_word )
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
    
    
