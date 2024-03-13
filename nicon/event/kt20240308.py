import csv
import os

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

def mk_image(tel , name):
    '''캡쳐 만들기'''
    try:        
        img = ImageGrab.grab()
        imgCrop = img.crop( (0,0,1024,768))
        base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
        str = tel+'('+name+')'
        file_name = 'c:\\ncnc\\ktevent\\{}\\{}{}'.format(base_dttm, str ,'.png')
        imgCrop.save(file_name)
    except Exception as e:
        print('mk_image : ',e)

def mk_fold():
    try:        
        base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
        _path = 'c:\\ncnc\\ktevent\\{}'.format(base_dttm)
        os.mkdir( _path )
    except Exception as e:
        print( e )



def fnInit():
    '''크룸 초기화'''
    options = webdriver.ChromeOptions()    
    options.add_argument('--window-size=1024x768')    
    options.add_argument('incognito') # incognito 시크릿 모드입니다.

    #_rt = webdriver.Chrome('C:\\nicon\\chromedriver.exe' , options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
    _rt = webdriver.Chrome('C:\\Users\\DLIVE\\eclipse-workspace\\nicon\\chromedriver.exe' , options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
    _rt.get('https://pack.kt.com/event/2024Roulette/m/entry.asp')
    _rt.implicitly_wait(5)  
    time.sleep(1)  
    return _rt

def fnInit_chk():
    '''크룸 초기화 당첨 확인'''
    options = webdriver.ChromeOptions()    
    options.add_argument('--window-size=1024x768')    
    options.add_argument('incognito') # incognito 시크릿 모드입니다.

    #_rt = webdriver.Chrome('C:\\nicon\\chromedriver.exe' , options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
    _rt = webdriver.Chrome('C:\\Users\\DLIVE\\eclipse-workspace\\nicon\\chromedriver.exe' , options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
    _rt.get('https://pack.kt.com/event/2024Roulette/m/win.asp')
    _rt.implicitly_wait(5)  
    time.sleep(1)  
    return _rt


def readfile(path):
    '''파일 읽기'''
    _rt = []
    f = open(path+'\\test.cvs', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        _rt.append( line )
    f.close()    
    return _rt    

def main( _list ):
    '''이벤트 참여'''
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
            time.sleep(1)
            try:
                alert_present = WebDriverWait(br, 5).until(EC.alert_is_present())
                if alert_present :
                    result = br.switch_to.alert
                    result.accept()
            except Exception as e:
                print( 'alert error', e )

            try:
                alert_present = WebDriverWait(br, 5).until(EC.alert_is_present())
                if alert_present :
                    result = br.switch_to.alert
                    result.accept()
                    
                    #경품 클릭
                    fnClick( br , '//*[@id="btn-start"]' )
                    #time.sleep(4)
                    #mk_image(i[0],i[1]) # 스샷 생성
                    time.sleep(1)
                    br.get('https://pack.kt.com/event/2024Roulette/m/entry.asp')
                    
            except Exception as e:
                print(i[0],' / ',i[1])
                br = fnInit() # 브라우저 로딩
                time.sleep(1)                    
            
        except Exception as e:
            print( 'ex 발생', e  )

def event_chk( _list , path ):
    '''이벤트 당첨 확인'''
    br = fnInit_chk() # 브라우저 로딩    
    _rt_list = []
    for i in _list:                        
        try:
            rt = { 'tel':i[0] , 'nm': i[1] , 'div' : '꽝'}
            br.refresh()            
            fnClick( br , '//*[@id="pUserName"]' )             
            fnCopyNpaste( br , i[1])            

            fnClick( br , '//*[@id="Phone"]' )
            fnCopyNpaste( br , i[0])

            fnClick( br , '//*[@id="btn_enter"]' )           
            
            time.sleep(1)
            _alert_txt = ''
            try:
                alert_present = WebDriverWait(br, 2).until(EC.alert_is_present())
                if alert_present :
                    result = br.switch_to.alert
                    _alert_txt = result.text
                    _alert_txt = ''
                    result.accept()
            except Exception as e:
                print( '알림' , i )                    

            try:
                _htmls = WebDriverWait(br, 1).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div/h1/img' )))
                rt['div'] = str(_htmls[0].get_attribute('alt'))                
            except Exception as e:
                print('이미지1',i)                
            
            try:
                _htmls = WebDriverWait(br, 1).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div[1]/div/span/img' )))
                rt['div'] = str(_htmls[0].get_attribute('alt'))                
            except Exception as e:
                print('이미지2',i)           
            
            _rt_list.append( rt )            
            
            br.get('https://pack.kt.com/event/2024Roulette/m/win.asp')
            
        except Exception as e:
            print( 'ex 발생', e  )
    print('끝0----------------------------')
    sorted_list = sorted(_rt_list, key=lambda x: x['div'])
    _t = []
    for i in sorted_list:
        _tt = []
        _tt.append( i['tel'] )
        _tt.append( i['nm']  )
        _tt.append( i['div'] )
        _t.append( _tt )     
    
    base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
    _file_path = path+'\\'+base_dttm+'.cvs'
    with open(_file_path, mode='w', newline='' , encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(_t)
    


if __name__ == "__main__":    
    #path = 'C:\\nicon\\event\\data'
    path = 'C:\\Users\\DLIVE\\eclipse-workspace\\nicon\\event\\data'
    _list = readfile( path )    
    main( _list )
    event_chk( _list , path )