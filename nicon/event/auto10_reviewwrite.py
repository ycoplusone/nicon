from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import pyperclip #복사
import time
import random

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

def ranTxt():
    lists = [
            '완벽한 선물이었습니다.'
            ,'다양한 상품 선택이 가능해요.'
            ,'원하는 상품을 자유롭게 고를 수 있어요.'
            ,'기대 이상의 다양한 상품 구매 가능!'
            ,'특별한 선물로 큰 환호를 받았어요.'
            ,'다양한 브랜드와 제품을 만날 수 있어 좋아요.'
            ,'원하는 상품을 마음껏 골라보세요.'
            ,'다른 사람들과 공유하기에 좋은 선물이에요.'
            ,'상품 선택의 폭이 넓어서 좋았어요.'
            ,'다양한 쇼핑 재미를 경험할 수 있어요.'
            ,'특별한 경험을 선물해줄 수 있는 아이템.'
            ,'자유롭게 마음에 드는 상품을 골라보세요.'
            ,'다양한 카테고리의 상품들이 매력적이에요.'
            ,'상품권으로 마음에 드는 것을 골라보세요.'
            ,'원하는 대로 사용할 수 있는 최고의 선물.'
            ,'상품권으로 특별한 경험을 선물해보세요.'
            ,'다양한 상품 중에서 마음에 드는 것을 찾아보세요.'
            ,'상품을 직접 고를 수 있는 재미가 있어요.'
            ,'상품을 마음에 따라 선택할 수 있는 자유로움.'
            ,'사람들에게 다양한 선택의 폭을 선물해보세요.'
            ,'상품권으로 마음에 드는 상품을 골라보세요.'
            ,'다양한 브랜드와 제품들을 만나볼 수 있어요.'
            ,'특별한 선물로 상품 선택의 즐거움을 선사해요.'
            ,'상품권으로 다양한 쇼핑의 즐거움을 누려보세요.'
            ,'상품 선택의 자유로움을 선물해드립니다.'
            ,'다양한 카테고리에서 마음에 드는 상품을 찾아보세요.'
            ,'상품권으로 원하는 상품을 마음껏 고를 수 있어요.'
            ,'상품권으로 특별한 선물을 선사해보세요.'
            ,'다양한 선택의 폭을 경험해볼 수 있는 기회입니다.'
            ,'원하는 상품을 선택할 수 있는 자유로움을 선물하세요.'
            ,'상품권으로 다양한 상품을 자유롭게 고를 수 있어요.'
            ,'특별한 선물로 다양한 상품의 선택을 선사해보세요.'
            ,'상품권으로 원하는 상품을 마음껏 고를 수 있는 기회입니다.'
            ,'원하는 대로 상품을 선택할 수 있는 자유로움을 선물하세요.'
            ,'상품권으로 특별한 경험과 다양한 상품을 만나보세요.'
            ,'다양한 카테고리에서 마음에 드는 상품을 골라보세요.'
            ,'상품권으로 마음에 드는 상품을 자유롭게 골라보세요.'
            ,'다양한 브랜드와 제품을 만나보며 선택의 즐거움을 느껴보세요.'
            ,'상품권으로 다양한 상품을 마음껏 고를 수 있는 기회입니다.'
            ,'상품권으로 특별한 선물을 줄 수 있어서 좋아요.'
            ,'상품권을 받아서 마음에 드는 상품을 고를 수 있어서 기뻐요.'
            ,'상품권으로 다양한 상품 중에서 마음에 드는 것을 찾아보세요.'
            ,'상품권을 사용해서 자유롭게 원하는 상품을 고를 수 있습니다.'
            ,'상품권으로 특별한 경험을 선물해볼 수 있는 좋은 기회입니다.'
            ,'상품권을 받아서 마음에 드는 상품을 마음껏 골라보세요.'
            ,'상품권을 이용해서 원하는 상품을 선택할 수 있어서 편리합니다.'
            ,'상품권으로 특별한 선물을 줄 수 있어서 좋은 선택입니다.'
            ,'상품권을 받으면 다양한 상품을 고를 수 있는 재미가 있어요.'
            ,'상품권을 사용해서 다양한 상품을 마음에 따라 선택할 수 있어요.'
            ,'상품권을 선물하면 상대방이 마음에 드는 상품을 고를 수 있어요.'
            ,'상품권으로 원하는 상품을 마음껏 골라보세요.'
            ,'다양한 브랜드와 제품을 만나볼 수 있어 좋아요.'
            ,'상품권으로 특별한 경험을 선물해줄 수 있습니다.'
            ,'상품 선택의 폭이 넓어서 좋았어요.'
            ,'다양한 쇼핑 재미를 경험할 수 있어요.'
            ,'특별한 경험을 선물해줄 수 있는 아이템.'
            ,'자유롭게 마음에 드는 상품을 골라보세요.'
            ,'다양한 카테고리의 상품들이 매력적이에요.'
            ,'상품권으로 마음에 드는 것을 골라보세요.'
            ,'원하는 대로 사용할 수 있는 최고의 선물.'
    ]
    _txt = ''
    _txt += lists[ random.randrange(0,len(lists)) ]+'\n'
    _txt += lists[ random.randrange(0,len(lists)) ]+'\n'
    _txt += lists[ random.randrange(0,len(lists)) ]+'\n'
    _txt += lists[ random.randrange(0,len(lists)) ]
    return _txt    


