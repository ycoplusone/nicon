import requests
from bs4 import BeautifulSoup
import json
import dbcon 
#import schedule
import time
from datetime import datetime
import requests
import json

import telegram
import asyncio


    
    

    

def getNicon():
    try:
        s_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        #print('s-time : ', datetime.today().strftime('%Y-%m-%d %H:%M:%S') )
        dd = dbcon.DbConn()
        # https://api2.ncnc.app/con-category2s?conCategory1Id=67&forSeller=1  카페
        # https://api2.ncnc.app/con-category2s?conCategory1Id=62&forSeller=1 편의점,마트
        # https://api2.ncnc.app/con-category2s?conCategory1Id=60&forSeller=1 빵,아이스크림
        # https://api2.ncnc.app/con-category2s?conCategory1Id=61&forSeller=1 피자,햄버거,치킨
        # https://api2.ncnc.app/con-category2s?conCategory1Id=65&forSeller=1 문화,게임,영화
        # https://api2.ncnc.app/con-category2s?conCategory1Id=129&forSeller=1 외식,분식
        # https://api2.ncnc.app/con-category2s?conCategory1Id=69&forSeller=1 백화점,주유,뷰티
        urls = [
            ['https://api2.ncnc.app/con-category2s?conCategory1Id=67&forSeller=1','카페']
            ,['https://api2.ncnc.app/con-category2s?conCategory1Id=62&forSeller=1','편의점,마트']
            ,['https://api2.ncnc.app/con-category2s?conCategory1Id=60&forSeller=1','빵,아이스크림']
            ,['https://api2.ncnc.app/con-category2s?conCategory1Id=61&forSeller=1','피자,햄버거,치킨']
            ,['https://api2.ncnc.app/con-category2s?conCategory1Id=65&forSeller=1','문화,게임,영화']
            ,['https://api2.ncnc.app/con-category2s?conCategory1Id=129&forSeller=1','외식,분식']
            ,['https://api2.ncnc.app/con-category2s?conCategory1Id=69&forSeller=1','백화점,주유,뷰티']
            ]

        for url in urls:
            url_addr = url[0]
            div_nm = url[1]            
            response = requests.get( url_addr )
            if response.status_code == 200:
                txt = response.json()
                lists = txt['conCategory2s']
                
                for list in lists:                    
                    param = {'category_id':list['id'] ,'category_nm' : list['name'] ,'div_nm': div_nm }
                    dd.insert_nicon_job(param)            
            else : 
                print(response.status_code)            
        
        '''
        url = 'https://api2.ncnc.app/con-items?forSeller=1&conCategory2Id='
        #print(category_id , category_nm)
        
        response = requests.get(url)
        
        if response.status_code == 200:
            txt = response.json()
            lists = txt['conCategory2s']        
        
        
        else : 
            print(response.status_code)
        '''
           
  
    
    except Exception as e:
        print( 'getNicon', e )
    finally:
        pass
    


#asyncio.set_event_loop_policy(asyncio.SelectorEventLoop())

#asyncio 정책을 유닉스 기반에서 윈도우 기반으로 변경한다.



if __name__ == "__main__":
    getNicon()
    



    
        
        