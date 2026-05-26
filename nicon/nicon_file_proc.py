import json
from pathlib import Path
from collections import Counter
from datetime import datetime
import os
import pandas as pd


'''
대량의 바코드를 삭제 이동 시키는 스크립트를 생성한다.
'''
def convert_date_to_yyyymmdd(date_str):
    """
    '2026-05-18T13:08:31.000Z' 형태의 문자열을 '20260518' 형태로 변경하는 함수
    """
    if not date_str:
        return ""
        
    try:
        # 1. 기존 ISO 8601 문자열 포맷을 datetime 객체로 파싱
        # 뒤의 밀리초(.000Z) 부분까지 포함하여 매핑합니다.
        dt_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        try:
            # 밀리초 뒤에 Z 대신 다른 타임존 표기가 올 경우를 대비한 예외 처리
            dt_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.000Z")
        except ValueError:
            # 만약 포맷이 다르면 원본에서 앞의 10자리(YYYY-MM-DD)만 추출해 하이픈을 제거하는 방식으로 대체
            return date_str[:10].replace("-", "")
            
    # 2. 원하는 yyyymmdd 포맷의 문자열로 변경하여 반환
    return dt_obj.strftime("%Y%m%d")

def parse_standard_json():
    '''데이터 파싱 처리'''
    # 바탕화면의 nicon.json 경로 설정
    
    file_path = r"c:\ncnc\nicon.json"
    

    try:
        # 표준 JSON이므로 open 후 곧바로 json.load()가 가능합니다.
        with open(file_path, "r", encoding="utf-8") as file:
            nested_list = json.load(file)
        
        # nested_list는 현재 [[쿠폰1], [쿠폰2], [쿠폰3]] 구조의 2차원 리스트입니다.
        # 이를 사용하기 편하게 1차원 리스트로 리스트 컴프리헤션을 통해 평탄화(Flatten)합니다.
        merged_list = [item for sublist in nested_list for item in sublist]
        
        print(f"\n✅ [표준 파싱 완료] 총 {len(merged_list)}개의 쿠폰 데이터를 읽어왔습니다.")        
        
        # 원하는 필드만 담을 결과 리스트 변수
        refined_list = []
        
        # 4. 반복문을 돌며 요청하신 데이터만 매핑하여 추출
        for li in merged_list:
            con_item = li.get("conItem", {})
            category2 = con_item.get("conCategory2", {})
            extracted_item = {
                "id": li.get("id"),
                "brand_name": category2.get("name"),       # conItem.conCategory2.name
                "item_name": con_item.get("name"),          # conItem.name
                "lastCodeNumber": li.get("lastCodeNumber"),
                "status": li.get("currentStatus"),
                "rejectedReason" : li.get("rejectedReason"),
                "con_dt": convert_date_to_yyyymmdd( li.get("confirmExpireAt") )
            }
            # 결과 리스트에 추가
            refined_list.append(extracted_item)        
        
        return refined_list

    except json.JSONDecodeError as e:
        print(f"❌ JSON 문법 오류: 파일 구조를 다시 확인해주세요. ({e})")
        return []
    except FileNotFoundError:
        print("❌ 파일을 찾을 수 없습니다.")
        return []
    
from collections import Counter

def file_search(item):
    unmatched_status_list = []
    matched_files         = []
    file_data = []
    base_path = Path("C:/ncnc")

    brand_name = str(item.get("brand_name", "")).strip()
    item_name  = str(item.get("item_name", "")).strip()
    last_code  = str(item.get("lastCodeNumber", "")).strip()
    
    if not brand_name or not item_name or not last_code:
        item["file_match_count"] = 0
        item["file_match_status"] = "Not Found11"
        file_data.append(item)

    matched_files = []
    target_folder = None
    
    # 1. C:\ncnc 하위 실제 폴더명 스캔 (앞 2글자 제외 대조)
    if base_path.is_dir():
        for local_dir in base_path.iterdir():
            if local_dir.is_dir():
                if len(local_dir.name) > 2 and local_dir.name[2:] == brand_name:
                    target_folder = local_dir / item_name
                    break
        
    # 2. item_name 폴더 존재 확인 후 하위 폴더들 탐색
    if target_folder and target_folder.exists() and target_folder.is_dir():
        for sub_dir in target_folder.iterdir():
            if sub_dir.is_dir():  # 하위 폴더 진입
                
                # 3. 하위 폴더 내부 파일 탐색 및 뒷자리 6글자 검증
                for file_path in sub_dir.iterdir():
                    if file_path.is_file():
                        file_name_without_ext = file_path.stem.split('_')[0]
                        if file_name_without_ext[-6:] == last_code:
                            matched_files.append(str(file_path))
                            


                    
    # 4. 파일 매칭 카운트 및 상태 세팅
    match_count = len(matched_files)
    item["file_match_count"] = match_count
    item["actual_file_paths"] = matched_files 
    
    # 상태 값 지정
    if match_count == 0:
        item["file_match_status"] = "Not Found"
    elif match_count == 1:
        item["file_match_status"] = "Matched"
    else:
        item["file_match_status"] = "File Duplicate" 
    
    file_data.append(item)
    return file_data
       


