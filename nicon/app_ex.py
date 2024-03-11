import requests
#from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import json
import math
import time
import numpy as np
import schedule

import lib.dbcon as dbcon 


def get_ex_list( ex_use ): #환율코드정보
    '''환율코드 리스트 정보'''
    dd = dbcon.DbConn()    
    _ex_kinds = dd.get_ex_kind( {'ex_use': ex_use })
    return _ex_kinds



def get_usd_curreny():
    '''신한 은행 송금 환율 정보 가져오기'''    
    dd = dbcon.DbConn()    # db 객체
    korea_timezone = timezone('Asia/Seoul')
    dt = datetime.today()
    st = dt.astimezone(korea_timezone)
    today = st.strftime('%Y%m%d')
    data = {"dataBody":{"ricInptRootInfo":{"serviceType":"GU","serviceCode":"F3730","nextServiceCode":"","pkcs7Data":"","signCode":"","signData":"","useSign":"","useCert":"","permitMultiTransaction":"","keepTransactionSession":"","skipErrorMsg":"","mode":"","language":"ko","exe2e":"","hideProcess":"","clearTarget":"","callBack":"shbObj.fncF3730Callback","exceptionCallback":"","requestMessage":"","responseMessage":"","serviceOption":"","pcLog":"","preInqForMulti":"","makesum":"","removeIndex":"","redirectUrl":"","preInqKey":"","_multi_transfer_":"","_multi_transfer_count_":"","_multi_transfer_amt_":"","userCallback":"","menuCode":"","certtype":"","fromMulti":"","fromMultiIdx":"","isRule":"N","webUri":"/index.jsp","gubun":"","tmpField2":""},"조회구분":"","조회일자":today,"고시회차":1,"조회일자_display":"","startPoint":"","endPoint":""},"dataHeader":{"trxCd":"RSHRC0213A01","language":"ko","subChannel":"49","channelGbn":"D0"}}
    url = 'https://bank.shinhan.com/serviceEndpoint/httpDigital'
    try:
        res = requests.post(url, data=json.dumps(data))
        currency_exchanges = res.json()['dataBody']['R_RIBF3730_1']
        _aaa = {'BASE_DT': today ,'CODE': currency_exchanges[0]['통화CODE'], 'AMT': currency_exchanges[0]['전신환매도환율']}        
        dd.upsert_shini_info(_aaa)
    except Exception as e:
        print('get_usd_curreny',e)



def visa():
    # db 객체
    dd = dbcon.DbConn()    

    # 현재시간
    _today      = datetime.now(timezone('Asia/Seoul')) #.strftime('%Y-%m-%d')
    _today_f    = _today.strftime('%m')+'%2F'+_today.strftime('%d')+'%2F'+_today.strftime('%Y')    
    _today_ymd  = _today.strftime('%Y%m%d')
    
    # 환율리스트 
    _ex_kind     = get_ex_list('Y')   

    # 브라우저 정보 넣기
    headers = {
            'Referer': 'www.visakorea.com',
            #'User-Agent':'Mozilla/5.0 (Windows NT 11.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.130 Safari/537.36 NetHelper70'
    }
    
    
    for i in _ex_kind:
        _ex     = i['ex_id']
        _to_ex     = i['to_ex']
        url     = f'https://www.visakorea.com/cmsapi/fx/rates?amount=1&fee=0&utcConvertedDate={_today_f}&exchangedate={_today_f}&fromCurr={_to_ex}&toCurr={_ex}'
        print(url)
        
        try: 
            res = requests.get(url , headers=headers)    
            if res.status_code == 200:
                _txt = res.json()
                _tmp = { 'BASE_DT'      : _today_ymd 
                        , 'CUR_ID'      : i['ex_id']
                        , 'CUR_NM'      : i['ex_nm']
                        , 'TO_CUR_ID'   : _txt['conversionFromCurrency']
                        , 'RATE'        : _txt['fxRateWithAdditionalFee']
                        , 'INPUT_DT'    : _txt['conversionInputDate']
                        }                
                dd.upsert_ex_info(_tmp)
            else : 
                print(res.status_code)        
        except Exception as e:
            print('except', e )
    
    _aaa = { 'BASE_DT'      : _today_ymd 
                , 'CUR_ID'      : 'USD'
                , 'CUR_NM'      : '미국(달러)'
                , 'TO_CUR_ID'   : 'USD'
                , 'RATE'        : 1
                , 'INPUT_DT'    : _today_ymd
                }   
    dd.upsert_ex_info(_aaa)             
        
