from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip #복사
import time

import lib.util as w2ji
import lib.dbcon as dbcon
import datetime



def fnClick(str):
    global driver
    time.sleep(0.15)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, str ))).click()
    

def fnCopyNpaste( _str ):
    global driver
    time.sleep(0.2)
    pyperclip.copy( _str )
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    
def fnReadAlert():
    _rt = '문구없음'
    try:
        global driver
        alert_present = WebDriverWait(driver, 2).until(EC.alert_is_present())
        if alert_present :
            result = driver.switch_to.alert
            _rt = result.text                
            return _rt
    except Exception as e:
        print( 'alert error', e )
        return _rt

def fn_exe_script( script ):
    '''스크립트 실행'''
    global driver
    time.sleep(0.1)
    start_time = datetime.datetime.now()
    _ret_script = "return document.readyState === 'complete';"
    while not driver.execute_script(_ret_script):
        pass
    
    end_time = datetime.datetime.now()     
    # 소요 시간 계산
    elapsed_time = end_time - start_time
    # 결과 출력
    print('*'*50)
    print('fn_exe_script : ', script , '\t : \t', elapsed_time  , ' : ', elapsed_time.total_seconds() * 3 )   
    print('*'*50)
    time.sleep( elapsed_time.total_seconds() *3 )

    _rt = ''
    try:
        _rt = driver.execute_script( script )
    except Exception as e:
        print('fn_exe_script : ',e)
    
    return _rt


def fnLoging():
    '''로그인'''
    global driver
    __id = 'skfmtltm1052'
    __ps = 'Natktkfkd84!'    
    time.sleep(0.2)
    fnClick('//*[@id="app"]/div/div[2]/div/section/section/nav/section/button')
    
    fnClick('//*[@id="app"]/div/div[2]/div/div/div/section/div[4]/a/span')

    fnClick('/html/body/div[1]/div/div[2]/div/div/div/button[1]/div') #네이버 클릭
    time.sleep(0.5)
    tabs = driver.window_handles
    print(tabs)
    driver.switch_to.window( tabs[1] )        
    print('창 이동', driver.current_window_handle )     

    fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[2]/div[1]/input') #id    
    fnCopyNpaste( __id )   
    fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[2]/div[2]/input') #ps
    fnCopyNpaste( __ps )    
    fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[8]/button/span') #확인
    time.sleep(10)
    
    driver.switch_to.window( tabs[0] )           
    print('창 이동', driver.current_window_handle )       
    time.sleep(1.5)
    driver.get('https://ncnc.app/sell/wait-confirmed')  
    time.sleep(0.5)

def fnDiv01( str = '카' ): #str = '카'
    '''대분류 찾기'''
    _state = False    
    try:
        fn_exe_script('$("#app > div > div.right-container > div > section > div > section > section.flex.flex-column.bb-ccc > div > button").click()');        
        _div01 = ''
        if str == '카':
            _div01 = '$("#app > div > div.right-container > div > section > div > div > div > section > a:nth-child(3) > div").click();'
        elif str == '편':
            _div01 = '$("#app > div > div.right-container > div > section > div > div > div > section > a:nth-child(4) > div").click();'
        elif str == '빵':
            _div01 = '$("#app > div > div.right-container > div > section > div > div > div > section > a:nth-child(5) > div").click();'
        elif str == '피':
            _div01 = '$("#app > div > div.right-container > div > section > div > div > div > section > a:nth-child(6) > div").click();'
        elif str == '문':
            _div01 = '$("#app > div > div.right-container > div > section > div > div > div > section > a:nth-child(7) > div").click();'
        elif str == '외':
            _div01 = '$("#app > div > div.right-container > div > section > div > div > div > section > a:nth-child(8) > div").click();'
        elif str == '백':
            _div01 = '$("#app > div > div.right-container > div > section > div > div > div > section > a:nth-child(9) > div").click();'
        elif str == '휴':
            _div01 = '$("#app > div > div.right-container > div > section > div > div > div > section > a:nth-child(10) > div").click();'
        fn_exe_script(_div01)
        _state = True
        return _state
    except Exception as e:
        print('ERROR fnDiv01',e)
        return _state

def fnDiv02_1( _str = '2' ): # _str = '2' 투썸플레이스이다.
    '''중분류 찾기(카테고리 찾기)'''    
    _state = False
    try:
        seq = int(_str)+1
        tag = '$("#items-container > a:nth-child({}) > div > img").click();'.format(seq)    
        fn_exe_script( tag )
        _state = True
        return _state
    except Exception as e:
        print('ERROR fnDiv02',e)
        return _state

def fnDiv03_1( _str = '11' ): # _str = 11 '아메리카노 L'
    '''하분류 찾기(상품 차지)'''
    _state = False
    _sale_type = ''
    _prod_nm = ''
    _send_txt = ''
    global driver
    try:
        seq = int(_str)+1
        tag1 = '$("#items-container > a:nth-child({}) > img").click();'.format(seq) # 링크 테그
        tag2 = 'return $("#items-container > a:nth-child({})").text();'.format(seq)  #판매중 판매보류 값 가져오기
        _txt = fn_exe_script(tag2)
        if _txt[-2:] == '보류':
            _sale_type = '매입보류'
        else :
            _sale_type = '판매중'   
        
        _prod_nm = _txt.split('예상')[0]
        
        _send_txt = '{} : {}'.format( _prod_nm , _sale_type)
        
        print('*'*50)
        print('_sale_type : ', _send_txt )

        if (_sale_type == '매입보류') or (_sale_type=='') :
            w2ji.send_telegram_message( _send_txt )
            _state = False
        else :
            fn_exe_script( tag1 )
            _state = True     
  
        return _state
    except Exception as e:
        print('ERROR fnDiv03_1',e)
        time.sleep(0.2)
        return _state    
    

