import pyautogui
import pyperclip
import os
import shutil
from datetime import datetime
import time
from PIL import ImageGrab , Image # pip install pillow



def abc():
    print('abc()')
    global a,b
    a += 1
    b += 12
    print('a',a)
    print('b',b)


def aa():
    print('a()')
    global a
    a += 1
    print('a',a)
    print('b',b)

def test():    
    print(datetime.today())
    __xy = pyautogui.locateOnScreen( './nicon/sale.png' )
    print(__xy)
    print(datetime.today())
    
def mk_image():
    '''캡쳐 만들기'''
    try:
        base_dttm = datetime.today().strftime('%Y%m%d_%H%M%S')
        img = ImageGrab.grab()
        imgCrop = img.crop()
        file_name = 'c:\\ncnc\\{}{}'.format(base_dttm,'.png')
        imgCrop.save(file_name)
    except Exception as e:
        print('mk_image : ',e)


if __name__ == "__main__":
    mk_image()
