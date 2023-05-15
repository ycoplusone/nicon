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
        self.__conn = pymysql.connect(host = self.__url , user = self.__id , password = self.__ps , db= self.__db , charset= self.__charset )

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
            #query = query.format( **param )
            cur = self.__conn.cursor()            
            cur.execute( query )            
            __dblists = cur.fetchall()
            for i in __dblists:
                m_list = []
                s_list = []
                _strs = str( i[1].decode('utf-8') ).split('^')
                #print(_strs)
                for item in _strs:
                    s_list.append( item )
                
                m_list.append( i[0].decode('utf-8') )
                m_list.append( s_list )
                m_list.append( i[2].decode('utf-8') )
                _lists.append(m_list)            
            
            
            return _lists            
        except Exception as e:
            print( 'get_nicon error' , e )   


    
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
            " set last_date = now() "
            )            
            query = query.format( )                      
            cur.execute( query )
            self.__conn.commit()          
            
        except Exception as e:
            print( 'update_nicon_state error', e )
        finally:
            pass          

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
                m_list.append( i['category_id'].decode('utf-8') )
                m_list.append( i['category_nm'].decode('utf-8') )
                m_list.append( i['prod_nm'].decode('utf-8') )
                m_list.append( i['send_type'].decode('utf-8') )
                _lists.append(m_list)
            return _lists 
        
        
          
        except Exception as e:
            print( 'get_nicon error' , e )              

             