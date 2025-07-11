import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
from datetime import date

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
          'referer':'https://www.zillow.com/homes/Missoula,-MT_rb/'}

url = "https://www.zillow.com/menifee-ca/"
adr=[]
zid=[]
pr=[]
beds=[]
baths=[]
sqfoot=[]

#Connect to SQL DB
db_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "seppiesrealestate"
)
print("Database connected!")

#Get the number of pages
data =  requests.get(url, headers=header)
soup = BeautifulSoup(data.text, 'lxml')

#Open page by page
for i in range(1,15):
    resp =  requests.get(url+"{}_p/".format(i), headers=header)
    soup = BeautifulSoup(resp.text, 'lxml')

    #Find all property cards
    cards = soup.find_all('article', {'data-test':'property-card'})
    for tag in cards:
        #get zillow id
        zid = tag['id'][5:]
        #get addvertised price
        price = tag.find('span', {'data-test':'property-card-price'}).text[1:].replace(',', '').replace('+', '')
        #get addreess
        adrs = tag.find('address', {'data-test':'property-card-addr'}).text
        #get remainign property details (Beds, baths, sq footage)
        for ultag in tag.find_all('ul', {'class': re.compile('^StyledPropertyCardHomeDetailsList*')}):
            for litag in ultag.find_all('li'):
                if "lot" in litag.text:
                    beds = 'nan'
                    baths = 'nan'
                    sqfoot = 'nan'
                else:
                    if "bds" in litag.text:
                        beds = litag.text[:-4].replace('-', '0')
                    elif "bd" in litag.text:
                        beds = litag.text[:-3].replace('-', '0')
                    elif "ba" in litag.text:
                        baths = litag.text[:-3].replace('-', '0')
                    elif "sqft" in litag.text:
                        temp = litag.text[:-5].replace(',', '')
                        sqfoot = temp.replace('-','0')
        print(zid, price, adrs, beds, baths, sqfoot)

        #Lets check the DB for this ID
        cursor = db_connection.cursor()
        query = "SELECT 1 FROM `listings_tbl` WHERE `id` = " + zid
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        if not results:
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO `listings_tbl`(`id`, `address`, `beds`, `baths`, `sqfoot`, `DateAdded`) VALUES ('"+ zid +"','"+ adrs +"','"+ beds +"','"+ baths +"','"+ sqfoot +"','"+ str(date.today()) +"')")
            db_connection.commit()
            cursor.execute("INSERT INTO `price_tbl`(`id`, `price`, `dateChanged`) VALUES ('"+ zid +"','"+ price +"','"+ str(date.today()) +"')")
            db_connection.commit()
            cursor.close()
            print("Property Added to DB")
        if results:
            #check if price has changed
            cursor = db_connection.cursor()
            query = "SELECT `dateChanged`,`price` FROM `price_tbl` WHERE `id` = " + zid
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            #extract just the dates changed
            dates = [x[0] for x in results]
            latestprice = results[dates.index(max(dates))][1]
            print(price, latestprice)
            if int(price) != int(latestprice):
                print("price update")
                cursor = db_connection.cursor()
                cursor.execute("INSERT INTO `price_tbl`(`id`, `price`, `dateChanged`) VALUES ('"+ zid +"','"+ price +"','"+ str(date.today()) +"')")
                db_connection.commit()
                cursor.close()
            
        
db_connection.close()


#Can search zpid like this
        #https://www.zillow.com/homedetails/69283610_zpid/
        
            


    