def separate_and_sort_duplicates(refined_list):
    """
    refined_list에서 brand_name, item_name, lastCodeNumber 기준으로 
    중복이 발생한 '모든 데이터'를 duplicate_list로 격리한 뒤 기준 필드로 정렬하고,
    단 한 번만 나타난 고유 데이터만 unique_list에 남기는 함수
    
    :param refined_list: 6개 필드로 정형화한 데이터 리스트
    :return: (unique_list, duplicate_list)
    """
    unique_list = []
    duplicate_list = []
    
    # 1. 등장 횟수를 세기 위한 고유 키(지문) 목록 생성
    key_list = []
    for item in refined_list:
        brand_name = item.get("brand_name")
        item_name = item.get("item_name")
        last_code = item.get("lastCodeNumber")
        
        dup_key = (str(brand_name), str(item_name), str(last_code))
        key_list.append(dup_key)
    
    key_counts = Counter(key_list)
    
    # 2. 2회 이상 등장한 중복 데이터는 duplicate_list로, 1회는 unique_list로 분리
    for item in refined_list:
        brand_name = item.get("brand_name")
        item_name = item.get("item_name")
        last_code = item.get("lastCodeNumber")
        
        dup_key = (str(brand_name), str(item_name), str(last_code))
        
        if key_counts[dup_key] > 1:
            duplicate_list.append(item)
        else:
            unique_list.append(item)
            
    # 3. ⭐️ [정렬 로직 추가] ⭐️
    # duplicate_list를 brand_name -> item_name -> lastCodeNumber 순서로 정렬합니다.
    # 데이터가 None일 경우를 대비해 str()로 안전하게 감싸서 비교합니다.
    duplicate_list.sort(key=lambda x: (
        str(x.get("brand_name")), 
        str(x.get("item_name")), 
        str(x.get("lastCodeNumber"))
    ))
            
    return unique_list, duplicate_list

def separate_unsold_data(refined_list):
    """
    정형화된 데이터 리스트에서 currentStatus 값이 'sold'가 아닌 데이터를 
    별도의 리스트로 격리하고, 'sold'인 데이터만 기존 리스트(sold_list)에 남기는 함수
    
    :param refined_list: 정형화된 데이터 리스트
    :return: (sold_list, unsold_list) -> 판매 완료 리스트, 미판매/기타 리스트의 튜플
    """
    sold_list = []      # 상태가 'sold'인 데이터만 남을 리스트 (기존 리스트 대체용)
    unsold_list = []    # 상태가 'sold'가 아닌 모든 데이터를 따로 저장할 리스트
    
    for item in refined_list:
        # 대소문자나 공백으로 인한 오류를 방지하기 위해 strip()과 lower()를 적용하면 더 안전합니다.
        status = str(item.get("status", "")).strip().lower()
        
        # 상태가 'sold'인 경우
        if status == "sold":
            sold_list.append(item)
        # 'sold'가 아닌 경우 (예: 'unsold', 'expired', None 등)
        else:
            unsold_list.append(item)
    
    aa = []
    for item in unsold_list:
        aa.append( file_search(item) )
    
    print(aa[0])

    
            
    return sold_list, unsold_list

