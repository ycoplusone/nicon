import requests
#from bs4 import BeautifulSoup
import json
import dbcon 
#import schedule
import time
from datetime import datetime
#import requests
import json
    
    

'''
"id":1114,"name":"싱글레귤러 아이스크림","askingPrice":2950,"isRefuse":1,"isBlock":0
askingPrice :매입가격 
isRefuse : 0 매입중 , 1 매입대기
isBlock : 0 매입가능 , 1 매입불가

bot 접속 현황 
https://api.telegram.org/bot6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc/getUpdates
METHOD_NAME

메세지 테스트
https://api.telegram.org/bot6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc/sendMessage?chat_id=-1001813504824&text=forgetme1

'''
def send_telegram_message( message ,send_type ):
    token = '6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc' 
    chats = ['-1001932446119','-1001839221120','-1001906908142']    
    '''
    -1001932446119 : 니콘내콘 알림
    -1001839221120 : 더모아방
    -1001906908142 : themore
    
    -1001813504824 : 우정이 개인방 SEND_TYPE V , VE 일경우 이쪽으로 보낸다.
    '''
    base_dttm = datetime.today().strftime('%Y-%m-%d %H:%M')
        
    try: 
        if 'V' in send_type: #우정이 전용방
            url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
            data = {'chat_id': '-1001813504824', 'text': base_dttm+'\n'+message}
            response = requests.post(url, data=data)
            time.sleep(1)
            print( 'with V : ' , response.json() )
        
        if 'E' in send_type:       
            for chat in chats:
                url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
                data = {'chat_id': chat , 'text': base_dttm+'\n'+message}
                response = requests.post(url, data=data)
                time.sleep(1)
                print( 'without V : ',response.json() )
    except Exception as e:
        print( 'telegram_send', e )
    finally:
        pass
    
        
    

def getNicon():
    try:
        s_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        #print('s-time : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )
        dd = dbcon.DbConn()    
        dd.update_nicon_state();
        
        __lists = dd.get_job_list()
        
        '''__lists = [
                  #['137' , ['싱글레귤러 아이스크림'] ,'베라' ] 
                  ['64'  , ['1만원권'] ,'커피빈' ]  
                , ['70'  , ['1만원권','로얄밀크티쉐이크(R)','떠먹는 스트로베리 초콜릿 생크림'] ,'투썸'] 
                , ['332' , ['(ICE)아메리카노','샤인머스캣그린주스','레드오렌지자몽주스'] ,'메가MGC커피']            
                , ['61'  , ['2만원권'] ,'CU'] 
                , ['62'  , ['2만원권','2천원권','3천원권','매일)어메이징오트언스위트190ml'] ,'GS25']   
                , ['67'  , ['1만원권'] ,'세븐일레븐']
                , ['55'  , ['1만원권 (일시사용)','2만원권 (일시사용)'] ,'뚜레쥬르']
                , ['58'  , ['1만원권 (일시사용)','딸기 마블 쉬폰'] ,'파리바게뜨']
                , ['77'  , ['먼치킨 10개팩'] ,'던킨도너츠']
                , ['446' , ['돌체 콜드브루 라떼(ONLY ICE) M'] ,'매머드익스프레스']
                , ['256' , ['싸이버거 세트'] ,'맘스터치']
                , ['180' , ['빅맥 세트','1만원권','디지털상품권 1만원권'] ,'맥도날드']
                , ['421' , ['3만원권'] ,'써브웨이']
                , ['142' , ['2인 영화관람권(평일/주말)','영화관람권(평일/주말)'] ,'메가박스']
                , ['162' , ['영화관람권(평일/주말)'] ,'CGV']
                , ['510' , ['투머치 베이컨 버거세트'] ,'노브랜드버거(NBB)']
                , ['65' , ['소금버터스콘 + 봄 말차크림 오트라떼(R)'] ,'이디야']
                , ['56' , ['와퍼주니어+콜라R'] ,'버거킹']
        ]
        '''
           
        for ii in __lists:
            category_id = ii[0] #카테고리 id
            category_nm = ii[2] #카테리고리명
            __details = dd.get_nicon_job_detail( {'category_id':category_id } )         # 검증 세부 레스트
            url = 'https://api2.ncnc.app/con-items?forSeller=1&conCategory2Id='+category_id
            #print(category_id , category_nm)
            
            
            
            response = requests.get(url)
            
            if response.status_code == 200:
                txt = response.json()
                lists = txt['conItems']
                
                for list in lists:
    
                    for detail in __details: # 상품명 리스트  
                        #print(str ,str in name , name )        
                        if ( detail[2] == list['name'].strip() ):
                                  
                            id = list['id']
                            name = list['name'].strip()
                            amount = list['askingPrice']
                            refuse = list['isRefuse']
                            block  = list['isBlock']
                            param = {'category_id':category_id ,'category_nm' : category_nm ,'id': id , 'name':name , 'amount': amount , 'refuse' : refuse , 'block': block }
                            
                            res = dd.get_prod_chg(param)
                            #print(param)
                            #print(len(res))
                            sent_text = ''
                            sent_text += category_nm+' / '+name+'\n'
                            sent_text += "가격 : {}".format(amount)+'\n'
                            sent_text += '매입 : '+( '매입중' if refuse == 0 else '매입보류')
                            #print(sent_text)
                            if len(res) == 0: # 신규일경우
                                dd.insert_nicon(param)
                                print('신규 : ',param)
                                #asyncio.run( telegram_send(sent_text , detail[3] ) )
                                send_telegram_message(sent_text , detail[3] )
    
                            else : #기존 상품일경우
                                result = dd.get_nicon( param )
    
                                if result[0][0] == b'F':
                                    dd.update_nicon(param)
                                    print('변경 : ',param)                                    
                                    #asyncio.run( telegram_send(sent_text, detail[3] ) )
                                    send_telegram_message(sent_text , detail[3] )
                                    
            else : 
                print(response.status_code)
            
        e_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print('start / end time : {} ~ {}'.format(s_time , e_time) )    
    
    except Exception as e:
        print( 'getNicon', e )
    finally:
        pass
    


#asyncio.set_event_loop_policy(asyncio.SelectorEventLoop())

#asyncio 정책을 유닉스 기반에서 윈도우 기반으로 변경한다.



if __name__ == "__main__":
    
    while True:
        #schedule.run_pending()
        getNicon()
        time.sleep(40)    
#schedule.every(1).minutes.do(getNicon)


    
        
        