def cal_rating( _param ):
    '''환율 계산'''   
    try:
        _min = float( _param['min'] )
        _max = float( _param['max'] )
        _step = float( _param['step'] )
        _correction_amt = float( _param['correction_amt'] )
        # db 객체
        dd = dbcon.DbConn()    

        # 환율정보
        _data = dd.get_ex_info( {'CUR_ID':_param['ex_id']} )    
        
        if len( _data ) != 0:   
            _ex_info = _data[0]  
        
            _rate           = float( _ex_info['RATE'] )             #환율
            _bank_rate      = float( _ex_info['BANK_FIX_RATE'] )    #고시환율1차    
            _glo_brand_fee  = 0.011                     #국제브랜드수수료
            _for_sv_fee     = 0.0018                    #해외서비스수수료

            def rounddown(num):
                #내림
                return math.floor( num * 100) / 100
            
            _lists = []
            for i in list(np.arange( _min , _max , _step )):
                _amt = round(i,2) #수량
                _aa1 = math.trunc( rounddown( round( _amt * _rate,2 ) * (1+_glo_brand_fee) ) * _bank_rate  )
                _aa2 = math.trunc( _aa1 * _for_sv_fee )   
                _aa3 = _aa1 + _aa2
                _aa4 = round(( _aa3 % 1000) * 2 / _aa3 ,4) if _aa3 != 0  else 0 
                _tmp = { 'BASE_DT': _ex_info['BASE_DT'],'CUR_ID': _ex_info['CUR_ID'] , 'QTY':_amt , 'AMT':_aa3 , 'ACC': _aa4}
                _lists.append( _tmp )

            _amt_05 = {}
            _amt_06 = {}
            _amt_07 = {}
            _amt_08 = {}
            _amt_09 = {}
            _amt_10 = {}
            _amt_11 = {}
            _amt_12 = {}
            _amt_13 = {}
            _amt_14 = {}
            _amt_15 = {}
            _amt_16 = {}
            _amt_17 = {}
            _amt_tot = []
            
            for _list in _lists:
                if _list['AMT'] <= 5999:
                    _amt_05 = _list
                    _amt_05['kind'] = '5999'
                elif _list['AMT'] <= 6999:
                    _amt_06 = _list
                    _amt_06['kind'] = '6999'
                elif _list['AMT'] <= 7999:
                    _amt_07 = _list
                    _amt_07['kind'] = '7999'
                elif _list['AMT'] <= 8999:
                    _amt_08 = _list
                    _amt_08['kind'] = '8999'
                elif _list['AMT'] <= 9999:
                    _amt_09 = _list
                    _amt_09['kind'] = '9999'
                elif _list['AMT'] <= 10999:
                    _amt_10 = _list
                    _amt_10['kind'] = '10999'
                elif _list['AMT'] <= 11999:
                    _amt_11 = _list
                    _amt_11['kind'] = '11999'
                elif _list['AMT'] <= 12999:
                    _amt_12 = _list
                    _amt_12['kind'] = '12999'
                elif _list['AMT'] <= 13999:
                    _amt_13 = _list
                    _amt_13['kind'] = '13999'
                elif _list['AMT'] <= 14999:
                    _amt_14 = _list
                    _amt_14['kind'] = '14999'
                elif _list['AMT'] <= 15999:
                    _amt_15 = _list
                    _amt_15['kind'] = '15999'
                elif _list['AMT'] <= 16999:
                    _amt_16 = _list
                    _amt_16['kind'] = '16999'
                elif _list['AMT'] <= 17999:
                    _amt_17 = _list
                    _amt_17['kind'] = '17999'

            _amt_tot.append( _amt_05 )
            _amt_tot.append( _amt_06 )
            _amt_tot.append( _amt_07 )
            _amt_tot.append( _amt_08 )
            _amt_tot.append( _amt_09 )
            _amt_tot.append( _amt_10 )
            _amt_tot.append( _amt_11 )
            _amt_tot.append( _amt_12 )
            _amt_tot.append( _amt_13 )
            _amt_tot.append( _amt_14 )
            _amt_tot.append( _amt_15 )
            _amt_tot.append( _amt_16 )
            _amt_tot.append( _amt_17 )
            
            
            # 보정 데이터 찾기
            _amt_tot2 = []
            for i in _amt_tot:
                #print( i  , _correction_amt)
                _chk_amt = round(i['QTY'] + _correction_amt ,2)
                for _list in _lists:
                    if _list['QTY'] == _chk_amt:
                        _tmp = _list
                        _tmp['kind'] = i['kind']
                        _amt_tot2.append(  _tmp )
            
            
            # 기록 하는 부분
            for i in _amt_tot2:
                dd.upsert_ex_info2( i )
    except Exception as e:
        print( 'error : ' , _param , ' / ',e )
    
    
def get_ex_data():
    '''환율 가져오기'''
    start = time.time()    
    get_usd_curreny()       # 신한 송금 환율 정보 가져오기
    visa()
    
    _ex_list = get_ex_list('%')
        
    for i in _ex_list:
        cal_rating(  i  )
    
    end = time.time()
    print(f"환율 소요시간 : {end - start:.5f} sec")
    




if __name__ == "__main__":    
    print('환율 시작')
    
    get_ex_data()    

    #schedule.every(30).minutes.do( get_ex_data )    
    
    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)
    