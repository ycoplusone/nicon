'''
RPA 작업
pip install pyautogui
pip install opencv-python
'''
import pyautogui
import pyperclip
import os
import shutil
from datetime import datetime
import time

import dbcon


# 현재 사용하는 모니터의 해상도 출력
print(pyautogui.size())

# 현재 마우스 커서의 위치 출력
print(pyautogui.position())

# 
#pyautogui.mouseInfo()


# 절대 좌표로 이동
#pyautogui.moveTo(100, 100)                 # 100, 100 위치로 즉시 이동
#pyautogui.moveTo(500, 500, duration=0.5)   # 200, 200 위치로 0.5초간 이동

# 상대 좌표로 이동
#pyautogui.move(100, 100, duration=1)    # 현재 위치 기준으로 100, 100만큼 1초간 이동
#pyautogui.moveTo(100, 100, duration=0.5)   # 200, 200 위치로 0.5초간 이동


#pyautogui.click(200, 200)

#pyautogui.click(x=200,y=200 , clicks=2 , interval=0.5 , button='left')

#pyautogui.click(500, 500)
#pyautogui.write('Hello world!', interval=0.2)
#pyautogui.write(['H', 'e', 'l', 'l', 'o'], interval=0.2)

# 캐쳐이미지로 좌표 찾기

def getXyinfo( obj ):
    ''' Box(left=802, top=139, width=80, height=82) 값 받아서 x , y 좌표 리턴 '''
    x = obj.left + (obj.width / 2 )
    y = obj.top + (obj.height /2)
    return {'x' : x , 'y' : y}

def getImg( str ):
    if str == '카':
        return './nicon/1.png'
    elif str == '편':
        return './nicon/2.png'
    elif str == '빵':
        return './nicon/3.png'
    elif str == '피':
        return './nicon/4.png'
    elif str == '문':
        return './nicon/5.png'
    elif str == '외':
        return './nicon/6.png'    
    elif str == '백':
        return './nicon/7.png'    

def getfolelist(str):
    base = 'c:\\ncnc'
    path_str = base+'\\'+str
    __list = os.listdir( path_str )
    temp_list = [ X for X in __list if os.path.isdir(path_str+'\\'+X)]
    list = [ path_str+'\\'+X for X in temp_list if X[-4:-1] != '(완료']
    return list

def complete_fold(path):
    '''해당 path 의 이름 변경'''
    os.rename( path , path+'(완료)')

#test_img = pyautogui.locateOnScreen('./nicon/1.png') 
#print( getXyinfo(test_img)['x'] )



def fn_main():
    dd = dbcon.DbConn()    
    base_sleep = 3
    area_xy = {}
    sale_xy = {}
    search_xy = {}
    nobrand_xy = {}
    noitem_xy  = {}
    additem_xy = {}
    exploer_xy = {}
    ok_xy = {}
    __lists = dd.get_nicon_upload_list()



    for list in __lists:
        print('시작.')
        print(list)
        prod_fold_list = getfolelist( list['fold_nm'] )
        
        for __i in prod_fold_list:
            pyautogui.click(100, 150)
            pyautogui.press('f5')
            time.sleep(base_sleep-1)

            if len(area_xy) == 0:
                print('area_xy 설정')
                area_xy = pyautogui.locateOnScreen('./nicon/area.png')             


            if len(sale_xy) == 0:
                print('sale_xy 설정')
                sale_img = pyautogui.locateOnScreen('./nicon/sale.png') 
                sale_xy  = getXyinfo(sale_img)
            print(area_xy , sale_xy)

            pyautogui.click(  sale_xy['x'], sale_xy['y'])
            time.sleep(base_sleep-1)

            div_img = pyautogui.locateOnScreen( getImg(list['div_nm'] )  )
            div_xy  = getXyinfo(div_img)
            pyautogui.click(  div_xy['x'], div_xy['y'])
            time.sleep(base_sleep-1)

            if len(search_xy) == 0:
                print('search_xy 설정')
                search_img = pyautogui.locateOnScreen('./nicon/search.png')
                search_xy  = getXyinfo(search_img)
                print('search_xy : ',search_xy)  
            
            pyautogui.click(  search_xy['x'], search_xy['y'])
            time.sleep(base_sleep-1)
            pyperclip.copy(list['category_nm'])
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            time.sleep(base_sleep-2)

            if len(nobrand_xy) == 0:
                print('nobrand_xy 설정')
                nobrand_img = pyautogui.locateOnScreen('./nicon/nobrand.png')
                nobrand_xy  = getXyinfo(nobrand_img)
                print('nobrand_xy : ',nobrand_xy)  
            
            pyautogui.click(  nobrand_xy['x']+140, nobrand_xy['y'])
            time.sleep(base_sleep-1)

            pyautogui.click(  search_xy['x'], search_xy['y'])
            pyperclip.copy(list['prod_nm'])
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            time.sleep(base_sleep-2)

            if len(noitem_xy) == 0:
                print('noitem_xy 설정')
                noitem_img = pyautogui.locateOnScreen('./nicon/noitem.png')
                noitem_xy  = getXyinfo(noitem_img)
                print('noitem_xy : ',noitem_xy)  
            pyautogui.click(  noitem_xy['x'], noitem_xy['y']+120)
            time.sleep(base_sleep-1)

            if len(additem_xy) == 0:
                print('additem_xy 설정')
                additem_img = pyautogui.locateOnScreen('./nicon/additem.png')             
                additem_xy  = getXyinfo(additem_img)
                print('additem_xy : ',additem_xy)  
            pyautogui.click(  additem_xy['x'], additem_xy['y'])
            time.sleep(base_sleep-1)
            
            if len(exploer_xy) == 0:
                print('exploer_xy 설정')
                exploer_img = pyautogui.locateOnScreen('./nicon/exploer.png')             
                exploer_xy  = getXyinfo(exploer_img)
                print('exploer_xy : ',exploer_xy)  
            pyautogui.click(  exploer_xy['x']+60, exploer_xy['y'])
            time.sleep(base_sleep-1)       
            path_copy = __i
            pyperclip.copy( path_copy )
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            time.sleep(base_sleep-1)

            pyautogui.click(  exploer_xy['x']+60, exploer_xy['y']-40)
            time.sleep(base_sleep-2)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(base_sleep-2)
            pyautogui.hotkey('alt', 'o')
            time.sleep(base_sleep-2)
            if len(ok_xy) == 0:
                print('ok_xy 설정')
                ok_img = pyautogui.locateOnScreen('./nicon/ok.png')             
                ok_xy  = getXyinfo(ok_img)
                print('ok_xy : ',ok_xy) 
            pyautogui.click(  ok_xy['x'], ok_xy['y'])
            time.sleep(base_sleep-1)
            pyautogui.press('enter')
            time.sleep(base_sleep-2)
            complete_fold(path_copy)

        


    

