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
        print('fnText error : ',e)
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
    #print('창 이동', driver.current_window_handle )  

       


    fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[2]/div[1]/input') #id    
    fnCopyNpaste( __id )   
    fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[2]/div[2]/input') #ps
    fnCopyNpaste( __ps )    
    fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[8]/button/span') #확인
    time.sleep(0.5)
    #driver.close()
    driver.switch_to.window( tabs[0] )           
    print('창 이동', driver.current_window_handle )       
    time.sleep(0.5)
    driver.get('https://ncnc.app/sell/wait-confirmed')  
    time.sleep(0.3)

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
    try:
        fnClick( '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/div[2]/input') #검색바 클릭
        fnCopyNpaste( _str )    
        time.sleep(0.2) # 딜레이.
        _sale_type = fnText( '/html/body/div[1]/div/div[2]/div/section/div/div/div/section/div[3]/a[2]/div[2]' ) #상품판매상태 확인
        if (_sale_type == '매입보류') or (_sale_type=='') :
            w2ji.send_telegram_message( _str+' : '+ '매입보류' )
            _state = False
        else :
            fnClick( '//*[@id="items-container"]/a[2]') # 두번째 아이콘 클릭
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
        if alert_txt != '문구없음':
            telegram_str = '정상 : '+alert_txt+'\n\n'
            telegram_str += _nm +' : '+ _amt +'\n\n'
            telegram_str += '원본 : '+ _fold_nm +'\n\n'
            telegram_str += '완료 : '+ w2ji.complete_fold(_fold_nm)
            w2ji.send_telegram_message(  telegram_str )
            w2ji.mk_image() # 스샷 생성
            # 완료 메세지
            # 폴더 완료 적용    
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
    
    driver = fnInit() #초기화    
    time.sleep(1)
    fnLoging() #매개변수 없음   
  