from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import pyperclip #복사
import time

import lib.util as w2ji
import lib.dbcon as dbcon
import pyautogui


def fnText(str):
    global driver
    _rt = ''
    try:        
        time.sleep(0.3)
        _html = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, str )))
        #print('fnTxt',_html.text)
        return _html.text
    except Exception as e:
        #print('fnText error : ',e)
        return _rt

def fnClick(str):
    global driver
    time.sleep(0.3)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, str ))).click()
    

def fnCopyNpaste( _str ):
    global driver
    time.sleep(0.2)
    pyperclip.copy( _str )
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    

def fnEnter():
    '''엔터입력'''   
    try:      
        global driver
        ActionChains(driver).send_keys(Keys.ENTER)
    except Exception as e:
        print('fnEnter error : ',e)  

def fnReadAlert():
    _rt = '문구없음'
    try:
        global driver
        WebDriverWait(driver, 3).until(
            EC.alert_is_present()
            , '문구없음'
        )
        alert = Alert(driver)
        _rt = alert.text        
        return _rt
    except Exception as e:
        print('fnReadAlert',e)
        return _rt



def fnLoging():
    '''로그인'''
    global driver
    __id = 'ycoplusone'
    __ps = 'natkfkdgo1!'    
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
    time.sleep(1.5)
    
    driver.switch_to.window( tabs[0] )           
    print('창 이동', driver.current_window_handle )       
    time.sleep(1.5)
    driver.get('https://ncnc.app/sell/wait-confirmed')  
    time.sleep(0.5)

    #로그인 클릭
    '''
    fnClick( '//*[@id="app"]/div/div[2]/div/div/div/button[4]/div') 
    fnClick( '//*[@id="username"]')    
    fnCopyNpaste( __id )   

    fnClick( '//*[@id="password"]')    
    fnCopyNpaste( __ps )    

    fnClick( '//*[@id="app"]/div/div[2]/div/div/div/button')        
    fnClick( '//*[@id="app"]/div/nav/a[2]')
    time.sleep(0.5)
    '''

def fnDiv01( str = '카' ):
    '''대분류 찾기'''
    _state = False    
    try:
        fnClick( '//*[@id="app"]/div/div[2]/div/section/div/section/section[1]/div/button')    
        _div01 = ''
        if str == '카':
            _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[2]/div'
        elif str == '편':
            _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[3]/div'
        elif str == '빵':
            _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[4]/div'
        elif str == '피':
            _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[5]/div'
        elif str == '문':
            _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[6]/div'
        elif str == '외':
            _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[7]/div'
        elif str == '백':
            _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[8]/div'
        elif str == '휴':
            _div01 = '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/a[9]/div'        
            print(_div01)
        fnClick(_div01)
        time.sleep(0.25)
        _state = True
        return _state
    except Exception as e:
        print('ERROR fnDiv01',e)
        return _state

def fnDiv02( _str = '투썸플레이스' ):
    '''중분류 찾기(카테고리 찾기)'''    
    _state = False
    try:
        fnClick( '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/div[2]/input') # 검색바 클릭
        fnCopyNpaste( _str )
        fnClick( '//*[@id="items-container"]/a[2]') #두번째 아이콘 클릭
        time.sleep(0.25)
        _state = True
        return _state
    except Exception as e:
        print('ERROR fnDiv02',e)
        return _state


