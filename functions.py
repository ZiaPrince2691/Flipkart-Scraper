from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from email.message import EmailMessage
import smtplib
import time

SENDER = 'muhammadzia19285@gmail.com'
PASSWORD = 'dvvc mwqh pfjn wmok'

def send_email(sender, password, to, message):

    subject = "Change in price of an item you were interested in."

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

def get_new_price(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    new_price = int(driver.find_element(By.CLASS_NAME , 'Nx9bqj').text.replace('₹',''))
    return new_price

def monitor_item(url, old_price, sender, password, to):
    new_price = get_new_price(url)
    if new_price < old_price:
        message = f'''
            The price of the product you asked me to monitor has been decreased from ₹{old_price} to ₹{new_price}.
            Check it out :-
            {url}
        '''
        send_email(sender, password, to, message)

def scrape_data_coloumn(products, names, prices, links):
    
    for product in products:

        try:
            product_name = product.find('div', class_ = 'KzDlHZ').text
        except:
            product_name = np.nan

        try:    
            product_price_raw = product.find('div', class_ = 'Nx9bqj _4b5DiR')
            product_price = int(product_price_raw.text[1:].replace(',' , ''))
        except:
            product_price = np.nan

        try:
            relative_link = product.find('a', class_ = 'CGtC98').get('href')
            product_link = 'flipkart.com' + relative_link
        except:
            product_link = np.nan

        names.append(product_name)
        prices.append(product_price)
        links.append(product_link)

def scrape_data_grid(products, names, prices, links):
    
    for product in products:
        try:
            product_name = product.find('a', class_ = 'wjcEIp').get('title')
        except:
            product_name = np.nan

        try:    
            product_price_raw = product.find('div', class_ = 'Nx9bqj')
            product_price = int(product_price_raw.text[1:].replace(',' , ''))
        except:
            product_price = np.nan

        try:
            relative_link = product.find('a', class_ = 'wjcEIp').get('href')
            product_link = 'flipkart.com' + relative_link
        except:
            product_link = np.nan

        names.append(product_name)
        prices.append(product_price)
        links.append(product_link)

def scrape_data_from_page(html, names, prices, links):
    
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('div', class_ = 'slAVV4')

    if len(products) == 0:
        products = soup.find_all('div', class_ = 'tUxRFH')
        scrape_data_coloumn(products, names, prices, links)
    else:
        scrape_data_grid(products, names, prices, links)
    
def filter_negative_keywords(df, negative_keywords):
    negative_keywords = negative_keywords.replace(' ', '')
    negative_keywords = negative_keywords.replace(',', '|')

    if not negative_keywords.strip():
        return df
    
    print(negative_keywords)
    df['Names'] = df['Names'].astype(str)
    df = df[~df['Names'].str.contains(negative_keywords, case=False, na=False)]
    return df

def scrape_all_pages(driver, names, prices, links):
    
    while True :

        old_data_length = len(names)
        scrape_data_from_page(driver.page_source, names, prices, links)
        print(f'Products scraped : {old_data_length}')

        next_btn = driver.find_elements(By.CLASS_NAME , '_9QVEpD')[-1]
        time.sleep(1)

        if len(names) == old_data_length:
            break
        
        if next_btn.text == 'NEXT':
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(2)
        else:
            break

def get_data(names, prices, links, negative_keywords):
    df = pd.DataFrame({
        'Names' : names,
        'Prices' : prices,
        'Links' : links
    } , index = [i for i in range(1,len(names)+1)])

    df = df.dropna()
    df = filter_negative_keywords(df, negative_keywords)
    df = df.sort_values(by='Prices')
    df.index = [i for i in range(1,len(df)+1)]

    return df

def create_files(df, product , budget):

    product_name = product.replace(' ' , '_')
    df = df[df['Prices'] <= float(budget)] 
    df.to_csv(f'{product_name}s_under_{budget}.csv')

def scraper():
    product           = input('     What do you want to buy? : ')
    budget            = input(' What is your maximum budget? : ')
    negative_keywords = input("Enter Keywords you don't want : ")
    print('Please wait.....\n It may take few minutes.....\n Thanks for your patience.....')

    url = f"https://www.flipkart.com/search?q={product}&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D{budget}"

    names = []
    prices = []
    links = []

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)
    print(driver.title)

    scrape_all_pages(driver, names, prices, links)
    driver.quit()

    df = get_data(names, prices, links, negative_keywords)
    create_files(df, product , budget)