def verify_and_separate_by_matched(refined_list):
    """
    C:\\ncnc 내부 깊은 하위 폴더까지 탐색하여 파일 매칭을 검증한 후,
    상태가 정확히 'matched'(파일 1개 정상 발견)인 데이터와 
    아닌 데이터(0개 미발견 또는 2개 이상 중복)를 두 개의 배열로 분리하는 함수
    """
    base_path = Path("C:/ncnc")
    
    # 최종 분리할 2개의 배열
    matched_status_list   = []    # 파일이 정확히 1개 매칭된 데이터 (성공)
    unmatched_status_list = []    # 파일이 0개이거나 2개 이상 중복된 데이터 (실패 및 검토 대상)
    
    if not base_path.exists():
        print(f"❌ 에러: 시스템에 {base_path} 폴더가 존재하지 않습니다.")
        return [], refined_list

    for item in refined_list:
        brand_name = str(item.get("brand_name", "")).strip()
        item_name = str(item.get("item_name", "")).strip()
        last_code = str(item.get("lastCodeNumber", "")).strip()
        
        if not brand_name or not item_name or not last_code:
            item["file_match_count"] = 0
            item["file_match_status"] = "Not Found"
            unmatched_status_list.append(item)
            continue
            
        matched_files = []
        target_folder = None
        
        # 1. C:\ncnc 하위 실제 폴더명 스캔 (앞 2글자 제외 대조)
        if base_path.is_dir():
            for local_dir in base_path.iterdir():
                if local_dir.is_dir():
                    if len(local_dir.name) > 2 and local_dir.name[2:] == brand_name:
                        target_folder = local_dir / item_name
                        break
        
        # 2. item_name 폴더 존재 확인 후 하위 폴더들 탐색
        if target_folder and target_folder.exists() and target_folder.is_dir():
            for sub_dir in target_folder.iterdir():
                if sub_dir.is_dir():  # 하위 폴더 진입
                    
                    # 3. 하위 폴더 내부 파일 탐색 및 뒷자리 6글자 검증
                    for file_path in sub_dir.iterdir():
                        if file_path.is_file():
                            file_name_without_ext = file_path.stem
                            
                            if file_name_without_ext[-6:] == last_code:
                                matched_files.append(str(file_path))
                        
        # 4. 파일 매칭 카운트 및 상태 세팅
        match_count = len(matched_files)
        item["file_match_count"] = match_count
        item["actual_file_paths"] = matched_files 
        
        # 상태 값 지정
        if match_count == 0:
            item["file_match_status"] = "Not Found"
        elif match_count == 1:
            item["file_match_status"] = "Matched"
        else:
            item["file_match_status"] = "File Duplicate"
            
        # 5. ⭐️ [핵심 수정] file_match_status가 'Matched'인 것과 아닌 것으로 배열 분리
        if item["file_match_status"] == "Matched":
            matched_status_list.append(item)      # 정상 매칭 배열에 추가
        else:
            unmatched_status_list.append(item)    # 미발견 및 중복 오류 배열에 추가
            
    return matched_status_list, unmatched_status_list

def export_unmatched_to_excel(d_list , none_list , not_list , fin_list):
    """
    unmatched_status_list 데이터를 DataFrame으로 변환하여
    C:\\ncnc\\unmatched_report.xlsx 파일로 저장하는 함수
    d_list   중복리스트
    none_list  판매상태 이상 리스트
    not_list  로컬 이상 검출 리스트

    """
    # 1. 저장할 폴더 및 파일 경로 설정
    current_date_str = datetime.now().strftime('%Y%m%d_%H%M')
    file_name = f"nicon_{current_date_str}.xlsx"
    target_dir = Path("C:/ncnc")
    file_path = target_dir / file_name
    
    # 만약 C:\ncnc 폴더가 없다면 자동으로 생성해 줍니다.
    if not target_dir.exists():
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            print(f"📁 폴더가 존재하지 않아 새로 생성했습니다: {target_dir}")
        except Exception as e:
            print(f"❌ 폴더 생성 실패 (권한 부족 등): {e}")
            return

    # 2. 엑셀에 담을 형태로 데이터 정제 (열 이름 매핑)
    excel_data = []
    def fn_inner(li , str):
        '''내부 함수'''
        for item in li:
            # 데이터 내부에 있는 중첩 구조(actual_file_paths)를 문자열로 보기 좋게 합쳐줍니다.
            paths = item.get("actual_file_paths", [])
            paths_str = ", ".join(paths) if paths else "없음"
            file_proc = ''
            
            if str =='정상':
                file_proc = f'del /f /q "{paths_str}"'
            elif str == '판매상태이상':
                ''''''
                file_path = Path(paths_str)
                print('asdfasdf',file_path)
                if file_path.exists():
                    # 바로 위 폴더(부모 폴더) 경로 가져오기 (.parent)
                    parent_dir  = file_path.parent.parent
                    move_path   = f"{parent_dir}\{file_path.name}"
                    file_proc   = f'move "{file_path}" "{move_path}" '
            else :
                file_proc = paths_str


            
            refined_row = {
                "구분"      : str,
                "확인일"    : item.get('con_dt',''),
                "브랜드명"   : item.get("brand_name"),
                "상품명"     : item.get("item_name"),
                "바코드_끝6자리": item.get("lastCodeNumber"),
                "상태": item.get("currentStatus"),
                "발견된_파일_개수": item.get("file_match_count", 0),                
                "발견된_파일_경로": file_proc
            }
            excel_data.append(refined_row)  
    fn_inner(d_list , '중복파일')      
    fn_inner(none_list , '판매상태이상')      
    fn_inner(not_list , '이상검색')      
    fn_inner(fin_list , '정상')    

    # 3. 데이터가 비어있을 경우 예외 처리
    if not excel_data:
        print("⚠️ 안내: 추출된 미매칭 데이터가 없어서 엑셀 파일 생성을 건너뜁니다.")
        return

    try:
        # 4. Pandas DataFrame 생성 및 엑셀 저장
        df = pd.DataFrame(excel_data)
        
        # index=False 옵션으로 엑셀 맨 왼쪽에 불필요한 번호 열(0, 1, 2...)이 생기지 않게 합니다.
        df.to_excel(file_path, index=False, engine='openpyxl')
        
        print("\n" + "="*50)
        print("✅ [엑셀 파일 생성 완료]")
        print(f" 파일이 성공적으로 저장되었습니다.")
        print(f" 📂 경로: {file_path}")
        print("="*50)
        
    except PermissionError:
        print(f"❌ 에러: 해당 엑셀 파일이 이미 켜져 있어 저장할 수 없습니다.")
        print(f"   열려 있는 'unmatched_report.xlsx' 파일을 닫고 다시 실행해 주세요.")
    except Exception as e:
        print(f"❌ 예기치 못한 에러 발생: {e}")    

    

