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
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
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


def getCophon():
    global driver
    # 상품 클릭
    driver.get('http://www.10x10.co.kr/shopping/category_prd.asp?itemid=5420951&disp=104125101&pRtr=%EC%BB%AC%EC%B3%90%EB%9E%9C%EB%93%9C&rc=rpos_1_1')
    # 쿠폰 받기 
    fnClick( '/html/body/div[2]/div[7]/div/div[1]/div[2]/div[1]/div[1]/form[2]/div[2]/dl[2]/dd/a/span')    

    tabs = driver.window_handles
    driver.switch_to.window( tabs[1] )
    #driver.switch_to_window(driver.window_handles[1])  
    # 쿠폰받기 다운로드
    fnClick('/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/a/span')
    time.sleep(1)
    driver.switch_to.alert.accept()    # 자식 알림창 확인    
    driver.switch_to.window( tabs[0] ) #다시 메인창 전환
    time.sleep(0.3)
    
    # 바로구매 클릭
    fnClick('/html/body/div[2]/div[7]/div/div[1]/div[2]/div[2]/span[1]/a')
    
    # 전화번호 입력1
    fnClick('/html/body/div[2]/div[8]/div/div/div[2]/form/table[2]/tbody/tr[4]/td[2]/input[1]')
    fnCopyNpaste('010')
    # 전화번호 입력2
    fnClick('/html/body/div[2]/div[8]/div/div/div[2]/form/table[2]/tbody/tr[4]/td[2]/input[2]')
    fnCopyNpaste('3020')

    # 전화번호 입력3
    fnClick('/html/body/div[2]/div[8]/div/div/div[2]/form/table[2]/tbody/tr[4]/td[2]/input[3]')
    fnCopyNpaste('2281')

    # 구매금액 입력
    fnClick('/html/body/div[2]/div[8]/div/div/div[2]/form/div[4]/div[1]/table/tbody/tr[5]/td[1]/input')
    fnCopyNpaste('9300')

    # 구매동의
    fnClick('/html/body/div[2]/div[8]/div/div/div[2]/form/div[7]/div/label/input')

    #결제하기
    fnClick('/html/body/div[2]/div[8]/div/div/div[2]/form/div[8]/a[2]')
    time.sleep(0.3)
    driver.switch_to.alert.accept()    # 자식 알림창 확인    
    
    

        
        

def fnLoging():
    '''로그인'''
    global driver
    __id = 'skfmtltmxm84'
    __ps = '10tktkfkd84!'    
    time.sleep(0.2)
    #fnClick('//*[@id="app"]/div/div[2]/div/section/section/nav/section/button')

    #fnClick('//*[@id="app"]/div/div[2]/div/div/div/section/div[4]/a/span')

    #fnClick( '//*[@id="app"]/div/div[2]/div/div/div/button[4]/div') 
    

    fnClick( '/html/body/div[2]/div[8]/div/div/div/div[1]/form/fieldset/div[1]/div/input')    
    fnCopyNpaste( __id )
    

    fnClick( '/html/body/div[2]/div[8]/div/div/div/div[1]/form/fieldset/div[2]/div/input')    
    fnCopyNpaste( __ps )    

    fnClick( '/html/body/div[2]/div[8]/div/div/div/div[1]/form/p[2]')        
    time.sleep(0.5)
    
    



def fnInit():
    '''크룸 초기화'''
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument('window-size=1024x768')    
    _rt = webdriver.Chrome('chromedriver.exe' , options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
    _rt.get('https://www.10x10.co.kr/login/loginpage.asp?vType=G')
    _rt.implicitly_wait(5)  
    time.sleep(1)  
    return _rt

if __name__ == "__main__":   
    ''' 문화상품권 만원권 구매 '''
    
    driver = fnInit() #초기화        
    time.sleep(1)
    fnLoging() #매개변수 없음
    time.sleep(1)
    for i in range(0,1000):
        print('횟수',i)
        getCophon()


    
