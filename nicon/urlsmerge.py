import cv2
import os

def main( path , file_nm):
    # 이미지 파일 로드
    image = cv2.imread( path )
 
    cv2.line(image, (0,469), (512,469), (255,255,255), thickness=30, lineType=cv2.LINE_AA)

    # 추출할 영역 좌표 설정
    x = 0
    y = 82
    width = 512
    height = 600




    # 이미지에서 영역 추출
    cropped_image = image[y:y+height, x:x+width]

    # 추출된 영역 이미지 저장
    cv2.imwrite('C:\\ncnc_class\\sim_back\\'+file_nm, cropped_image)

def getFileList( _path ):    
    __list = os.listdir( _path )    
    list = [ _path+'\\'+X for X in __list ]
    return list

_path = 'C:\\ncnc_class\\sim'

for i in getFileList(_path):
    print(i , i.split('\\')[-1] )
    #main('C:\\ncnc_class\\test20240208\\000_FQYSUBIJJW.png','000_FQYSUBIJJW.png')
    main( i , i.split('\\')[-1])
    
    