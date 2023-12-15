import requests
from bs4 import BeautifulSoup
from sacrap1 import get_data
import time
import random
import sqlite3
db = sqlite3.connect("data_scrap.db")
cursor = db.cursor()
cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
        name TEXT,
        url TEXT NOT NULL PRIMARY KEY,
        phones_list TEXT,
        address TEXT
        )
    ''')
item_name = get_data.item_name

headers = {
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
# def get_data(file_path):
#     with open(file_path) as file:
#         urls_list = [url.strip() for url in file.readlines()]
#     result_list = []
#     urls_count = len(urls_list)
#     count = 1
#     for url in urls_list[:2]:
#         response = requests.get(url=url, headers = headers)
#         soup = BeautifulSoup(response.text, "lxml")
#         try:
#             item_name = soup.find("span", {"itemprop" : "name"}).text.strip()
#         except Exception as _ex:
#             item_name = None 
#         item_phones_list = []
#         try:
#             item_phones = soup.find("div", class_="service-phones-list").find_all("a", class_="js-phone-number")
            
#             for phone in item_phones:
#                 item_phone = phone.get("href").split(":")[-1].strip()
#                 item_phones_list.append(item_phone)
#         except Exception as _ex:
#             item_phones_list = None
#         print(item_name,item_phones_list) 
#         try:
#             item_address = soup.find("address", class_="iblock").text.strip()
#         except Exception as _ex:
#             item_address = None
#         cursor.execute(
#             'INSERT or REPLACE INTO data(name, url, phones_list, address)'
#             ' VALUES(?, ?, ?, ?)', (str(item_name), str(url), str(item_phones_list), str(item_address))
#             )
#         time.sleep(random.randrange(2, 5))
#         if count%10 == 0:
#             time.sleep(random.randrange(5, 9))    
#         print(f"[+] Processed: {count}/{urls_count}")
#         count += 1  
#     cursor.execute("SELECT * FROM data")
#     for i in cursor.fetchall():
#         print(i)
#     db.commit()
#     db.close()    

def main():
    get_data(file_path="items_urls.txt")
if __name__ == "__main__":
    main()  