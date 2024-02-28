import requests
import bs4
import json
import lib.dbcon as dbcon 
import time
from datetime import datetime
    
def fn_history():
    datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    
    data_arr = [
        {   'authority' : 'api2.ncnc.app'
            , 'accept' : 'application/json, text/plain, */*'
            , 'accept-language' : 'ko,en;q=0.9'
            , 'authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjI1MzMwLCJ0eXBlcyI6Imtha2FvLHBob25lIiwiYmFua0lkIjo0LCJpYXQiOjE2ODE4NjQyNTEsImV4cCI6MTc0NDkzNjI1MX0.7FR1Taz1ukOZntopSAD3A3wp8YRDiokXkQWt1wyJ4E4'
            , 'origin': 'https://ncnc.app'
            , 'referer': 'https://ncnc.app/'
        }, # 원일 계정
        {    'authority' : 'api2.ncnc.app'
            , 'accept' : 'application/json, text/plain, */*'
            , 'accept-language' : 'ko,en;q=0.9'
            , 'authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjAwNjM3LCJ0eXBlcyI6Imtha2FvLG5hdmVyIiwiYmFua0lkIjo0LCJpYXQiOjE3MDkxMDAxMDksImV4cCI6MTc3MjE3MjEwOX0.1FXuAeUntYVUS59eUqgHRKU_1y3e2ZE0A16OCXJnSkU'
            , 'origin': 'https://ncnc.app'
            , 'referer': 'https://ncnc.app/'
        }  # 우정계정
        ]
    
    ''' 
    data = {  
              'authority' : 'api2.ncnc.app'
            , 'accept' : 'application/json, text/plain, */*'
            , 'accept-language' : 'ko,en;q=0.9'
            , 'authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjAwNjM3LCJ0eXBlcyI6Imtha2FvLG5hdmVyIiwiYmFua0lkIjo0LCJpYXQiOjE3MDkxMDAxMDksImV4cCI6MTc3MjE3MjEwOX0.1FXuAeUntYVUS59eUqgHRKU_1y3e2ZE0A16OCXJnSkU'
            , 'origin': 'https://ncnc.app'
            , 'referer': 'https://ncnc.app/'
        }   
    '''
    

    for j in data_arr:            
        r_url = 'https://api2.ncnc.app/cons/confirmed?page={}'
        for i in range(1,10):
            url = r_url.format(i)
            print(url)
            response = requests.get(url , headers= j )
            if response.status_code == 200:
                _json = response.json()
                _json_cons = _json['cons']
                dd = dbcon.DbConn()
                for _i in _json_cons:
                    _confirmExpireAt =  _i['confirmExpireAt'] if _i['confirmExpireAt'] != None else '1999-12-31T01:01:01.000Z'
                    _expireAt        =  _i['expireAt'] if _i['expireAt'] != None else '1999-12-31T01:01:01.000Z'
                    _createdAt       =  _i['createdAt'] if _i['createdAt'] != None else '1999-12-31T01:01:01.000Z'
                    
                    
                    param = {
                        'seq':_i['id']
                        , 'askingPrice' : _i['askingPrice']
                        , 'confirmExpireAt' : datetime.strptime( _confirmExpireAt , datetime_format)    
                        , 'expireAt'        : datetime.strptime( _expireAt        , datetime_format)
                        , 'createdAt'       : datetime.strptime( _createdAt       , datetime_format)
                        , 'rejectedReason' : _i['rejectedReason']
                        , 'lastCodeNumber' : _i['lastCodeNumber']
                        , 'currentStatus' : _i['currentStatus']
                    }
                    _conitem = _i['conItem']
                    
                    param['prod_id']  = _conitem['id']
                    param['prod_nm']  = _conitem['name']
                    _conCategory2 = _conitem['conCategory2']
                    param['div_id']  = _conCategory2['conCategory1Id']
                    param['category_id']  = _conCategory2['id']
                    param['category_nm']  = _conCategory2['name']  
                    print( param )          
                    dd.upsert_nicon_sale_info(param)
    
if __name__ == "__main__":    
    fn_history() #판매정보 가져오기
   
 
    




    
        
        