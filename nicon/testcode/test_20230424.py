import lib.dbcon as dbcon 
import requests
dd = dbcon.DbConn()

__lists = [
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

__dblists = dd.get_nicon_job_detail( {'category_id': 62 } )


print('-'*50)
print(__dblists)
for list in __dblists:
    print( type(list[2]) )

def send_telegram_message( message ):
    url = 'https://api.telegram.org/bot6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc/sendMessage'
    data = {'chat_id': '-1001813504824', 'text': message}
    response = requests.post(url, data=data)
    print( response.json() )
        


send_telegram_message( '개별 임시태스트 입니다.' )
    
