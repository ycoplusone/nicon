from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

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
3.0.1 니콘 내콘 데이터 수집및 판매기.
'''


class nicon():
    '''니콘 클래스'''
    __version   = '3.0.1'
    __comment  = '니콘 내콘 데이터 수집및 판매기.'   

    # 변수 시작 ****************************************************
    __driver = None # 크롬 드라이버
    # 변수 종료 ****************************************************
    def __init__(self):
        ''' init '''
        print('*'*50)
        print( f'VERSION : {self.__version} \t COMMENT : {self.__comment}' )
        print('*'*50)


    def fnText(self , str):
        _rt = ''
        try:        
            time.sleep(0.3)
            _html = WebDriverWait(self.__driver, 5).until(EC.element_to_be_clickable((By.XPATH, str )))
            return _html.text
        except Exception as e:
            return _rt

    def fnText_1(self , str):
        _rt = ''
        try:        
            time.sleep(0.01)
            _html = WebDriverWait(self.__driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, str )))
            return _html.text
        except Exception as e:
            return _rt

    def fnClick(self , str):
        time.sleep(0.15)
        WebDriverWait(self.__driver, 5).until(EC.element_to_be_clickable((By.XPATH, str ))).click()
    

    def fnCopyNpaste( self, _str ):
        time.sleep(0.2)
        pyperclip.copy( _str )
        ActionChains(self.__driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    

    def fnEnter(self):
        '''엔터입력'''   
        try:      
            ActionChains(self.__driver).send_keys(Keys.ENTER)
        except Exception as e:
            print('fnEnter error : ',e)  

    def fnReadAlert(self):
        _rt = '문구없음'
        try:
            alert_present = WebDriverWait(self.__driver, 10).until(EC.alert_is_present())
            if alert_present :
                result = self.__driver.switch_to.alert
                _rt = result.text                
                return _rt
        except Exception as e:
            print( 'alert error', e )
            return _rt



    def fnLoging(self):
        '''로그인'''        
        __id = 'skfmtltm1052'
        __ps = 'Natktkfkd84!'    
        time.sleep(0.2)
        self.fnClick('//*[@id="app"]/div/div[2]/div/section/section/nav/section/button')
        
        self.fnClick('//*[@id="app"]/div/div[2]/div/div/div/section/div[4]/a/span')

        self.fnClick('/html/body/div[1]/div/div[2]/div/div/div/button[1]/div') #네이버 클릭    
        time.sleep(0.5)
        
        tabs = self.__driver.window_handles
        print(tabs)
        self.__driver.switch_to.window( tabs[1] )        
        print('창 이동', self.__driver.current_window_handle )     

        #fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[2]/div[1]/input') #id    
        self.fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[1]/input') #id    
        self.fnCopyNpaste( __id )   
        #fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[2]/div[2]/input') #ps
        self.fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[2]/input') #ps    
        self.fnCopyNpaste( __ps )    
        #fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[8]/button/span') #확인
        #self.fnClick('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[7]/button') #확인
        self.fnClick('//*[@id="log.login.text"]')
        time.sleep(30)
        
        self.__driver.switch_to.window( tabs[0] )           
        print('창 이동', self.__driver.current_window_handle )       
        time.sleep(2)
        self.__driver.get('https://ncnc.app/sell/wait-confirmed')  
        time.sleep(1)

    def fnDiv01( self , str = '카' ): #str = '카'
        '''대분류 찾기'''
        _state = False    
        try:
            self.fnClick( '//*[@id="app"]/div/div[2]/div/section/div/section/section[1]/div/button')    
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

            self.fnClick(_div01)
            time.sleep(0.15)
            _state = True
            return _state
        except Exception as e:
            print('ERROR fnDiv01',e)
            return _state

    def fnDiv02( self , _str = '커피빈' ): # _str = '투썸플레이스'
        '''중분류 찾기(카테고리 찾기)'''    
        _state = False
        try:
            self.fnClick( '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/div[2]/input') # 검색바 클릭
            self.fnCopyNpaste( _str )
            self.fnClick( '//*[@id="items-container"]/a[2]') #두번째 아이콘 클릭
            time.sleep(0.15)
            _state = True
            return _state
        except Exception as e:
            print('ERROR fnDiv02',e)
            return _state

    def fnDiv03( self , _str = '아이스커피S' ): # _str = '아메리카노 L'
        '''하분류 찾기(상품 차지)'''
        _state = False
        item_name  = '//*[@id="items-container"]/a[2]'
        item_state = '/html/body/div[1]/div/div[2]/div/section/div/div/div/section/div[3]/a[2]/div[2]'
        item_seq = 2        
        flag = True
        _ttt = ''
        try:
            self.fnClick( '//*[@id="app"]/div/div[2]/div/section/div/div/div/section/div[2]/input') #검색바 클릭
            self.fnCopyNpaste( _str )    
            
            while( flag ):            
                _ttt       = "/html/body/div[1]/div/div[2]/div/section/div/div/div/section/div[3]/a[{}]/div[1]/div[1]".format(item_seq)
                item_state = "/html/body/div[1]/div/div[2]/div/section/div/div/div/section/div[3]/a[{}]/div[2]".format(item_seq)
                print( '_ttt : ',_ttt,' / flag : ',flag )
                # 상품 리스트 가져오기
                titles = WebDriverWait( self.__driver, 1).until(EC.presence_of_all_elements_located((By.XPATH, _ttt )))
                #복수개(3개)의 앨리먼트가 추출 됨 (3개중 마지막)
                for title in titles:
                    #print(' ==> ',title.tag_name ,' / ' , title.text,' / ' , title.get_attribute('xpath'))
                    #print( title.text == _str )
                    if title.text == _str:
                        flag = False
                        break
                item_seq += 1            

            _sale_type = self.fnText( item_state ) #상품판매상태 확인
            print( f'상품명 : {_str} \t 상태 : {_sale_type}' )
            #print('_sale_type : ', _sale_type )
            #print('item_name  : ', item_name  )
            #print('item_state : ', item_state )        

            if (_sale_type == '매입보류') or (_sale_type=='') :
                #w2ji.send_telegram_message( _str+' : '+ '매입보류' )
                print( f'{_str} : 매입보류' )
                _state = False
            else :
                print( f'{_str} : 매입중' )
                self.fnClick( _ttt ) # 두번째 아이콘 클릭
                _state = True
            
            return _state
        except Exception as e:
            print('ERROR fnDiv03',e)
            return _state

    def fnSale( self , _nm = '' , _fold_nm = '' , _files = [] , _dbconn = None ):
        '''판매 '''
        try:
            for file in _files:
                self.__driver.find_element(By.CSS_SELECTOR , "input[type='file']").send_keys(file) #파일 등록
            
            time.sleep(1)            
            self.fnClick('//*[@id="app"]/div/div[2]/div/section/div/div/div/section/button') # 판매 등록        
            time.sleep(1)    
            alert_txt = self.fnReadAlert() # 알림창 읽기
            
            if '쿠폰이 등록' in alert_txt :
                telegram_str = '정상 : '+alert_txt+'\n\n'
                telegram_str += _nm +'\n\n'
                telegram_str += '원본 : '+ _fold_nm +'\n\n'
                telegram_str += '완료 : '+ w2ji.complete_fold(_fold_nm , True)
                w2ji.send_telegram_message(  telegram_str )
                w2ji.mk_image() # 스샷 생성
            else:
                telegram_str = '이상 : '+alert_txt+'\n\n'
                telegram_str += _nm +'\n\n'
                telegram_str += '원본 : '+ _fold_nm +'\n\n'
                telegram_str += '완료 : '+ w2ji.complete_fold(_fold_nm , False)
                w2ji.send_telegram_message(  telegram_str )
            
            _dbconn.update_nicon_job_list_2( {'qty': len(_files) , 'path' : _nm} ) # 처리 한 상품의 건수를 조절한다.

            time.sleep(0.15)
            self.fnRefresh() #드라이버 초기화
        except Exception as e:
            print('fnSale',e)

    def fnInit(self):
        '''크룸 초기화'''
        options = ChromeOptions() #webdriver.ChromeOptions()
        #options.add_argument('headless')
        #options.add_argument('window-size=1024x768')    
        #        
        self.__driver = webdriver.Chrome( options=options) # http://chromedriver.chromium.org/ 다운로드 크롬 버젼 확인해야함.
        self.__driver.get('https://ncnc.app/sell/wait-confirmed')
        self.__driver.implicitly_wait(10)  
        time.sleep(1)  
        return self.__driver
    
    def fnRefresh(self):
        '''refresh'''
        self.__driver.refresh()

if __name__ == "__main__":   
    ''''''    
    _lastupdate = '' # 업데이트 시간 저장
    _dbconn     = dbcon.DbConn() #db연결    
    _nicon      = nicon() #니콘 클래스 생성

    print('기본폴더 생성','-'*10)
    w2ji.base_fold_create( _dbconn ) #기초폴더 생성    
    w2ji.into_rename_barcode() #파일명 바코드 명으로 변경작업 바코드 생성 못하면   None으로 치환된다.
    w2ji.init_fold( _dbconn ) #폴더내 파일 정리.
    w2ji.getFileCnt( _dbconn ) #파일 잔여 개수 확인 후 텔레그램 발송    


    _nicon.fnInit() #초기화    
    time.sleep(1)
    _nicon.fnLoging() #매개변수 없음
    _nicon.fnDiv01( )  # 대분류 첫글짜 매개변수
    _nicon.fnDiv02( )   # 중분류명 매개변수
    _nicon.fnDiv03( )   # 상품명 매개변수	
    _nicon.fnClick( '//*[@id="warning-agree"]/label/div' ) # 동의 체크
    _nicon.fnRefresh() #브라이져 새로고침	    
    
    while(True): 
        try:           
            _tmp = _dbconn.getNiconState()                           
            _lastupdate = _tmp
            __lists    = _dbconn.get_nicon_upload_list() # 판매 상품 갯수가 있는 상품을 전체 순회 한다. 판매중 판매보류 여부 상관 없다.
            print('시작 : ',w2ji.getNow() , '\t 상품 갯수 : ', len( __lists ))                
            _dbconn.insert_nicon_client_log() #로그 등록

            for list in __lists:                    
                div01_str = list['div_nm']
                div02_str = list['category_nm']
                div03_str = list['prod_nm']
                fold_nm   = list['fold_nm']
                amt       = str( list['amount'] )
                #qty       = str( list['qty'] )

                prod_fold_list = w2ji.getfolelist( fold_nm ) # 상품 폴더 리스트의 하위 폴더 리스트 생성.
                _stat_flag = True
                for _fold_nm in prod_fold_list:
                    
                    cnt = _dbconn.select_nicon_job_list( { 'path':fold_nm} )[0]['qty'] # 현재 상품 잔여 건수

                    print( f'{fold_nm} 의 잔여 상품수가 {cnt}입니다.' )
                    
                    if cnt <= 0 : #잔여 판매수가 0건이면 수행을 중단한다.
                        _stat_flag = False                            

                    _nicon.fnRefresh() #브라이져 새로고침
                    try:
                        
                        if _stat_flag:
                            print(f'1단계 : {div01_str}' )
                            _stat_flag = _nicon.fnDiv01( div01_str )   # 대분류 첫글짜 매개변수
                            time.sleep(0.5)
                        else:
                            break
                        
                        if _stat_flag:
                            print(f'2단계 : {div02_str}' )
                            _stat_flag = _nicon.fnDiv02( div02_str )   # 중분류명 매개변수
                            time.sleep(0.5)
                        else:
                            break
                        
                        if _stat_flag:
                            print(f'3단계 : {div03_str}' )
                            _stat_flag = _nicon.fnDiv03( div03_str )   # 상품명 매개변수
                            time.sleep(0.5)
                        else:
                            break
                        
                        if _stat_flag:
                            print(f'4단계 : {_fold_nm}' )
                            files = w2ji.getFileList( _fold_nm ) #상품폴더내 파일 리스트 생성
                            _nicon.fnSale(fold_nm , _fold_nm, files , _dbconn ) # 판매                                    
                        else:
                            break

                    except Exception as e:
                        print( '판매 작업중 오류',e )
            
            time.sleep(60) # 일회 순회 후 대기 시간
        except Exception as e:
            print('error : ' , e)
            w2ji.send_telegram_message(  'NICON 재시작해 주세요.......... ' )  
            quit()
            

