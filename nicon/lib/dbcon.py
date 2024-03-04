'''
Created on 2022. 7. 22.

@author: DLIVE
'''
import pymysql

class DbConn(object):
    '''
    '''
    __url = 'themoreschool.cafe24.com'
    __id = 'themoreschool'
    __ps = 'school2@'
    __db = 'themoreschool'    
    __charset = 'utf8'
    
    __conn = ''
    

    def __init__(self):
        '''        
        '''
        self.__conn = pymysql.connect(host = self.__url , user = self.__id , password = self.__ps , db= self.__db , charset= self.__charset  )

    def get_job_list(self):        
        try :
            _lists = []
            query = (
                " SELECT  "
                " category_id  "
                " , group_concat(prod_nm order by prod_nm separator '^' ) prod_nm  " 
                " , max( category_nm ) category_nm "
                " from nicon_job_list "
                " where upper(use_yn) = 'Y' "
                " group by category_id "
                " order by lpad(category_id,6,0) "    
            )
            
            cur = self.__conn.cursor( )                 
                
            cur.execute( query  )
            __dblists = cur.fetchall()
            
            print('get_job_list', len( __dblists ) )
            for i in __dblists:
                m_list = []
                s_list = []
                                
                _strs =  i[1].split('^')
                

                
                for item in _strs:
                    s_list.append( item )
                
                m_list.append( i[0] )
                m_list.append( s_list )
                m_list.append( i[2] )
                _lists.append(m_list)            
            
            
            return _lists            
        except Exception as e:
            print( 'get_job_list error' , e )   


    
    def get_prod_chg(self , param):        
        try :            
            query = (
                " select "
                " category_id , id , name , amount , refuse  , block , c_date " 
                " from nicon_info "
                " where 1=1"
                " and id = '{id}' "
                " and category_id = '{category_id}' "    
            )
            query = query.format( **param )
            cur = self.__conn.cursor()            
            cur.execute( query )            
            return cur.fetchall()            
        except Exception as e:
            print( 'get_nicon error' , e )        
    
    
    def get_nicon(self , param):        
        try :
            
            query = (
                " select "
                " case when amount = {amount} and refuse = '{refuse}' and block = '{block}' then 'T' else 'F' end chk " 
                " from nicon_info "
                " where 1=1 "
                " and id = '{id}' "
                " and category_id = '{category_id}' "    
            )
            query = query.format( **param )
            cur = self.__conn.cursor()            
            cur.execute( query )            
            return cur.fetchall()            
        except Exception as e:
            print( 'get_nicon error' , e )
            

    def insert_nicon(self , param ):
        '''get_nicon'''
        try :
            cur = self.__conn.cursor()
                        
            query_del = (
                " delete from nicon_info "
                " where category_id = '{category_id}' "
                " and id = '{id}' "
                )
            query = (
            " INSERT INTO nicon_info (category_id,id, name, amount, refuse, block, c_date)  "
            " VALUES('{category_id}', '{id}', '{name}', {amount}, '{refuse}', '{block}', now()) "
            )

            query_del = query_del.format( **param )
            cur.execute( query_del )
            self.__conn.commit()
            
            query = query.format( **param )                      
            cur.execute( query )
            self.__conn.commit()          
            
        except Exception as e:
            print( 'insert_nicon', e )
        finally:
            pass
                
   

    def update_nicon(self , param ):
        '''u_off_info insert'''
        try :
            cur = self.__conn.cursor()
                        
            query = (
            " update nicon_info  "
            " set name = '{name}' , amount ={amount} , refuse = '{refuse}' , block = '{block}' , c_date = now() "
            " where id = '{id}' "
            " and category_id = '{category_id}' "
            )            
            query = query.format( **param )                      
            cur.execute( query )
            self.__conn.commit()          
            
        except Exception as e:
            print( 'u_off_info error', e )
        finally:
            pass    
    
    def insert_nicon_job(self,param):
        '''insert_nicon_job'''
        try :
            cur = self.__conn.cursor()
                        
            query = (
            " INSERT INTO nicon_job_list (category_id, category_nm, prod_nm, use_yn, div_nm)  "
            " VALUES('{category_id}', '{category_nm}', '', 'N', '{div_nm}') "
            )

            query = query.format( **param )                      
            cur.execute( query )
            self.__conn.commit()          
            
        except Exception as e:
            print( 'insert_nicon_job', e )
        finally:
            pass        

    def update_nicon_state(self  ):
        '''update_nicon_state '''
        try :
            cur = self.__conn.cursor()
                        
            query = (
            " update nicon_state  "
            " set  "
            " pre_update_date = last_date"
            " , last_date = now() "
            )            
            query = query.format( )                      
            cur.execute( query )
            self.__conn.commit()          
            
        except Exception as e:
            print( 'update_nicon_state error', e )
        finally:
            pass  

    def getNiconState(self):       
        '''데이터 마지막 갱신 시간을 확인한다.''' 
        try :
            _lists = []
            query = (
                " select last_date from nicon_state  "
            )
            #query = query.format( **param )
            cur = self.__conn.cursor(  pymysql.cursors.DictCursor)            
            cur.execute( query )            

            __dblists =  cur.fetchall()    
            return (__dblists[0]['last_date']) 
            '''
            for i in __dblists:
                #print(i)
                m_list = []                
                m_list.append( i['last_date']

                _lists.append(m_list)
            return _lists 
            '''
        except Exception as e:
            print( 'getNiconState error' , e )  

    def getNiconStateRewindSec(self):       
        '''데이터 마지막 갱신 시간을 확인한다.''' 
        try :
            _lists = []
            query = (
                " select rewind_sec from nicon_state  "
            )
            #query = query.format( **param )
            cur = self.__conn.cursor(  pymysql.cursors.DictCursor)            
            cur.execute( query )            

            __dblists =  cur.fetchall()    
            return (__dblists[0]['rewind_sec']) 

        except Exception as e:
            print( 'getNiconStateRewindSec error' , e )

        

    def get_nicon_job_detail(self , param): 
              
        try :
            _lists = []
            query = (
                " SELECT   "
                " category_id , category_nm , prod_nm , upper(send_type) send_type "
                " from nicon_job_list  "
                " where upper(use_yn) = 'Y' " 
                " AND category_id = '{category_id}'     "            
            )
            query = query.format( **param )
            cur = self.__conn.cursor(  pymysql.cursors.DictCursor)            
            cur.execute( query )            
            __dblists =  cur.fetchall()          
            for i in __dblists:
                #print(i)
                m_list = []                
                m_list.append( i['category_id'] )
                m_list.append( i['category_nm'] )
                m_list.append( i['prod_nm'] )
                m_list.append( i['send_type'] )
                _lists.append(m_list)
            return _lists 
        
        
          
        except Exception as e:
            print( 'get_nicon error' , e )        

    def get_nicon_upload_list(self): 
              
        try :
            _lists = []
            query = (
                " select  "
                " SUBSTR(c.div_nm,1,1) div_nm "
                " , a.category_id "
                " , CONCAT(c.category_nm,'')  category_nm  "
                " , a.prod_nm  "
                " , concat(c.category_nm , '_' , a.prod_nm2 ) fold_nm "
                " , b.amount "
                " from ( "
                " 	SELECT " 
                " 	category_id  , prod_nm   "
                "   , replace(replace(replace(replace( replace( replace( replace( replace(prod_nm,'/','') ,':','') ,'*','') , '?','') ,'',''),'<',''),'>',''),'|','') prod_nm2 "
                " 	from nicon_job_list njl  "
                " 	where use_yn = 'Y' "
                " 	and send_type like '%V%' "
                " 	group by category_id  , prod_nm "
                " ) a "
                " join ( "
                " 	select "
                " 	category_id  , name prod_nm , amount   "
                " 	from nicon_info ni  "
                " 	where refuse = 0 "
                " ) b on (a.category_id = b.category_id and a.prod_nm = b.prod_nm)   "
                " join nicon_category_info c on ( a.category_id = c.category_id  ) "
                " order by  case when a.category_id  in (137, 180) then 0 else 99 end ,  3,6 desc "
            )
            #query = query.format( **param )
            cur = self.__conn.cursor(  pymysql.cursors.DictCursor)            
            cur.execute( query )            
            __dblists =  cur.fetchall()          
            for i in __dblists:                
                m_list = {}
                m_list['div_nm']        = i['div_nm']
                m_list['category_id']   = i['category_id']
                m_list['category_nm']   = i['category_nm']
                m_list['prod_nm']       = i['prod_nm']
                m_list['fold_nm']       = i['fold_nm']
                m_list['amount']        = i['amount']
                _lists.append(m_list)
            return _lists 
          
        except Exception as e:
            print( 'get_nicon error' , e )    


    def get_nicon_fold_list(self): 
              
        try :
            _lists = []
            query = (
                " select  "
                " SUBSTR(c.div_nm,1,1) div_nm "
                " , a.category_id "
                " , c.category_nm  "
                " , a.prod_nm  "
                " , concat(c.category_nm , '_' , a.prod_nm2 ) fold_nm "
                " from ( "
                " 	SELECT  "
                " 	category_id  , prod_nm   "
                "   , replace(replace(replace(replace( replace( replace( replace( replace(prod_nm,'/','') ,':','') ,'*','') , '?','') ,'',''),'<',''),'>',''),'|','') prod_nm2 "
                " 	from nicon_job_list njl  "
                " 	where use_yn = 'Y' "
                " 	and send_type like '%V%' "
                " 	group by category_id  , prod_nm "
                " ) a   "
                " join nicon_category_info c on ( a.category_id = c.category_id  ) "
                " order by 3,4 "
            )
            #query = query.format( **param )
            cur = self.__conn.cursor(  pymysql.cursors.DictCursor)            
            cur.execute( query )            
            __dblists =  cur.fetchall()          
            for i in __dblists:
                
                m_list = {}
                m_list['div_nm'] = i['div_nm']
                m_list['category_id'] = i['category_id']
                m_list['category_nm'] = i['category_nm']
                m_list['prod_nm'] = i['prod_nm']
                m_list['fold_nm'] = i['fold_nm']
                _lists.append(m_list)
            return _lists 
        
        
          
        except Exception as e:
            print( 'get_nicon error' , e )    


    def insert_nicon_barcode(self , param ):
        '''get_nicon'''
        try :
            cur = self.__conn.cursor()
                        
            query = (
            " INSERT INTO nicon_barcode_info(base_fold, prod_fold, file_nm, barcode, reg_date)  "
            " VALUES('{base_fold}', '{prod_fold}', '{file_nm}', '{barcode}', now()) "
            )
            query = query.format( **param )                      
            cur.execute( query )
            self.__conn.commit()
        except Exception as e:
            print( 'insert_nicon_barcode', e )
        finally:
            pass             


    def upsert_nicon_sale_info(self , param ):
        '''get_nicon'''
        try :
            cur = self.__conn.cursor()                        
            query = (
            " INSERT INTO nicon_sale_info (seq , prod_id   , prod_nm   , div_id   , category_id   , category_nm   ,askingPrice  , confirmExpireAt  ,expireAt  , createdAt  , rejectedReason    , lastCodeNumber    , currentStatus    , reg_date)  "
            "                      VALUES({seq},'{prod_id}','{prod_nm}','{div_id}','{category_id}','{category_nm}','{askingPrice}', '{confirmExpireAt}','{expireAt}', '{createdAt}', '{rejectedReason}', '{lastCodeNumber}', '{currentStatus}', now() ) "
            " on DUPLICATE key update askingPrice = '{askingPrice}' , reg_date = now()  "
            " , confirmExpireAt  =  '{confirmExpireAt}'  "
            " , expireAt		 = '{expireAt}'  "
            " , createdAt	 	 = '{createdAt}'  "
            " , lastCodeNumber = '{lastCodeNumber}'  "
            " , currentStatus	 = '{currentStatus}' "
            )
            query = query.format( **param )     
            #print(query)                 
            cur.execute( query )
            self.__conn.commit()
        except Exception as e:
            print( 'upsert_nicon_sale_info', e ,'\n',query ,'\n',param )
        finally:
            pass            

    def insert_nicon_client_log(self ):
        '''insert_nicon_client_log'''
        try :
            cur = self.__conn.cursor()                        
            query = (
            " insert nicon_client_log(reg_date , send_time) values( now() , now() )  "
            )
            #query = query.format( **param )                      
            cur.execute( query )
            self.__conn.commit()
        except Exception as e:
            print( 'insert_nicon_client_log', e )
        finally:
            pass     

    def update_nicon_client_log(self ,param ):
        '''update_nicon_client_log '''
        try :
            cur = self.__conn.cursor()                        

            query_del = (
                " delete from nicon_client_log where reg_date <= DATE_ADD(now(), INTERVAL -7 day) "
                )            
            query = (
                " update nicon_client_log "
                " set send_yn = 'Y' , send_time = now() "
                " where seq = {seq} "
            )
            cur.execute( query_del )
            self.__conn.commit()            

            query = query.format( **param )                      
            cur.execute( query )
            self.__conn.commit()          
            
        except Exception as e:
            print( 'update_nicon_client_log error', e )
        finally:
            pass    


    def get_nicon_client_log( self ):
        try :
            _lists = []
            query = (
                " SELECT  "
                " seq , reg_date , send_yn "
                " , case when TIMESTAMPDIFF(SECOND, reg_date, now() )>=300 then 'Y' else 'N' end diff_time "
                " , case when TIMESTAMPDIFF(SECOND, send_time, now()) >=3600 then 'Y' else 'N' end send_time "
                " from nicon_client_log  "
                " order by reg_date desc "
                " limit 1 "
            )
            #query = query.format( **param )
            cur = self.__conn.cursor(  pymysql.cursors.DictCursor)            
            cur.execute( query )            
            return cur.fetchall()         
        except Exception as e:
            print( 'get_nicon_client_log => ' , e )



    def get_ex_kind(self , param):               
        try :
            _lists = []
            query = (
                " SELECT CUR_ID ex_id, CUR_NM ex_nm, TO_CUR_ID to_ex, MIN_AMT min, MAX_AMT max, STEP step, correction_amt  "
                " FROM exchange_kind "
                " WHERE EX_USE like '{ex_use}' "
                " order by sort , cur_id "
            )
            query = query.format( **param )
            cur = self.__conn.cursor(  pymysql.cursors.DictCursor)            
            cur.execute( query )            
            return cur.fetchall()         
        except Exception as e:
            print( 'get_ex_kind => ' , e )



    def upsert_ex_info(self , param ):
        ''' 환율 업데이트 '''
        try :
            cur = self.__conn.cursor()                        
            query = (
                " INSERT INTO exchange_rate_other_currency (BASE_DT, CUR_ID, CUR_NM, TO_CUR_ID,INPUT_DT, RATE,U_DATE,c_date) "
                " VALUES('{BASE_DT}', '{CUR_ID}', '{CUR_NM}', '{TO_CUR_ID}','{INPUT_DT}', '{RATE}', now(), now() ) "
                " on DUPLICATE key update INPUT_DT='{INPUT_DT}' , RATE='{RATE}' , PRE_RATE=RATE , PRE_U_DATE=U_DATE, u_date = now() "
            )
            query = query.format( **param )     
            
            cur.execute( query )
            self.__conn.commit()
        except Exception as e:
            print( 'upsert_ex_info', e ,'\n',query ,'\n',param )
        finally:
            pass                     

    def get_ex_info(self , param):               
        try :
            _lists = []
            query = (
                " select a.BASE_DT , a.CUR_ID , a.CUR_NM , a.RATE , a.INPUT_DT  , b.amt BANK_FIX_RATE "
                " from exchange_rate_other_currency a "
                " join exchange_shinhan_info b on (a.base_dt = b.base_dt ) "
                " where a.BASE_DT = ( select max(base_dt) from exchange_shinhan_info ) "
                " AND a.CUR_ID = '{CUR_ID}' "
            )
            query = query.format( **param )
            #cur = self.__conn.cursor()            
            cur = self.__conn.cursor(  pymysql.cursors.DictCursor)            
            cur.execute( query )            
            return cur.fetchall()         
        except Exception as e:
            print( 'get_ex_info => ' , e )

    def upsert_ex_info2(self , param ):
        ''' 환율 업데이트 '''
        try :
            cur = self.__conn.cursor()                        
            query = (
                " INSERT INTO exchange_info (BASE_DT, CUR_ID , KIND , QTY, AMT, ACC, u_date, c_date)  "
                " VALUES('{BASE_DT}', '{CUR_ID}', '{kind}', {QTY}, {AMT},{ACC}, now(), now() ) "
                " on DUPLICATE key update QTY='{QTY}' , AMT='{AMT}' , ACC={ACC} , u_date = now() "
            )
            query = query.format( **param )
            cur.execute( query )
            self.__conn.commit()
        except Exception as e:
            print( 'upsert_ex_info2', e ,'\n',query ,'\n',param )
        finally:
            pass                     

    def upsert_shini_info(self , param ):
        ''' 신한 업데이트 '''
        try :
            cur = self.__conn.cursor()                        
            query = (
                " INSERT INTO exchange_shinhan_info (BASE_DT, AMT, u_date, c_date)  "
                " VALUES('{BASE_DT}', {AMT}, now(), now()) "
                " on DUPLICATE key update amt= {AMT} , u_date = now() "
            )
            query = query.format( **param )
            cur.execute( query )
            self.__conn.commit()
        except Exception as e:
            print( 'upsert_shini_info', e ,'\n',query ,'\n',param )
        finally:
            pass      


    def upsert_soldout_info(self , param ):
        '''  '''
        try :
            cur = self.__conn.cursor()                        
            query = (
                " INSERT INTO nicon_soldout_info (prod_nm, stats, reg_date)  "
                " VALUES('{prod_nm}', '{stats}', now())  "
                " on DUPLICATE key update stats='{stats}' ,  reg_date = now()  "
            )
            query = query.format( **param )
            cur.execute( query )
            self.__conn.commit()
        except Exception as e:
            print( 'upsert_soldout_info => ', e ,'\n',query ,'\n',param )
        finally:
            pass           

    def get_soldout_info(self , param):               
        try :
            _lists = []
            query = (
                " select prod_nm , stats  "
                " from nicon_soldout_info a "
                " where 1=1 "                
                " AND a.prod_nm = '{prod_nm}' "
            )
            query = query.format( **param )
            cur = self.__conn.cursor(  pymysql.cursors.DictCursor)            
            cur.execute( query )            
            return cur.fetchall()         
        except Exception as e:
            print( 'get_ex_info => ' , e )