if __name__ == "__main__":
    '''
        /*1번 consonle 에 텍스트 허용 */
        allow pasting

        /*2번 스크립트 실행
        bearer 부분은 접속 기록 확인후 변경 가능.
        */
        fetch('https://api2.ncnc.app/cons/confirmed?page=1', {
        headers: {
            'accept': 'application/json, text/plain, */*',
            'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjAwNjM3LCJ0eXBlcyI6Imtha2FvLHBob25lLG5hdmVyIiwiYmFua0lkIjoyNCwiaWF0IjoxNzc5MTY0MDc0LCJleHAiOjE4NDIyMzYwNzR9.zzAi8JEZl3thM5P3eNs2EmE1dUabXfM8eZYsM-hY0rg',
            'sec-gpc': '1'
        }
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));


        바탕 화면에 nicon.json 파일 생성
        /* 라이브러리*/
        pip install   openpyxl 
    '''
    print('Nicon 파일 처리 중입니다. c:\ncnc 폴더에 niconxxx.xlsx 이상 파일 생성됩니다. ')
    print('정상인경우 삭제 스크립트 출력됩니다. 전체 복사해서 붙여넣기 해서 삭제 수행합니다.')

    lists = parse_standard_json()

    # u_list 중복없는 데이터 , d_list 중복된 데이터 개별로 확인해야 하는 리스트
    u_list , d_list = separate_and_sort_duplicates(lists)

    # 판맨완료와 기타반려 리스트 
    sold_list , none_list = separate_unsold_data( u_list )

    # fin_list 단일 파일 리스트 , not_list 중복혹은 파일을 찾지 못한 리스트
    fin_list , not_list = verify_and_separate_by_matched(sold_list)

    # 엑셀 생성
    export_unmatched_to_excel(d_list , none_list, not_list , fin_list)


    '''
    fin_list 를 이용해서 삭제 스크립트 생성 문제 없는 리스트 파일 삭제
    문제가 없다는것은 
    1번 : "브랜드 + 상품명 + 바코드" 에 대해서 중복 판매 이력이 없는건
    2번 : 1번에서 판매상태가 "판매완료" 인건
    3번 : 2번에서 로컬pc 에서 파일을 1개만 검출된 대상
    4번 : 1번 2번 3번 모두 통과한 리스트

    문제있는것
    - "브랜드 + 상품명 + 바코드" 중복이 있는건
    - 판매상태가 "판매완료" 가 아닌 건
    - 로컬pc 에서 파일이 0개 혹은 2개 이상 검출된 대상
    '''
    '''
    for item in fin_list:
        file_paths = item.get("actual_file_paths", [])
        win_path = file_paths[0].replace("/", "\\")
        print( f'del /f /q "{win_path}"' )
    '''
    

    
    
