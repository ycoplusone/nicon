import re
from datetime import date,datetime
import cv2
import numpy as np
import pytesseract
from  pathlib import Path
import pandas as pd
import os

import lib.util as w2ji
import lib.dbcon as dbcon



pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# 다양한 날짜 패턴(연/월/일)
DATE_PATTERNS = [
    # 2026년 1월 9일
    re.compile(r"(?P<y>\d{4})\s*년\s*(?P<m>\d{1,2})\s*월\s*(?P<d>\d{1,2})\s*일"),
    # 2026.01.09 / 2026-1-9 / 2026/01/09
    re.compile(r"(?P<y>\d{4})\s*[.\-/]\s*(?P<m>\d{1,2})\s*[.\-/]\s*(?P<d>\d{1,2})"),
    # 26.01.09 / 26-1-9 / 26/01/09 (2자리 연도)
    re.compile(r"(?P<y>\d{2})\s*[.\-/]\s*(?P<m>\d{1,2})\s*[.\-/]\s*(?P<d>\d{1,2})"),
    # 2026 01 09 (공백/구분자 혼합)
    re.compile(r"(?P<y>\d{4})\s+(?P<m>\d{1,2})\s+(?P<d>\d{1,2})"),
]

def _normalize_text(s: str) -> str:
    # OCR 흔한 오타 보정: O->0, l->1 등 (필요시 확장)
    rep = str.maketrans({
        "O": "0", "o": "0",
        "I": "1", "l": "1", "|": "1",
        "S": "5",
    })
    return s.translate(rep)

def _to_date(y: int, m: int, d: int) -> date:
    try:
        return date(y, m, d)
    except ValueError:
        return None

def _parse_any_date(text: str) -> date :
    text = _normalize_text(text)
    candidates: list[date] = []

    for pat in DATE_PATTERNS:
        for m in pat.finditer(text):
            y = int(m.group("y"))
            mm = int(m.group("m"))
            dd = int(m.group("d"))

            # 2자리 연도 처리 (기본: 2000~2099로 해석)
            if y < 100:
                y += 2000

            dt = _to_date(y, mm, dd)
            if dt:
                candidates.append(dt)

    if not candidates:
        return None

    # 쿠폰 유효기간은 보통 "가까운 미래"인 경우가 많으니
    # 가장 최근(가장 큰 날짜)을 선택 (원하면 규칙 바꿔드림)
    return max(candidates)

def extract_expiry_date_flexible(image_path: str) -> str :
    #img = cv2.imread(image_path)
    data = np.fromfile(image_path, dtype=np.uint8)
    img = cv2.imdecode(data ,  cv2.IMREAD_COLOR)
    #if img is None:
    #    raise FileNotFoundError(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    data = pytesseract.image_to_data(th, lang="kor+eng", output_type=pytesseract.Output.DICT)

    # 전체 텍스트 먼저 파싱 시도
    full_text = " ".join([t for t in data["text"] if t and t.strip()])
    dt = _parse_any_date(full_text)
    if dt:
        return dt.strftime("%Y-%m-%d")

    # '유효기간' 키워드 찾아서 주변 영역 OCR
    h, w = th.shape[:2]
    boxes = []
    for i, txt in enumerate(data["text"]):
        if not txt:
            continue
        t = txt.strip().replace(" ", "")
        if ("유효" in t) and (("기간" in t) or ("기한" in t)):
            x, y, bw, bh = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            boxes.append((x, y, bw, bh))

    if not boxes:
        return None

    for (x, y, bw, bh) in boxes:
        # 키워드 오른쪽/아래를 넓게 잡아서 날짜가 어떤 형태든 포함되게
        x1 = max(0, x - int(0.05 * w))
        y1 = max(0, y - int(0.03 * h))
        x2 = min(w, x + bw + int(0.70 * w))
        y2 = min(h, y + bh + int(0.15 * h))

        roi = th[y1:y2, x1:x2]
        txt = pytesseract.image_to_string(roi, lang="kor+eng")
        dt = _parse_any_date(txt)
        if dt:
            return dt.strftime("%Y-%m-%d")

    return None

def read_image_unicode(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"경로에 파일이 없음: {path}")

    data = np.fromfile(path, dtype=np.uint8)
    if data.size == 0:
        raise ValueError("파일은 있으나 바이트를 못 읽음(권한/잠금 가능)")

    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("파일은 있으나 이미지 디코딩 실패(손상/확장자 불일치 가능)")

    return img


if __name__ == "__main__":
    '''
    Tesseract 설치 파일 경로 : https://github.com/UB-Mannheim/tesseract/wiki
    나머지는 실행하면서 lib를 추가 하자.
    '''
    __ver = '0.1'
    __comment = '니콘의 유효기간을 추출해서 엑셀로 출력한다.'
    print(__ver , __comment)
    _dbconn     = dbcon.DbConn() #db연결    
    __lists = w2ji.getFileCnt_v02( _dbconn , False ) # 251216 수정완 파일 잔여 개수 확인 후 텔레그램 발송  
    _data = []
    for list in __lists:            
        # {'div_nm' : __category , 'brand':__brand , 'prod':__prod , 'fold_cnt':0 , 'fold_date':'99991231' , 'bal_qty':0 , 'suc_qty':0 , 'chk_qty':0}        
        div01_str   = list['div_nm']
        div02_str   = list['brand']
        div03_str   = list['prod']
        fold_nm     = f'{div01_str}_{div02_str}\\{div03_str}'
        cnt         = list['fold_cnt'] 

        prod_fold_list = w2ji.getfolelist( fold_nm ) # 상품 폴더 리스트의 하위 폴더 리스트 생성.       
        for fold in prod_fold_list:
            files = w2ji.getFileList( fold ) #상품폴더내 파일 리스트 생성
            for file in files:
                expire_date = extract_expiry_date_flexible( file )
                _temp = {'path':file , '유효기간':expire_date}
                _data.append(_temp)
    
    def sort_key(item):
        d = item.get('유효기간')
        if not d:
            return datetime.max  # None은 맨 뒤로
        return datetime.strptime(d, "%Y-%m-%d")
    
    data_sorted = sorted(_data, key=sort_key)
    COLUMNS = ["path", "유효기간"]
    df = pd.DataFrame(data_sorted , columns=COLUMNS)

    df.to_excel("c:\\ncnc\\result.xlsx", index=False)   # index=False 추천
                
    