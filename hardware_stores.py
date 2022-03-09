import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json

links = {
    "lowes" : "https://www.lowes.com/pd/DEWALT-12-in-15-Amp-Dual-Bevel-Sliding-Compound-Miter-Saw/1000145735",
    "homedepot" : "https://www.homedepot.com/p/DEWALT-15-Amp-Corded-12-in-Double-Bevel-Sliding-Compound-Miter-Saw-Blade-Wrench-Material-Clamp-DWS779/206541015",
    "ace" : "https://www.acehardware.com/departments/tools/power-tools/miter-saws/2111235"
}

def get_lowes_price(links,driver):
    
    driver.get(links["lowes"])
    data = driver.page_source
    elem = driver.find_element_by_xpath('/html/body/script[6]')
    data = json.loads(elem.get_attribute("innerHTML")[32:])    
    item_id = data['productId']
    name = data['productDetails'][str(item_id)]['product']['description']
    try:
        price = data['productDetails'][str(item_id)]['price']['itemPrice']
    except:
        price = data['productDetails'][str(item_id)]['price']['analyticsData']['mapPrice']
    avail = data['productDetails'][str(item_id)]['itemInventory']['analyticsData']['parcel']['productStockType']
    if avail == "STK":
        avail = True
    else:
        avail = False
    return(name, price, avail)

def get_homedepot_price(links, driver):
    
    driver.get(links["homedepot"])
    elem = driver.find_element_by_xpath('//*[@id="thd-helmet__script--productStructureData"]')
    data = json.loads(elem.get_attribute("innerHTML"))
    name = data['name']
    price = data['offers']['price']
    try:
        avail = data['offers']['availability'].split('/')[-1]
        if avail =="InStock":
            avail = True
    except:
        avail = False
    return(name, price, avail)

def get_ace_price(links, driver):
    
    driver.get(links["ace"])
    elem = driver.find_element_by_xpath('//*[@id="data-mz-preload-product"]')
    data = json.loads(elem.get_attribute("innerHTML"))
    name = data['content']['productName']
    price = data['price']['price']
    avail = data['purchasableState']['isPurchasable']
    return(name, price, avail)




if __name__ == "__main__":
    with open("output.txt", "w") as output_file:
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(options=options)

        name, price, avail = get_lowes_price(links,driver)
        output_file.write(f"Name: {name}\nPrice: {price}\nAvailability: {avail}\nLink: {links['lowes']}\n\n")
        name, price, avail = get_homedepot_price(links, driver)
        output_file.write(f"Name: {name}\nPrice: {price}\nAvailability: {avail}\nLink: {links['homedepot']}\n\n")
        name, price, avail = get_ace_price(links, driver)
        output_file.write(f"Name: {name}\nPrice: {price}\nAvailability: {avail}\nLink: {links['ace']}\n\n")
        driver.close()