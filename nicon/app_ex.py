import requests
#from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import json
import math
import time
import numpy as np

import lib.dbcon as dbcon 


def get_ex_list(): #환율코드정보
    '''환율코드 리스트 정보'''
    _ex_kinds = [    
     #{'ex_id':'USD','ex_nm':'미국' ,'to_ex':'KRW'              ,'min':1,'max':20,'step':0.01}
    {'ex_id':'EUR','ex_nm':'유로' ,'to_ex':'USD'               ,'min':1,'max':20,'step':0.01}
    ,{'ex_id':'JPY','ex_nm':'일본 엔' ,'to_ex':'USD'          ,'min':500,'max':2500,'step':1}
    ,{'ex_id':'GBP','ex_nm':'영국 파운드' ,'to_ex':'USD'      ,'min':1,'max':20,'step':0.01}
    ,{'ex_id':'AUD','ex_nm':'호주 달러' ,'to_ex':'USD'        ,'min':3,'max':30,'step':0.01}
    ,{'ex_id':'CAD','ex_nm':'캐나다 달러'  ,'to_ex':'USD'     ,'min':3,'max':30,'step':0.01}
    ,{'ex_id':'CHF','ex_nm':'스위스 프랑' ,'to_ex':'USD'      ,'min':1,'max':20,'step':0.01}
    ,{'ex_id':'CNY','ex_nm':'중국 위안 인민폐','to_ex':'USD'   ,'min':10,'max':200,'step':0.01}
    ,{'ex_id':'AED','ex_nm':'UAE 디르함'  ,'to_ex':'USD'      ,'min':1,'max':100,'step':0.01}
    ,{'ex_id':'ARS','ex_nm':'아르헨티나 페소' ,'to_ex':'USD'   ,'min':2500,'max':20000,'step':1}
    ,{'ex_id':'BDT','ex_nm':'방글라데시 타카' ,'to_ex':'USD'   ,'min':250,'max':2000,'step':0.01}
    ,{'ex_id':'BRL','ex_nm':'브라질 레알'  ,'to_ex':'USD'     ,'min':10,'max':100,'step':0.01}
    ,{'ex_id':'CLP','ex_nm':'칠레 페소' ,'to_ex':'USD'        ,'min':2000,'max':17000,'step':1}
    ,{'ex_id':'CZK','ex_nm':'체코 코루나'  ,'to_ex':'USD'     ,'min':50,'max':400,'step':0.01}
    ,{'ex_id':'DKK','ex_nm':'덴마크 크로네' ,'to_ex':'USD'    ,'min':15,'max':150,'step':0.01}
    ,{'ex_id':'EGP','ex_nm':'이집트 파운드'  ,'to_ex':'USD'   ,'min':60,'max':600,'step':0.01}
    ,{'ex_id':'HKD','ex_nm':'홍콩 달러'  ,'to_ex':'USD'       ,'min':15,'max':150,'step':0.01}
    ,{'ex_id':'HUF','ex_nm':'헝가리 포린트'  ,'to_ex':'USD'   ,'min':700,'max':7000,'step':1}
    ,{'ex_id':'IDR','ex_nm':'인도네시아 루피아' ,'to_ex':'USD' ,'min':30000,'max':200000,'step':1}
    ,{'ex_id':'INR','ex_nm':'인도 루피'  ,'to_ex':'USD'       ,'min':150,'max':1500,'step':0.01}
    ,{'ex_id':'KRW','ex_nm':'대한민국 원'   ,'to_ex':'USD'    ,'min':5000,'max':20000,'step':1}
    ,{'ex_id':'LKR','ex_nm':'스리랑카 루피' ,'to_ex':'USD'    ,'min':700,'max':6000,'step':1}
    ,{'ex_id':'MOP','ex_nm':'마카오 파타카' ,'to_ex':'USD'    ,'min':15,'max':150,'step':0.01}
    ,{'ex_id':'MXN','ex_nm':'멕시코 페소'  ,'to_ex':'USD'     ,'min':30,'max':330,'step':0.01}
    ,{'ex_id':'MYR','ex_nm':'말레이시아 링깃'  ,'to_ex':'USD'  ,'min':10,'max':100,'step':0.01}
    ,{'ex_id':'NGN','ex_nm':'나이지리아 나이라' ,'to_ex':'USD' ,'min':2000,'max':15000,'step':1}
    ,{'ex_id':'NOK','ex_nm':'노르웨이 크로네' ,'to_ex':'USD'   ,'min':20,'max':200,'step':0.01}
    ,{'ex_id':'NPR','ex_nm':'네팔 루피'     ,'to_ex':'USD'    ,'min':300,'max':2800,'step':1}
    ,{'ex_id':'NZD','ex_nm':'뉴질랜드 달러'  ,'to_ex':'USD'    ,'min':1,'max':30,'step':0.01}
    ,{'ex_id':'PEN','ex_nm':'페루 누에보솔'  ,'to_ex':'USD'   ,'min':5,'max':75,'step':0.01}
    ,{'ex_id':'PHP','ex_nm':'필리핀 페소'    ,'to_ex':'USD'   ,'min':100,'max':1500,'step':0.01}
    ,{'ex_id':'PLN','ex_nm':'폴란드어 뉴즐로티','to_ex':'USD' ,'min':7,'max':75,'step':0.01}
    ,{'ex_id':'RON','ex_nm':'루마니아어 레이' ,'to_ex':'USD'  ,'min':10,'max':100,'step':0.01}
    ,{'ex_id':'RUB','ex_nm':'러시아 루블'    ,'to_ex':'USD'   ,'min':200,'max':2000,'step':0.01}
    ,{'ex_id':'SAR','ex_nm':'사우디 리얄'   ,'to_ex':'USD'    ,'min':6,'max':75,'step':0.01}
    ,{'ex_id':'SEK','ex_nm':'스웨덴 크로나'  ,'to_ex':'USD'   ,'min':25,'max':200,'step':0.01}
    ,{'ex_id':'SGD','ex_nm':'싱가포르 달러'  ,'to_ex':'USD'   ,'min':2,'max':25,'step':0.01}
    ,{'ex_id':'THB','ex_nm':'태국 바트'    ,'to_ex':'USD'     ,'min':75,'max':750,'step':0.01}
    ,{'ex_id':'TRY','ex_nm':'터키 리라'     ,'to_ex':'USD'    ,'min':75,'max':600,'step':0.01}
    ,{'ex_id':'TWD','ex_nm':'신대만 달러'   ,'to_ex':'USD'    ,'min':60,'max':600,'step':0.01}
    ,{'ex_id':'UAH','ex_nm':'우크라이나 흐리브냐','to_ex':'USD','min':85,'max':750,'step':0.01}
    ,{'ex_id':'UYU','ex_nm':'우루과이 페소'  ,'to_ex':'USD'   ,'min':80,'max':750,'step':0.01}
    ,{'ex_id':'VND','ex_nm':'베트남 동'    ,'to_ex':'USD'     ,'min':40000,'max':400000,'step':1}
    ]
    return _ex_kinds



def get_usd_curreny():

    # db 객체
    dd = dbcon.DbConn()    
    korea_timezone = timezone('Asia/Seoul')
    # now = datetime.now(korea_timezone)

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
    _ex_kind     = get_ex_list()   

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
    _min = _param['min']
    _max = _param['max']
    _step = _param['step']
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
        
        for i in _amt_tot:
            dd.upsert_ex_info2( i )
        
        
        #return _amt_tot   
    
    





if __name__ == "__main__":    
    print('환율 시작')
    get_usd_curreny()
    '''
    visa()

    aa = get_ex_list()
    aa.append( {'ex_id':'USD','ex_nm':'미국' ,'to_ex':'KRW'              ,'min':1,'max':30,'step':0.01} )
    
    for i in aa:
        start = time.time()
        math.factorial(100000)
        #print( i ,'='*50)
        cal_rating(  i  )
        end = time.time()
        print(f"{end - start:.5f} sec")
    '''
