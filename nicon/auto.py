import psutil
import time
import os




def main():
    ''''''
    try:
        while(True):
            _ret = False
            _cnt = 0
            for pid in psutil.pids():
                p = psutil.Process(pid)
                #if 'chromedriver.exe' == p.name():
                #    _ret = True
                if 'python' in p.name():
                    print(p)
                    _cnt += 1
            if _cnt >=2 :
                print('실행중','*'*100)
            else:
                print('정지중')
                os.system("python C:\\Users\\DLIVE\\eclipse-workspace\\nicon\\autonicon2.py")
            time.sleep(20)
            
    except Exception as e:
        print('auto == ' , e)



if __name__ == "__main__":
    main()

    