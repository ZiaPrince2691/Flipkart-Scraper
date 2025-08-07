from functions import *

print('''
    ********************************************************
    ------------------- Flipkart Scraper -------------------
    ********************************************************
      
    Hey! How can I help you :
            [1] Get a CSV file of items under your budget
            [2] Monitor some items and get notified whenever there is a change in price
''')

choice = int(input("Choose between 1 and 2 : "))

if choice == 1:
    scraper()
elif choice == 2:
    
    url = f"{input('Enter the url of item : ')}"
    old_price = int(input('Enter its current price : '))
    to = input('Enter your Email : ')
    try:
        df = pd.read_csv('monitored_items.csv')
        df.loc[len(df)+1] = [url, old_price, to]
        df.to_csv('monitored_items.csv', index=False)
        
    except:
        df = pd.DataFrame({
            'url' : [url],
            'old_price' : [old_price],
            'to' : [to]
        })
        df.to_csv('monitored_items.csv', index=False)