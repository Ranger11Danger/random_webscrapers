from bs4 import BeautifulSoup
import requests
import lxml
import csv

def get_ajax(url, tire_id):
    session = requests.Session()
    session.get(f'https://www.rockymountainatvmc.com:443{url}')
    burp0_cookies = session.cookies.get_dict()
    burp0_url = f"https://www.rockymountainatvmc.com:443{url}?0-1.0-SelectionPanel-MainPanel-AttrsForm-Attrs-1-AttrList&idd1=60312&idd2=5187"
    burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"91\", \" Not;A Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "Wicket-Focusedelementid": "id8fSelectBoxIt", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept": "application/xml, text/xml, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "Wicket-Ajax": "true", "Wicket-Ajax-Baseurl": "tires-and-wheels/tusk-terrabite%C2%AE-radial-tire-p", "Origin": "https://www.rockymountainatvmc.com", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.rockymountainatvmc.com/tires-and-wheels/tusk-terrabite%C2%AE-radial-tire-p", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
    burp0_data = {"Attrs:1:AttrList": f"{tire_id}"}
    data = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
    soup = BeautifulSoup(data.text, 'lxml')
    price = soup.find('span', {'itemprop': 'price'}).get_text()
    sku = soup.find('span', {'itemprop': 'sku'}).get_text()
    name = soup.find('h2', {'itemprop': 'name'}).get_text()
    details = soup.find_all('ul')[-1].get_text()
    return(price,sku.split(" ")[1],name, details)

base_url = 'https://www.rockymountainatvmc.com'
url = 'https://www.rockymountainatvmc.com/tires-and-wheels/utv-tires?il_medium=promo&il_source=tires&page=All'

data = requests.get(url)
soup = BeautifulSoup(data.text, 'html.parser')
tires = soup.find('div', {'id': 'Families'})
filename = 'tires.csv'
with open(filename, 'w') as csvfile:
    fields = ['Name', 'Size', 'Height', 'Width', 'Wheel Size', 'Price', 'SKU', 'Image', 'Site Link', 'Details']
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for count,tire in enumerate(tires):
        
        url = tire.find('a')['href']
        
        #if url == '/tires-and-wheels/skat%7Etrak-talon-grip-tire-p':
        print(f"Found Tire {count + 1}/{len(tires)}")
        data = requests.get(base_url+url)
        soup = BeautifulSoup(data.text, 'html.parser')
        tests = soup.find('img', {'class': 'prodImgMed'})
        image = tests['src'][2:]
        forms = soup.find_all('form')
        for form in forms:
            if 'SelectionPanel-MainPanel-AttrsForm' in str(form):
                ids = form.find_all('option')
        for id in ids:
            if id.get_text() == 'Select':
                continue
            price, sku, name, det = get_ajax(url,id['value'])
            try:
                height = id.get_text().split('x')[0]
                width = id.get_text().split('x')[1].split('-')[0]
                wheel_size = id.get_text().split('x')[1].split('-')[1]
            except:
                try:
                    height = id.get_text().split('/')[0]
                    width = id.get_text().split('/')[1].split('-')[0]
                    wheel_size = id.get_text().split('/')[1].split('-')[1]
                except:
                    height = id.get_text().split('x')[0]
                    width = id.get_text().split('x')[1]
                    wheel_size = id.get_text().split('x')[2]
            #print(f"Name: {name}, Size: {id.get_text()}, Price: ${price}, SKU: {sku}, Image: {image}")
            csvwriter.writerow([f'{name}', f'{id.get_text()}',f'{height}', f'{width}', f'{wheel_size}', f'${price}', f'{sku}', f'=HYPERLINK("https://{image}", "Image Link")',f'=HYPERLINK("{base_url+url}", "Site Link")', f'{det}'])