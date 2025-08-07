from functions import *

df = pd.read_csv('monitored_items.csv')

for index,row in df.iterrows():
    monitor_item(row['url'], row['old_price'], SENDER, PASSWORD, row['to'])