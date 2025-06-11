from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

def scrape_data_from_page(html):
    
    soup = BeautifulSoup(html, 'html.parser')

    products = soup.find_all('div', class_ = 'slAVV4')

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

def filter_negative_keywords(df, negative_keywords):
    negative_keywords = negative_keywords.replace(' ', '')
    negative_keywords = negative_keywords.replace(',', '|')
    print(negative_keywords)
    df = df[~df['Names'].str.contains(negative_keywords, case=False, na=False)]
    return df

def scrape_all_pages(driver):
    
    while True :

        scrape_data_from_page(driver.page_source)

        next_btn = driver.find_elements(By.CLASS_NAME , '_9QVEpD')[-1]
        time.sleep(1)

        if next_btn.text == 'NEXT':
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(4)
        else:
            break

def get_data(names, prices, links):
    df = pd.DataFrame({
        'Names' : names,
        'Prices' : prices,
        'Links' : links
    } , index = [i for i in range(1,len(names)+1)])

    df = df.dropna()
    df = df.sort_values(by='Prices')
    df = filter_negative_keywords(df, negative_keywords)

    return df

def create_files(df):

    product_name = product.replace(' ' , '_')
    df.to_csv(f'all_{product_name}s.csv')

    df = df[df['Prices'] <= float(max_budget)] 
    df = df[df['Prices'] >= float(min_budget)] 
    df.to_csv(f'{product_name}s_under_{max_budget}.csv')

if __name__ == "__main__":    

    product           = input('     What do you want to buy? : ')
    max_budget        = input(' What is your maximum budget? : ')
    min_budget        = input(' What is your minimum budget? : ')
    negative_keywords = input("Enter Keywords you don't want : ")
    print('Please wait.....\n It may take few minutes.....\n Thanks for your patience.....')

    url = f"https://www.flipkart.com/search?q={product}"
    
    names = []
    prices = []
    links = []

    # options = Options()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    print(driver.title)

    scrape_all_pages(driver)
    driver.quit()

    df = get_data(names, prices, links)
    create_files(df)