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


'''
btns = driver.find_elements( By.XPATH , '//*[@id="grid"]/div[*]')
print(len(btns))
print(btns[0].text) #0번 요소의 텍스트
print()
'''
def fnClick(str):
    global driver
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, str ))).click()

def fnCopyNpaste( _str ):
    global driver
    pyperclip.copy( _str )
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

def fnEnter():
    '''엔터입력'''    
    pyautogui.press('enter')

def fnReadAlert():
    global driver
    alert = Alert(driver)
    return alert.text


def fnLoging():
    '''로그인'''
    global driver
    __id = 'ycoplusone'
    __ps = 'Nitkfkdgo1!'    

    fnClick('//*[@id="app"]/div/div[2]/div/section/section/nav/section/button')

    fnClick('//*[@id="app"]/div/div[2]/div/div/div/section/div[4]/a/span')

    fnClick( '//*[@id="app"]/div/div[2]/div/div/div/button[4]/div') 
    

    fnClick( '//*[@id="username"]')    
    fnCopyNpaste( __id )
    

    fnClick( '//*[@id="password"]')    
    fnCopyNpaste( __ps )    

    fnClick( '//*[@id="app"]/div/div[2]/div/div/div/button')        
    fnClick( '//*[@id="app"]/div/nav/a[2]')
    time.sleep(0.5)

def fnDiv01( str = '카' ):
    '''대분류 찾기'''    
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
    time.sleep(0.5)

def fnDiv02( _str = '투썸플레이스' ):
    '''중분류 찾기(카테고리 찾기)'''
    
    fnClick( '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/div[2]/input') # 검색바 클릭
    fnCopyNpaste( _str )
    fnClick( '//*[@id="items-container"]/a[2]') #두번째 아이콘 클릭
    time.sleep(0.5)

def fnDiv03( _str = '아메리카노 R' ):
    '''하분류 찾기(상품 차지)'''
    fnClick( '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/div[2]/input') #검색바 클릭
    fnCopyNpaste( _str )
    fnClick( '//*[@id="items-container"]/a[2]') # 두번째 아이콘 클릭

def fnSale( _nm = '' , _amt = '' , _fold_nm = '' , _files = [] ):
    '''판매 '''
    global driver
    fnClick( '//*[@id="warning-agree"]/label/div' ) # 동의 체크

    for file in _files:
        driver.find_element(By.CSS_SELECTOR , "input[type='file']").send_keys(file) #파일 등록
    
    fnClick('//*[@id="app"]/div/div[2]/div/section/div/div/div/section/button') # 판매 등록
    time.sleep(1)    
    alert_txt = fnReadAlert() # 알림창 읽기

    telegram_str = '정상 : '+alert_txt+'\n\n'
    telegram_str += _nm +' : '+ _amt +'\n\n'
    telegram_str += '원본 : '+ _fold_nm +'\n\n'
    telegram_str += '완료 : '+ w2ji.complete_fold(_fold_nm)
    w2ji.send_telegram_message(  telegram_str )
    w2ji.mk_image() # 스샷 생성
    # 완료 메세지
    # 폴더 완료 적용    
    fnEnter() #엔터

def fnInit():
    '''크룸 초기화'''
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument('window-size=1024x768')    
    _rt = webdriver.Chrome('chromedriver.exe' , options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
    _rt.get('https://ncnc.app/sell/wait-confirmed')
    _rt.implicitly_wait(5)    
    return _rt

if __name__ == "__main__":   
    ''''''
    _lastupdate = '' # 업데이트 시간 저장
    _dbconn = dbcon.DbConn() #db연결    

    print('기본폴더 생성','-'*10)
    w2ji.base_fold_create(_dbconn) #기초폴더 생성
    
    w2ji.init_fold(_dbconn) #폴더내 파일 정리.
    
    driver = fnInit() #초기화        
    fnLoging() #매개변수 없음
    
    while(True):
        print('시작 : ',w2ji.getNow() )
        _tmp = _dbconn.getNiconState()
        if _lastupdate != _tmp:
            print('\t','작업 수행')
            _lastupdate = _tmp
            __lists    = _dbconn.get_nicon_upload_list()
            print( '__lists : ', __lists ,'\n')
            for list in __lists:
                print(list)
                div01_str = list['div_nm']
                div02_str = list['category_nm']
                div03_str = list['prod_nm']
                fold_nm   = list['fold_nm']
                amt       = str( list['amount'] )
                prod_fold_list = w2ji.getfolelist( fold_nm )
                for _fold_nm in prod_fold_list:
                    driver.refresh() #브라이져 새로고침
                    fnDiv01( div01_str )  # 대분류 첫글짜 매개변수
                    fnDiv02( div02_str )   # 중분류명 매개변수
                    fnDiv03( div03_str )   # 상품명 매개변수
                    files = w2ji.getFileList( _fold_nm ) #상품폴더내 파일 리스트 생성
                    fnSale(fold_nm , amt, _fold_nm, files ) # 판매

        else:
            print('\t','nicon_state 변경 없음')
        time.sleep(5)
    

    #driver = fnInit() #초기화    
    
    #fnLoging() #매개변수 없음
    #driver.refresh() #브라이져 새로고침
    #fnDiv01()  # 대분류 첫글짜 매개변수
    #fnDiv02()   # 중분류명 매개변수
    #fnDiv03()   # 상품명 매개변수
    #fnSale()

    