def fnDiv03( _str = '아메리카노 L' ):
    '''하분류 찾기(상품 차지)'''
    _state = False
    global driver
    item_name  = '//*[@id="items-container"]/a[2]'
    item_state = '/html/body/div[1]/div/div[2]/div/section/div/div/div/section/div[3]/a[2]/div[2]'
    item_seq = '2'
    try:
        fnClick( '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/div[2]/input') #검색바 클릭
        fnCopyNpaste( _str )    
        time.sleep(0.2) # 딜레이.

        # 상품 리스트 가져오기
        titles = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='horizontal-box']")))
        #print("배열길이:", len(titles))
        # 복수개(3개)의 앨리먼트가 추출 됨 (3개중 마지막)
        for i in range(len(titles)):
            xpath_str1 = '/html/body/div[1]/div/div[2]/div/section/div/div/div/section/div[3]/a['+str(i)+']/div[1]/div[1]'
            xpath_str2 = '/html/body/div[1]/div/div[2]/div/section/div/div/div/section/div[3]/a['+str(i)+']/div[2]'
            tag_name = fnText(xpath_str1)
            if ( tag_name  == _str):
                print( tag_name , i )
                item_name  = '//*[@id="items-container"]/a['+str(i)+']'
                item_state = xpath_str2
                break
        
        _sale_type = fnText( item_state ) #상품판매상태 확인
        print('_sale_type : ', _sale_type )
        print('item_name  : ', item_name  )
        print('item_state : ', item_state )

        if (_sale_type == '매입보류') or (_sale_type=='') :
            w2ji.send_telegram_message( _str+' : '+ '매입보류' )
            _state = False
        else :
            #fnClick( '//*[@id="items-container"]/a[2]') # 두번째 아이콘 클릭
            fnClick( item_name ) # 두번째 클릭
            _state = True
        
        return _state
    except Exception as e:
        print('ERROR fnDiv03',e)
        return _state

def fnSale( _nm = '' , _amt = '' , _fold_nm = '' , _files = [] ):
    '''판매 '''
    global driver
    try:
        for file in _files:
            driver.find_element(By.CSS_SELECTOR , "input[type='file']").send_keys(file) #파일 등록
    
        fnClick('//*[@id="app"]/div/div[2]/div/section/div/div/div/section/button') # 판매 등록
        time.sleep(1)    
        alert_txt = fnReadAlert() # 알림창 읽기
        #if alert_txt != '문구없음':
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

        time.sleep(0.3)
        driver.refresh() #브라이져 새로고침
    except Exception as e:
        print('fnSale',e)

def fnInit():
    '''크룸 초기화'''
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument('window-size=1024x768')    
    _rt = webdriver.Chrome('chromedriver.exe' , options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
    _rt.get('https://ncnc.app/sell/wait-confirmed')
    _rt.implicitly_wait(5)  
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
    fnLoging() #매개변수 없음

    fnDiv01( )  # 대분류 첫글짜 매개변수
    fnDiv02( )   # 중분류명 매개변수
    fnDiv03( )   # 상품명 매개변수	
    fnClick( '//*[@id="warning-agree"]/label/div' ) # 동의 체크
    driver.refresh() #브라이져 새로고침	
    
    while(True):
        
        _tmp = _dbconn.getNiconState()
        if _lastupdate != _tmp:            
            print('시작 : ',w2ji.getNow() )
            _lastupdate = _tmp
            __lists    = _dbconn.get_nicon_upload_list()
            for list in __lists:
                print('list : ',list)
                div01_str = list['div_nm']
                div02_str = list['category_nm']
                div03_str = list['prod_nm']
                fold_nm   = list['fold_nm']
                amt       = str( list['amount'] )
                prod_fold_list = w2ji.getfolelist( fold_nm )
                for _fold_nm in prod_fold_list:
                    driver.refresh() #브라이져 새로고침
                    try:
                        _bool_01 = fnDiv01( div01_str )   # 대분류 첫글짜 매개변수
                        if _bool_01:
                            _bool_02 = fnDiv02( div02_str )   # 중분류명 매개변수
                            if _bool_02:
                                _bool_03 = fnDiv03( div03_str )   # 상품명 매개변수
                                if _bool_03:
                                    print('판매시작')
                                    files = w2ji.getFileList( _fold_nm ) #상품폴더내 파일 리스트 생성
                                    fnSale(fold_nm , amt, _fold_nm, files ) # 판매
                    except Exception as e:
                        print( '판매 작업중 오류',e )
        #else:
            #print('\t','nicon_state 변경 없음')
        time.sleep(3)