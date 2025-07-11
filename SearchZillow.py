import requests
import re
from bs4 import BeautifulSoup
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
          'referer':'https://www.zillow.com/homes/Missoula,-MT_rb/'}

url = "https://www.zillow.com/menifee-ca/"
adr=[]
pr=[]
beds=[]
baths=[]
sqfoot=[]

#Get the number of pages
data =  requests.get(url, headers=header)
soup = BeautifulSoup(data.text, 'lxml')
#pageNum = str(soup.find('span', attrs={"class": "Text-c11n-8-102-0__sc-aiai24-0 dyzSyF"}))
#print(pageNum)
#pageNum = int(pageNum[-9:-7])

for i in range(1,7):
    resp =  requests.get(url+"{}_p/".format(i), headers=header)
    soup = BeautifulSoup(resp.text, 'lxml')

    address = soup.find_all('address', {'data-test':'property-card-addr'})
    price = soup.find_all('span', {'data-test':'property-card-price'})
    ids = soup.find_all('artical', {'data-test':'property-card'})
    for ultag in soup.find_all('ul', {'class': re.compile('^StyledPropertyCardHomeDetailsList*')}):
        for litag in ultag.find_all('li'):
            if "lot" in litag.text:
                beds.append('nan')
                baths.append('nan')
                sqfoot.append('nan')
            else:
                #print(litag.text)
                if "bds" in litag.text:
                    temp = int(litag.text[:-4].replace('-', '0'))
                    beds.append(temp)
                elif "bd" in litag.text:
                    temp = int(litag.text[:-3].replace('-', '0'))
                    beds.append(temp)
                elif "ba" in litag.text:
                    temp = int(litag.text[:-3].replace('-', '0'))
                    baths.append(temp)
                elif "sqft" in litag.text:
                    temp = litag.text[:-5].replace(',', '')
                    temp = int(temp.replace('-','0'))
                    sqfoot.append(temp)
                
    for result in address:
        adr.append(result.text)
    for result in price:
        pr.append(int(result.text[1:].replace(',', '').replace('+', '')))
    print(ids)

    #print(i)
    #print(len(baths))
    #print(len(sqfoot))
    #print(len(beds))
    #print(len(pr))
    

df = pd.DataFrame({'Beds':beds, 'Price' : pr, 'Baths' : baths, 'SqFoot' : sqfoot})
fig = px.scatter(df, x="Beds", y="Price", labels=dict(Beds="Number of Beds", Price="Listing price ($)"))
#fig.show()

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Price versus beds", "Price versus baths", "Price versus Sq Footage", "Beds versus sq footage"))

fig.append_trace(go.Scatter(
   x=pr,
   y=beds,
), row=1, col=1)

fig.append_trace(go.Scatter(
   x=pr,
   y=baths,
), row=2, col=1)

fig.append_trace(go.Scatter(
   x=pr,
   y=sqfoot
), row=1, col=2)

fig.append_trace(go.Scatter(
   x=beds,
   y=sqfoot
), row=2, col=2)

fig.update_layout(height=1080, width=1900, title_text="Subplots")
#fig.show()

#print(adr)
#print(pr)
#print(beds)

#print("Number of Pages found=" + str(pageNum))