def fnSale( _nm = '' , _amt = '' , _fold_nm = '' , _files = [] ):
    '''판매 '''
    global driver
    try:
        upload = driver.find_element(By.CLASS_NAME,'input-file')
        for file in _files:
            upload.send_keys(file) #파일등록
    
        tag = '$("#app > div > div.right-container > div > section > div > div > div > section > button").click();'     # 링크 테그
        fn_exe_script(tag)

        alert_txt = fnReadAlert() # 알림창 읽기

        if '쿠폰이 등록' in alert_txt :
            telegram_str = '정상 : '+alert_txt+'\n\n'
            telegram_str += _nm +' : '+ _amt +'\n\n'
            telegram_str += '원본 : '+ _fold_nm +'\n\n'
            telegram_str += '완료 : '+ w2ji.complete_fold(_fold_nm , True)
            w2ji.send_telegram_message(  telegram_str )
            w2ji.mk_image() # 스샷 생성
        else:
            telegram_str = '이상 : '+alert_txt+'\n\n'
            telegram_str += _nm +' : '+ _amt +'\n\n'
            telegram_str += '원본 : '+ _fold_nm +'\n\n'
            telegram_str += '완료 : '+ w2ji.complete_fold(_fold_nm , False)
            w2ji.send_telegram_message(  telegram_str )

        time.sleep(0.1)
        driver.refresh() #브라이져 새로고침
    except Exception as e:
        print('fnSale',e)

def fnInit():
    '''크룸 초기화'''
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1024x768')   
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage") 
    '''
    options.add_argument('--headless')    
    options.add_argument('--disable-images')
    options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
    options.add_argument('--blink-settings=imagesEnabled=false')        
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--incognito')    
    '''
    _rt = webdriver.Chrome('chromedriver.exe' , options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
    _rt.get('https://ncnc.app/sell/wait-confirmed')
    _rt.implicitly_wait(2)  
    time.sleep(1)  
    return _rt

if __name__ == "__main__":   
    ''''''   
    _lastupdate = '' # 업데이트 시간 저장
    _dbconn = dbcon.DbConn() #db연결    
    
    print('기본폴더 생성','-'*10)
    w2ji.base_fold_create(_dbconn) #기초폴더 생성    
    w2ji.into_rename_barcode() #파일명 바코드 명으로 변경작업 바코드 생성 못하면   None으로 치환된다.
    w2ji.init_fold(_dbconn) #폴더내 파일 정리.    
    driver = fnInit() #초기화    
    time.sleep(1)
    
    # 시작 시간 기록
    
    
    fnLoging() #매개변수 없음
    start_time = datetime.datetime.now()
    fnDiv01( )  # 대분류 첫글짜 매개변수
    fnDiv02_1( )   # 중분류명 매개변수
    fnDiv03_1( )   # 상품명 매개변수	
    fnClick( '//*[@id="warning-agree"]/label/div' ) # 동의 체크
    
    ''' # 상품까지의 테스트 코드
    fold_nm = 'CU_1만원권'
    _fold_nm = 'C:\\ncnc\\CU_1만원권\\abc'
    amt = '123'
    files = w2ji.getFileList( _fold_nm ) #상품폴더내 파일 리스트 생성
    fnSale(fold_nm , amt, _fold_nm, files ) # 판매
    '''


    driver.refresh() #브라이져 새로고침	
    # 끝 시간 기록
    end_time = datetime.datetime.now() 
    # 소요 시간 계산
    elapsed_time = end_time - start_time
    # 결과 출력
    print("작업이 소요된 시간:", elapsed_time)               
    
    while(True): 
        try:           
            _tmp = _dbconn.getNiconState()
            #if _lastupdate != _tmp:            
            if True:                
                _lastupdate = _tmp
                __lists    = _dbconn.get_nicon_upload_list()
                print('시작 : ',w2ji.getNow() , '\t 상품 갯수 : ', len( __lists ))                
                _dbconn.insert_nicon_client_log() #로그 등록

                for list in __lists:             
                    div01_str   = list['div_nm']
                    div02_str   = list['category_nm']
                    div02_str_1 = list['cat_seq']
                    div03_str   = list['prod_nm']
                    div03_str_1 = list['prod_seq']
                    fold_nm     = list['fold_nm']
                    amt         = str( list['amount'] )
                    
                    prod_fold_list = w2ji.getfolelist( fold_nm )
                    for _fold_nm in prod_fold_list:
                        driver.refresh() #브라이져 새로고침
                        time.sleep(0.1)
                        try:
                            _bool_01 = fnDiv01( div01_str )   # 대분류 첫글짜 매개변수
                            if _bool_01:
                                _bool_02 = fnDiv02_1( div02_str_1 )   # 중분류명 매개변수
                                if _bool_02:
                                    _bool_03 = fnDiv03_1( div03_str_1 )   # 상품명 매개변수
                                    if _bool_03:
                                        files = w2ji.getFileList( _fold_nm ) #상품폴더내 파일 리스트 생성
                                        fnSale(fold_nm , amt, _fold_nm, files ) # 판매
                                    else:
                                        break

                        except Exception as e:
                            print( '판매 작업중 오류',e )
            time.sleep(0.5)
        except Exception as e:
            w2ji.send_telegram_message(  'nicon restart ' )
            time.sleep(10)
