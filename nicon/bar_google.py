import barcode
from barcode.writer import ImageWriter
from PIL import Image , ImageFont , ImageDraw
'''바코드 이미지 생성'''

def mk_barcode_img(str):
    barcode_num = str
    file_path = 'c:\\ncnc\\'+barcode_num
    options = {"module_width":0.1, "module_height":7, "font_size": 3, "text_distance": 2, "quiet_zone": 1}
    #image_writer = ImageWriter().set_options(options)
    code128 = barcode.get_barcode_class('code128')
    my_ean = code128( barcode_num, writer=ImageWriter())
    file_nm = my_ean.save( file_path , options )
    return file_nm

def mk_img( code , ps , ex ):
    '''텍스트 추가하기'''
    pass_word = '비밀번호 : '+ps
    ex_date   = '유효기간 : '+ex    
    _path = 'c:\\ncnc\\'+code+'.png'
    #바코드 이미지 가져오기
    _barcode_img = Image.open( mk_barcode_img(code) ) 

    #
    _target_img = Image.open('./test_img/google_gift.png')
    _font = ImageFont.truetype('./test_img/PyeongChang-Regular.ttf', 12)
    out_img = ImageDraw.Draw( _target_img )
    #out_img.text(xy=(30,290), text=pass_word , font=_font , fill=(0,0,0) )
    out_img.text(xy=(30,280), text=ex_date   , font=_font , fill=(0,0,0) ) 
    #out_img = ImageDraw.Draw(_target_img)
    #_target_img.show()
    _target_img.paste( _barcode_img, (0,300) )
    _target_img.save( _path )

#mk_barcode_img('109688459860')

lists = [
['00NPBYJSVSMCPSTT','','2028년 07월 13일까지 등록']
,['D7P0RC6124RBN7F7','','2028년 07월 13일까지 등록']
,['0F4YHG3GKU31S1F9','','2028년 07월 13일까지 등록']
,['CSR6L7JF5A9Y0W5K','','2028년 07월 13일까지 등록']
,['GYFCHSKNM2AH905B','','2028년 07월 13일까지 등록']
,['4WMB012CF6KJZTNU','','2028년 07월 13일까지 등록']
,['DR7PKY7CRLE0NZN9','','2028년 07월 13일까지 등록']
,['DZU208F1D6BZ70F1','','2028년 07월 13일까지 등록']
,['CDX21U8GN1WJ1LWT','','2028년 07월 13일까지 등록']
,['J6K0ZPRHC5RXCUJ2','','2028년 07월 13일까지 등록']
,['7057C8G228SHCYXT','','2028년 07월 13일까지 등록']
,['FFZFFK6Y5ZA7EF02','','2028년 07월 13일까지 등록']
,['533ATDKD8THD3YD4','','2028년 07월 13일까지 등록']
,['90Y7U06X62NNT7XU','','2028년 07월 13일까지 등록']
,['98ZKCMBTLL4WNUGW','','2028년 07월 13일까지 등록']
,['D863T4RXSTH1TZHZ','','2028년 07월 13일까지 등록']
,['B1YKW3PYVRAMREJN','','2028년 07월 13일까지 등록']
,['9T6X7PP94ETAUM7X','','2028년 07월 13일까지 등록']
,['KP5CX1KGDYFJC3B0','','2028년 07월 13일까지 등록']
,['BP676228ZS0YVC8H','','2028년 07월 13일까지 등록']
,['CCF86C1HLD5YP5XG','','2028년 07월 13일까지 등록']
,['C98C9S9DMHFUSJJF','','2028년 07월 13일까지 등록']
,['FDTGCFMYVH3EH2A9','','2028년 07월 13일까지 등록']
,['3P212SK8861HFBZH','','2028년 07월 13일까지 등록']
,['75AGLEDZ5Z285TF6','','2028년 07월 13일까지 등록']
,['010VS7GPF6PX7MJ3','','2028년 07월 13일까지 등록']
,['GHVX2GKH3GUHCPSV','','2028년 07월 13일까지 등록']
,['B5JN7AMTPAJPL6UT','','2028년 07월 13일까지 등록']
,['8JSMYKHXN10NN16F','','2028년 07월 13일까지 등록']
,['JCNPU1ZPVP9N2TCH','','2028년 07월 13일까지 등록']
,['0DJ55F562CXU0G5P','','2028년 07월 13일까지 등록']
,['K111KJ6109T5RSTZ','','2028년 07월 13일까지 등록']
,['JHCSXG6MPX8U1XZC','','2028년 07월 13일까지 등록']    
]
print(len(lists))

for i in lists:
    #print(i[0],i[1],i[2])
    mk_img(i[0],i[1],i[2])
