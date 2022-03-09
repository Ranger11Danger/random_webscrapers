import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)


sheet = client.open("zillow stats capture")
  # Open the spreadhseet

sheet1 = sheet.sheet1
col = sheet1.col_values(1)  # Get a specific column
 
session = requests.session()
test = pd.DataFrame(columns=['House Link','Timestamp','Time on Zillow','Views','Saves'])
def get_data(soup):
        time = soup.find(text="Time on Zillow").parent.next_element.next_element.text
        views = soup.find(text="Views").next_element.text
        saves = soup.find(text="Saves").next_element.text
        return(time,views,saves)

col.remove("House Link")
for house in col:
    burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"91\", \" Not;A Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
    data = session.get(house, headers=burp0_headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    time, views, saves = get_data(soup)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data = {"House Link": house,"Timestamp": dt_string,"Time on Zillow": time, 'Views': views, 'Saves': saves}
    test = test.append(data, ignore_index=True)
    #print(f"Time on Zillow: {house_data[0]}\nViews: {house_data[1]}\nSaves: {house_data[2]}")

sheet1.update([test.columns.values.tolist()] + test.values.tolist())