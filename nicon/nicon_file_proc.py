import json
from pathlib import Path
from collections import Counter
from datetime import datetime
import time
import os
import pandas as pd
import lib.util as w2ji
from pathlib import Path
import shutil

class FileProc():
    '''
    대량의 바코드를 삭제 이동 시키는 스크립트를 생성한다.
    '''
    # 일자 형변환 -- start
    def convert_date_to_yyyymmdd(self , date_str):
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
    # 일자 형변환 -- end

    # json 파일 파싱 -- start
    def parse_standard_json(self):
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
                    "con_dt": self.convert_date_to_yyyymmdd( li.get("confirmExpireAt") )
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
    # json 파일 파싱 -- end

    # 파일 탐색 -- start
    def file_search(self , alter_name , item):        
            
        base_path       = Path("C:/ncnc")
        brand_name      = str(item.get("brand_name", "")).strip()        #브랜드명
        item_name_org   = str(item.get("item_name", "")).strip()         #상품명
        item_name_alt   = w2ji.getResolveProd(alter_name ,brand_name , item_name_org ) #변경 상품명을 찾아온다.
        item_name       = item_name_alt if item_name_alt != '' else item_name_org
        last_code       = str(item.get("lastCodeNumber", "")).strip()    #마지막 바코드 6자리
        status          = str(item.get("status", "")).strip()            #판매상태
        
        matched_files = []
        target_folder = None

        # 1. C:\ncnc 하위 실제 폴더명(브랜드 폴더 검색) 스캔 (앞 2글자 제외 대조 ex) "카_스타벅스"=> "스타벅스" )
        if base_path.is_dir():
            for local_dir in base_path.iterdir():
                if local_dir.is_dir():
                    #print(local_dir.name , local_dir.name[2:] , brand_name , local_dir.name[2:] == brand_name )
                    if len(local_dir.name) > 2 and local_dir.name[2:] == brand_name:
                        target_folder = local_dir / item_name
                        break
        #print(f"브랜드:{brand_name} , 상품:{item_name} , 바코드:{last_code} , 경로:{target_folder}")
            
        # 2. item_name 폴더 존재 확인 후 하위 폴더들 탐색
        if target_folder and target_folder.exists() and target_folder.is_dir():
            for sub_dir in target_folder.iterdir():
                if sub_dir.is_dir():  # 하위 폴더 진입                    
                    # 3. 하위 폴더 내부 파일 탐색 및 뒷자리 6글자 검증
                    for file_path in sub_dir.iterdir():
                        if file_path.is_file():
                            file_name_without_ext = file_path.stem.split('_')[0]
                            #print(file_path , file_name_without_ext , file_name_without_ext[-6:] ,file_name_without_ext[-2:] )
                            if file_name_without_ext[-6:] == last_code:
                                if status =='sold':
                                    #matched_files.append(str(file_path))
                                    matched_files.append( f'del /f /q "{file_path}"' )
                                else:
                                    ''''''
                                    parent_dir  = file_path.parent.parent
                                    move_path   = f"{parent_dir}\{file_path.name}"
                                    matched_files.append(  f'move "{file_path}" "{move_path}" ')
                        
        # 3. 파일 매칭 카운트 및 상태 세팅
        match_count = len(matched_files)
        item["file_match_count"]    = match_count # 검색건수
        item["actual_file_paths"]   = ', '.join(matched_files)  # 검색된 경로들
        
        # 상태 값 지정
        if match_count == 0:
            item["file_match_status"] = "Not Found"
        elif match_count == 1:
            item["file_match_status"] = "Matched"
        else:
            item["file_match_status"] = "File Duplicate" 
        
        return item
    # 파일 탐색 -- end

    # 엑셀 생성 -- start
    def export_to_excel( self , lists ):
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
                    
        excel_data = []
        # 2. 엑셀 형식 정리
        for item in lists:
            refined_row = {
                "확인일"            : item.get('con_dt',''),
                "브랜드명"          : item.get("brand_name"),
                "상품명"            : item.get("item_name"),
                "바코드_끝6자리"     : item.get("lastCodeNumber"),
                "상태"              : item.get("status"),
                "파일수"            : item.get("file_match_count", 0),                
                "경로"              : item.get("actual_file_paths", ''),
            }        
            excel_data.append( refined_row )

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
            print(f" 📂 경로: {file_path}")
            print("="*50)
            
        except PermissionError:
            print(f"❌ 에러: 해당 엑셀 파일이 이미 켜져 있어 저장할 수 없습니다.")
            print(f"   열려 있는 'unmatched_report.xlsx' 파일을 닫고 다시 실행해 주세요.")
        except Exception as e:
            print(f"❌ 예기치 못한 에러 발생: {e}")    
    # 엑셀 생성 -- end

    # 폴더 정리기 -- start
    def clearer_folder(self):
        base_path       = Path("C:/ncnc")        

        # 완료) 폴더 내부 파일 이동
        for local_dir in base_path.iterdir(): # ncnc 폴더 아래 폴더 리스트
            if local_dir.is_dir():
                brand_path = Path(local_dir)
                for _item_fold in brand_path.iterdir():
                    if _item_fold.is_dir():
                        _last_fold = Path(_item_fold)
                        for _temp_path in _last_fold.iterdir():
                            if ( _temp_path.is_dir() ) and ( _temp_path.stem[-3:] == '완료)' ) :
                                # 1. 대상 디렉토리를 Path 객체로 변환
                                target_dir = Path(_temp_path)  
                                # 2. 상위(부모) 폴더 경로 지정
                                parent_dir = target_dir.parent
                                # 3. 대상 디렉토리가 존재하는지 확인
                                if not target_dir.exists():
                                    print(f"오류: '{target_dir}' 경로가 존재하지 않습니다.")
                                    return
                                # 4. 대상 폴더 안의 모든 아이템(파일/폴더) 순회
                                # iterdir()는 폴더 안의 내용을 가져옵니다.
                                for item in target_dir.iterdir():
                                    # 이동할 목표 경로 설정 (상위 폴더 경로 + 원래 이름)
                                    original_stem   = item.stem  # 파일 확장자를 제외한 이름 (예: 'test')
                                    extension       = item.suffix    # 파일 확장자 (예: '.txt')       
                                    time_digit      = str(time.time_ns())[-5:] # 중복방지를 위한 랜덤의 5자리수
                                    new_name        = f"{original_stem}-{time_digit}{extension}"
                                    #destination = parent_dir / item.name
                                    destination = parent_dir / new_name
                                    
                                    try:
                                        # shutil.move를 사용하여 파일/폴더 이동
                                        shutil.move(str(item), str(destination))
                                        print(f"이동 완료: {item.name} -> {parent_dir}")
                                    except Exception as e:
                                        print(f"이동 실패 ({item.name}): {e}")      
        
        # 하위 폴더의 파일수가 0이면 삭제 하는 스크립트
        for local_dir in base_path.iterdir(): # ncnc 폴더 아래 폴더 리스트
            if local_dir.is_dir():
                brand_path = Path(local_dir)
                for _item_fold in brand_path.iterdir():
                    if _item_fold.is_dir():
                        _last_fold = Path(_item_fold)
                        for _temp_path in _last_fold.iterdir():
                            if _temp_path.is_dir() :
                                target_dir = Path(_temp_path)  
                                _list = target_dir.iterdir()
                                if len(list(_list)) == 0 :
                                    target_dir.rmdir()

                        

                
  
    # 폴더 정리기 -- end
    
    # 실행
    def exec(self):
        # 1. json 파싱 처리
        lists = self.parse_standard_json()
        #fp.file_search(lists[1])
        
        # 2. 파일 경로 탐색및 명령 규정
        alter_name  = w2ji.getAlterProdList() #폴더명칭과 실제 상품명의 차이 때문에 해당 매핑을 이용한다.
        lists2 = []
        for list in lists:
            _temp = self.file_search(alter_name , list)
            lists2.append( _temp )

        # 3. 엑셀 생성
        self.export_to_excel( lists2 )        


if __name__ == "__main__":
    '''
    - 바코드의 중복여부는 중요하지 않다.
    - 판매완료와 반려만 분류 하여 local file 검출 하여 move와 rm 처리만 하면된다.
    - local file이 1개만 검출 되는지와 그렇지 않은 경우만 표기
    ex) 모두 확인후 빈폴더 삭제와 완료와 이상 폴더내 파일 상위 폴더로 이관 시키는 스크립트 필요.
    ex) 안정화 된 이후 2번 스크립트 자동 실행 부분 완성.


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
    
    fp = FileProc()    

    # json 생성및 파일 검출기
    fp.exec()

    #  폴더 정리 및 보유파일 0건 폴더 삭제 
    # 위 exec 처리후 파일 이관과 삭제작업을 완료한 이후에 주석을 제외하고 수행하면 정리가 된다.
    # fp.clearer_folder()
    