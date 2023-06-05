import lib.dbcon as dbcon
from datetime import datetime
import time
import requests

import lib.util as w2ji
import random

from pytz import timezone

def fn_history():
    datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    data = {  
              'authority' : 'api2.ncnc.app'
            , 'accept' : 'application/json, text/plain, */*'
            , 'accept-language' : 'ko,en;q=0.9'
            , 'authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjI1MzMwLCJ0eXBlcyI6Imtha2FvLHBob25lIiwiYmFua0lkIjo0LCJpYXQiOjE2ODE4NjQyNTEsImV4cCI6MTc0NDkzNjI1MX0.7FR1Taz1ukOZntopSAD3A3wp8YRDiokXkQWt1wyJ4E4'
            , 'origin': 'https://ncnc.app'
            , 'referer': 'https://ncnc.app/'
        }

    r_url = 'https://api2.ncnc.app/cons/confirmed?page={}'
    for i in range(1,12):
        url = r_url.format(i)
        print(url)
        response = requests.get(url , headers=data )
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
                dd.upsert_nicon_sale_info(param)

            
            


if __name__ == "__main__":
    #fn_history()
    
    #w2ji.mk_image()   

    # 0 이상 1 미만의 랜덤 실수 생성
    #random_float = random.randint(1,10)    
    #print(random_float)
    print( datetime.now(timezone('Asia/Seoul')) )
    print(     datetime.now(timezone('US/Hawaii')).strftime('%Y%m%d_%H%M%S') )