def setViewWrite(  ):
    global driver
    # 상품후기 페이지 이동
    try:
        tabs = driver.window_handles
        print('1',tabs)

        # 상품 후기 페이지 이동
        fnClick( '/html/body/div[2]/div[7]/div/div[2]/div[2]/div[2]/div/div[2]/ul/li[1]/div/div[3]/a')    

        tabs = driver.window_handles
        print('2',tabs)

        driver.switch_to.window( tabs[1] )        
        print('창 이동', driver.current_window_handle )       
                
        # 리뷰 쓰는 공간 클릭
        fnClick('/html/body/div[2]/div[1]/div[2]/div/form/fieldset/table/tbody/tr[2]/td/textarea')
        fnCopyNpaste( ranTxt() )
        
        driver.find_element(By.CSS_SELECTOR , "input[type='file']").send_keys('C:\\ncnc\\KakaoTalk_20230626_070450338.jpg') #파일 등록
        time.sleep(0.2)
        
        # 확인
        fnClick('/html/body/div[2]/div[1]/div[2]/div/form/fieldset/div/a[1]')        
        time.sleep(0.2)

        try:
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert        
            # 확인하기
            alert.accept()        
        except:
            print("no alert")   

        print('알람닫음?', driver.window_handles )  
        try:
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert        
            # 확인하기
            alert.accept()        
        except:
            print("no alert")   

        driver.close()
        driver.switch_to.window( tabs[0] )        
        print('마지막도 닫음', driver.window_handles )  
        print('창 이동', driver.current_window_handle )  
        fnClick('/html/body/div[2]/div[7]/div[1]/div[2]/div[2]/div[2]/div/div[1]/ul/li[1]/a/span')
        
        #time.sleep(5)
        '''
        tabs = driver.window_handles
        print('3',tabs)
        '''


        #time.sleep(0.3)
        #tabs = driver.window_handles
        #driver.switch_to.window( tabs[1] )
        #print(tabs)        
        #driver.switch_to.alert.accept()    # 자식 알림창 확인        
        #driver.close()        
        

    except Exception as e:
        print('fuck' , e)
    
    '''
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert        
        # 취소하기(닫기)
        alert.dismiss()        
        # 확인하기
        alert.accept()        
    except:
        print("no alert")
    '''
    
        

        
        

def fnLoging():
    '''로그인'''
    global driver
    __id = 'skfmtltmxm84'       #ycoplus1 #skfmtltmxm84
    __ps = '10tktkfkd84!'       #10tkfkdgo1! #10tktkfkd84!
    time.sleep(0.2)    
    

    fnClick( '/html/body/div[2]/div[8]/div/div/div/div[1]/form/fieldset/div[1]/div/input')    
    fnCopyNpaste( __id )
    

    fnClick( '/html/body/div[2]/div[8]/div/div/div/div[1]/form/fieldset/div[2]/div/input')    
    fnCopyNpaste( __ps )    

    fnClick( '/html/body/div[2]/div[8]/div/div/div/div[1]/form/p[2]')        
    time.sleep(0.5)
    driver.get('https://www.10x10.co.kr/my10x10/goodsUsing.asp')
    
    
    



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
    #setViewWrite()
    #time.sleep(0.5)
    #setViewWrite()
    #time.sleep(5)
    
    
    for i in range(0,370):
        print('횟수',i)
        setViewWrite()
        time.sleep(0.2)
    
    
    

    
