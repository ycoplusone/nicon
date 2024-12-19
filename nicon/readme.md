# adb 관련 작업 
### pip install pure-python-adb

[1. adb 설치](https://developer.android.com/tools/releases/platform-tools?hl=ko#downloads)
[2. ppadb 설치](pip install pure-python-adb)
[3. windown 환경 등록]( adb 설치 폴더 , adb/adb.exe 둘다)
4. 테스트
adb start-server
adb kill-server

#### 접속방법
adb pair ipaddr:port

### 기기접속 목록 가져오기
adb devices

### 명령어 adb -s [기기접속 목록이름] shell input keyevent 27
#### 카메라켜기
    adb -s adb-R5CW91FH82E-pvncHX._adb-tls-connect._tcp shell input keyevent 27
    adb -s 192.168.137.94:5555 shell input keyevent 27


# 화면연결
scrcpy -s 192.168.137.94:5555


# 순서
1. [adb 파일 다운로드](https://developer.android.com/tools/releases/platform-tools?hl=ko#downloads)
2. 설치파일 path 잡기 adb.exe 까지 잡아야 한다.
3. adb tcpip 5555
4. adb devices
5. 휴대폰 무선디버그 모드에서  ip 확인후
6. "adb connect ip:5555" 으로 접속 connected 되는것을 확인
7. [scrcpy get the app 다운로드](https://github.com/Genymobile/scrcpy?tab=readme-ov-file)
8. 다운받은 scrcpy를 adb폴더의 하위 폴더에 생성한다.
9. "scrcpy -s ip:5555" 로 화면 링크 확인
