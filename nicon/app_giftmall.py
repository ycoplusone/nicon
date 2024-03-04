import requests
import bs4
from datetime import datetime
from pytz import timezone
import time
import schedule

import lib.dbcon as dbcon 
def send_telegram_message2( message ):

    token = '6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc' 
    chats = ['-1002107720688','-1002078550724','-1002143408779']    
    '''
    알람 bargin -1002107720688
    알람 sale -1002078550724
    알람 show -1002143408779
    '''
    base_dttm = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        
    try: 

        for chat in chats:
            url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
            data = {'chat_id': chat , 'text': base_dttm+'\n'+message , 'parse_mode':'HTML' ,'disable_web_page_preview': True }
            response = requests.post(url, data=data)
            time.sleep(1)            

    except Exception as e:
        print( 'telegram_send', e )
    finally:
        pass

def shoptaiwan():
    dbdb = dbcon.DbConn()   
    param = {}
    url = 'https://shoptaiwan.com.tw/products/korea-album-luminous-horizons-booknlife-of-south-korea-world'
    with requests.session() as ses:
        res = ses.get( url )
        if res.status_code == 200:
            soup = bs4.BeautifulSoup(res.text.encode('utf-8') , 'html.parser' )
            tags = soup.find_all('div', class_='price price--large price--sold-out price--show-badge')
            if len(tags)>=1:
                param = {'prod_nm':'shoptaiwan','stats':'매진'}
            else:
                param = {'prod_nm':'shoptaiwan','stats':'판매'}
                
            chk = dbdb.get_soldout_info({'prod_nm':'shoptaiwan'})[0]

            txt =''
            if param['stats'] == '판매':
                txt = url+'\n'+'shoptaiwan'+' : 판매상태('+param['stats']+')'
            else :
                txt = 'shoptaiwan'+' : 판매상태('+param['stats']+')'

            if chk['stats'] != param['stats']:
                dbdb.upsert_soldout_info( param )
                send_telegram_message2( txt )
                print( param )

            

def happymbook():
    dbdb = dbcon.DbConn()   
    param = {}
    url = 'https://happymbook.com/products/korea-birthday-gift-item-happy-tshirts'
    with requests.session() as ses:
        res = ses.get( url )
        if res.status_code == 200:
            soup = bs4.BeautifulSoup(res.text.encode('utf-8') , 'html.parser' )
            tags = soup.find_all('div', class_='price price--large price--sold-out price--show-badge')
            if len(tags)>=1:
                param = {'prod_nm':'happymbook','stats':'매진'}
            else:
                param = {'prod_nm':'happymbook','stats':'판매'}
                
            chk = dbdb.get_soldout_info({'prod_nm':'happymbook'})[0]

            txt =''
            if param['stats'] == '판매':
                txt = url+'\n'+'happymbook'+' : 판매상태('+param['stats']+')'
            else :
                txt = 'happymbook'+' : 판매상태('+param['stats']+')'

            if chk['stats'] != param['stats']:
                dbdb.upsert_soldout_info( param )
                send_telegram_message2( txt )
                print( param )

   
def marahuyobox():
    dbdb = dbcon.DbConn()   
    param = {}    
    login_info = {
        'password' : 'maravip',
        'form_type':'storefront_password' ,
        'utf8' : '✓',
    }    
    url = 'https://marahuyobox.com/products/manila-history-bookn' 
    with requests.session() as ses:        
        loging_req = ses.post( 'https://marahuyobox.com/password' , data = login_info )
        
        if loging_req.status_code == 200:
            res = ses.get( url )            
            if res.status_code == 200:
                soup = bs4.BeautifulSoup(res.text.encode('utf-8') , 'html.parser' )
                tags = soup.find_all('div', class_='price price--large price--sold-out price--show-badge')
                if len(tags)>=1:
                    param = {'prod_nm':'marahuyobox','stats':'매진'}
                else:
                    param = {'prod_nm':'marahuyobox','stats':'판매'}
                    
            chk = dbdb.get_soldout_info({'prod_nm':'marahuyobox'})[0]

            txt =''
            if param['stats'] == '판매':
                txt = url+'\n'+'marahuyobox'+' : 판매상태('+param['stats']+')'
            else :
                txt = 'marahuyobox'+' : 판매상태('+param['stats']+')'

            if chk['stats'] != param['stats']:
                dbdb.upsert_soldout_info( param )
                send_telegram_message2( txt )
                print( param )

def treerun():
    # 시작 시간 기록
    start_time = time.time()
    shoptaiwan()     
    happymbook()
    marahuyobox()    
    # 종료 시간 기록
    end_time = time.time()
    # 소요된 시간 계산
    elapsed_time = end_time - start_time
    print( datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S') ,"소요된 시간:", elapsed_time, "초")


if __name__ == '__main__':   
    treerun()
    
    schedule.clear()
    schedule.every( 60 ).seconds.do( treerun )  

    while True:
        schedule.run_pending()
        time.sleep(1)    
    


