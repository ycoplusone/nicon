#from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.common.alert import Alert
#import pyautogui

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip #복사
import time

import lib.util as w2ji
import lib.dbcon as dbcon


'''
3.0.3 니콘 내콘 db 로딩 제외 local fold 만 접근 해서 처리 방식으로 변경.
3.0.2 니콘 내콘 수행 이력 텔러그램 발송 추가
3.0.1 니콘 내콘 데이터 수집및 판매기.
'''


class nicon():
    '''니콘 클래스'''
    __version   = '3.0.3'
    __comment   = '니콘 내콘 db 로딩 제외 local fold 만 접근 해서 처리 방식으로 변경.'   

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

    def fnDiv03( self , _str = '아이스커피S' , _flag = False ): # _str = '아메리카노 L'
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
                #print( '_ttt : ',_ttt,' / flag : ',flag )
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
                #print( f'{_str} : 매입보류' )
                _state = False
            else :
                #print( f'{_str} : 매입중' )
                self.fnClick( _ttt ) # 두번째 아이콘 클릭
                _state = True
            
            return _state
        except Exception as e:
            print('ERROR fnDiv03',e)
            if _flag :
                w2ji.send_telegram_message( f'******************** \n 상품명 : {_str} 를 찾을수 없습니다. \n ********************' )      
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
    _dbconn     = dbcon.DbConn() #db연결    
    _nicon      = nicon() #니콘 클래스 생성
    _check_time = w2ji.getNowDate()                   # 현재 시간
    _total_cnt  = 0         #총 실행수

    print('기본폴더 생성','-'*10)
    # 251216 제외 w2ji.base_fold_create( _dbconn ) #기초폴더 생성    
    w2ji.into_rename_barcode_v02()  # 251216 수정완 #파일명 바코드 명으로 변경작업 바코드 생성 못하면   None으로 치환된다.
    w2ji.init_fold_v02( _dbconn )   # 251216 수정완 폴더내 파일 정리.    
    __lists = w2ji.getFileCnt_v02( _dbconn ) # 251216 수정완 파일 잔여 개수 확인 후 텔레그램 발송

    _nicon.fnInit() #초기화    
    time.sleep(60)
    #_nicon.fnLoging() #매개변수 없음

    _nicon.fnDiv01( )  # 대분류 첫글짜 매개변수
    _nicon.fnDiv02( )   # 중분류명 매개변수
    _nicon.fnDiv03( )   # 상품명 매개변수	
    _nicon.fnClick( '//*[@id="warning-agree"]/label/div' ) # 동의 체크
    _nicon.fnRefresh() #브라이져 새로고침	    
    
    while(True): 
        try:
            _msg_sned_flag = w2ji.get1HourOver( _check_time )
            print('*'*80)
            print('시작 : ',w2ji.getNow() )

            for list in __lists:            
                # {'div_nm' : __category , 'brand':__brand , 'prod':__prod , 'fold_cnt':0 , 'fold_date':'99991231' , 'bal_qty':0 , 'suc_qty':0 , 'chk_qty':0}        
                div01_str   = list['div_nm']
                div02_str   = list['brand']
                div03_str   = list['prod']
                fold_nm     = f'{div01_str}_{div02_str}\\{div03_str}'
                cnt         = list['fold_cnt'] 

                prod_fold_list = w2ji.getfolelist( fold_nm ) # 상품 폴더 리스트의 하위 폴더 리스트 생성.
                _stat_flag = True
                for _fold_nm in prod_fold_list:

                    print('*'*80)
                    print( f'{fold_nm} 의 잔여 폴더수 [{cnt}] 입니다.' )
                    
                    if cnt <= 0 : #잔여 판매수가 0건이면 수행을 중단한다.
                        _stat_flag = False                            

                    _nicon.fnRefresh() #브라이져 새로고침
                    try:                        
                        if _stat_flag:
                            #print(f'1단계 : {div01_str}' )
                            _stat_flag = _nicon.fnDiv01( div01_str )   # 대분류 첫글짜 매개변수
                            time.sleep(0.5)
                        else:
                            break
                        
                        if _stat_flag:
                            #print(f'2단계 : {div02_str}' )
                            _stat_flag = _nicon.fnDiv02( div02_str )   # 중분류명 매개변수
                            time.sleep(0.5)
                        else:
                            break
                        
                        if _stat_flag:
                            #print(f'3단계 : {div03_str}' )
                            _stat_flag = _nicon.fnDiv03( div03_str , _msg_sned_flag )   # 상품명 매개변수
                            time.sleep(0.5)
                        else:
                            break
                        
                        if _stat_flag:
                            #print(f'4단계 : {_fold_nm}' )
                            files = w2ji.getFileList( _fold_nm ) #상품폴더내 파일 리스트 생성
                            _nicon.fnSale(fold_nm , _fold_nm, files , _dbconn ) # 판매
                            list['fold_cnt'] -= 1 #폴더 1건 처리
                            _temp_update = {'brand':div02_str , 'prod':div03_str , 'bal_qty':len(files) , 'sale_qty':len(files) }
                            _dbconn.update_nicon_sale_list(_temp_update) # 
                            
                        else:
                            break

                    except Exception as e:
                        print( '판매 작업중 오류',e )
            
            print('*'*80)
            print( w2ji.getNow() )                
            _total_cnt += 1
            if ( _msg_sned_flag ):    # 마지막 메세지 발송후 1시간 이상 되면 다시 텔레그램 메세지를 발송한다.
                _check_time = w2ji.getNowDate()         # 메세지 발송 시간을 다시 등록한다.
                w2ji.send_telegram_message(  f'NICON {_total_cnt}번재 실행중.' )      
            
            time.sleep(600) # 일회 순회 후 대기 시간
        except Exception as e:
            w2ji.send_telegram_message(  f'NICON 재시작해 주세요. \n {e}' )  
            quit()
            

