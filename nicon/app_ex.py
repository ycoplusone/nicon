import requests
from bs4 import BeautifulSoup

url = 'https://bank.shinhan.com/rib/easy/index.jsp#210501000000'
def app1():
    res = requests.get(url)
    

    
    if res.status_code == 200:
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        print( html )
    else : 
        print(res.status_code)
    


'''환율 관련'''



if __name__ == "__main__":    
    print('환율 시작')
    url = 'https://bank.shinhan.com/rib/easy/index.jsp#210501000000'
    app1()
    
