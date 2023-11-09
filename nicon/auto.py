import psutil
import time
import os




def main():
    ''''''
    try:
        while(True):
            _ret = False
            for pid in psutil.pids():
                p = psutil.Process(pid)
                if 'chromedriver.exe' == p.name():
                    _ret = True
            if _ret:
                print('실행중')
            else:
                print('정지중')
                os.system("python C:\\Users\\DLIVE\\eclipse-workspace\\nicon\\autonicon2.py")
            time.sleep(60)
            
    except Exception as e:
        print('auto == ' , e)



if __name__ == "__main__":
    main()

    