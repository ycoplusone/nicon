import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import pyperclip #복사
import time
from pytz import timezone
from datetime import datetime

from PIL import ImageGrab , Image # pip install pillow

def fnClick( driver , str):
    time.sleep(0.3)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, str ))).click()

def fnCopyNpaste( driver , _str ):
    time.sleep(0.2)
    pyperclip.copy( _str )
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

def fnReadAlert( driver):
    _rt = '문구없음'
    try:        
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

def mk_image(tel , name):
    '''캡쳐 만들기'''
    try:
        
        img = ImageGrab.grab()
        imgCrop = img.crop( (0,0,1024,768))
        base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
        str = base_dttm+'_'+tel+'('+name+')'
        file_name = 'c:\\ncnc\\ktevent\\{}{}'.format( str ,'.png')
        imgCrop.save(file_name)
    except Exception as e:
        print('mk_image : ',e)



def fnInit():
    '''크룸 초기화'''
    options = webdriver.ChromeOptions()    
    options.add_argument('--window-size=1024x768')    
    options.add_argument('incognito') # incognito 시크릿 모드입니다.

    _rt = webdriver.Chrome('chromedriver.exe' , options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
    _rt.get('https://pack.kt.com/event/2024Roulette/m/entry.asp')
    _rt.implicitly_wait(5)  
    time.sleep(1)  
    return _rt


def readfile():
    '''파일 읽기'''
    _rt = []
    f = open('C:\\Users\\DLIVE\\eclipse-workspace\\nicon\\event\\data\\test.cvs', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        _rt.append( line )
    f.close()    
    return _rt

if __name__ == "__main__":    
    _list = readfile() 
    br = fnInit() # 브라우저 로딩
    for i in _list:        
        
        try:
            br.refresh()
            # 이름 등록
            fnClick( br , '//*[@id="pUserName"]' )
            fnCopyNpaste( br , i[1])

            # 이름 등록
            fnClick( br , '//*[@id="Phone"]' )
            fnCopyNpaste( br , i[0])

            # 전체 동의 클릭
            fnClick( br , '//*[@id="Agree_all"]' )

            # 전체 동의 클릭
            fnClick( br , '//*[@id="btn_enter"]' )

            result = br.switch_to.alert()
            result.accept()
                        
            time.sleep(2)
            mk_image(i[0],i[1]) # 스샷 생성
            time.sleep(1)
            #br.close
            #br.refresh()
            #br.get(br.current_url)
            
            
        except Exception as e:
            print( 'ex 발생', e  )
            time.sleep(2)
            mk_image(i[0],i[1]) # 스샷 생성
            time.sleep(1)
        
    
