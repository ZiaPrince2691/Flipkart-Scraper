from functions import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

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