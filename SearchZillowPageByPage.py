import requests
from bs4 import BeautifulSoup

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
          'referer':'https://www.zillow.com/homes/Missoula,-MT_rb/'}

adr=[]
pr=[]
sl=[]

for i in range(0,2):
    resp =  requests.get("https://www.zillow.com/menifee-ca/".format(i), headers=header)
    soup = BeautifulSoup(resp.text, 'lxml')

    address = soup.find_all('address', {'data-test':'property-card-addr'})
    price = soup.find_all('span', {'data-test':'property-card-price'})
    seller =soup.find_all('div', {'class':'cWiizR'})
    
    for result in address:
        adr.append(result.text)
    for result in price:
        pr.append(result.text)
    for results in seller:
        sl.append(result.text)

print(adr)
print(pr)
print(sl)

#print(data.url)


