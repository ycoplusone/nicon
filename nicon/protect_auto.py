import subprocess
import time

def start_process():
    # 실행할 프로세스 명령어
    command = ["python", "c://Users//DLIVE//eclipse-workspace//nicon//autonicon2.py"]
    
    # 프로세스 시작
    process = subprocess.Popen(command)
    return process

def main():
    while True:
        process = start_process()
        
        # 프로세스가 종료될 때까지 대기
        while process.poll() is None:
            time.sleep(1)
        
        # 프로세스가 종료되면 로그를 남기고 재시작
        print("Process exited with code:", process.poll())
        process = None
        time.sleep(5)  # 재시작 전 잠시 대기

if __name__ == "__main__":
    main()