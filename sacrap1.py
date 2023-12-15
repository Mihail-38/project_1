from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from urllib.parse import unquote


headers = {
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def get_source_html(url):
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    try:
        driver.get(url=url)
        time.sleep(3)
        while True:
            find_more_element = driver.find_element(By.CLASS_NAME,"catalog-button-showMore.js-paging-block")
            if driver.find_elements(By.CLASS_NAME,"js-loading-box.loading-box-img"):
                actions = ActionChains(driver)
                actions.move_to_element(find_more_element).perform()
                find_more_el =  driver.find_element(By.CLASS_NAME,"js-next-page.button.button-show-more.button-block.button40.button-primary")
                find_more_el.click()
                time.sleep(3)
            else:
                with open("source-page.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)  
                break
                
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()
        
def get_items_urls(file_path):
    file = open(file_path, encoding="utf-8")
    src = file.read()
    soup = BeautifulSoup(src, "lxml")
    urls = []
    items_divs = soup.find_all('div', class_="minicard-item__info")
    for item in items_divs:
        item_url = item.find("h2", class_="minicard-item__title").find("a").get("href")
        urls.append(item_url)
    with open("items_urls.txt", "w", encoding="utf-8") as file:
        for url in urls:
            file.write(f"{url}\n")
    return "[INFO] Urls correct successfully"
def get_data(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]
    result_list = []
    urls_count = len(urls_list)
    count = 1
    for url in urls_list[:2]:
        response = requests.get(url=url, headers = headers)
        soup = BeautifulSoup(response.text, "lxml")
        try:
            item_name = soup.find("span", {"itemprop" : "name"}).text.strip()
        except Exception as _ex:
            item_name = None 
        item_phones_list = []
        try:
            item_phones = soup.find("div", class_="service-phones-list").find_all("a", class_="js-phone-number")
            
            for phone in item_phones:
                item_phone = phone.get("href").split(":")[-1].strip()
                item_phones_list.append(item_phone)
        except Exception as _ex:
            item_phones_list = None
        print(item_name,item_phones_list) 
        try:
            item_address = soup.find("address", class_="iblock").text.strip()
        except Exception as _ex:
            item_address = None
        cursor.execute(
            'INSERT or REPLACE INTO data(name, url, phones_list, address)'
            ' VALUES(?, ?, ?, ?)', (str(item_name), str(url), str(item_phones_list), str(item_address))
            )
        time.sleep(random.randrange(2, 5))
        if count%10 == 0:
            time.sleep(random.randrange(5, 9))    
        print(f"[+] Processed: {count}/{urls_count}")
        count += 1  
    cursor.execute("SELECT * FROM data")
    for i in cursor.fetchall():
        print(i)
    db.commit()
    db.close()    
def main():
    get_source_html(url="https://irkutsk.zoon.ru/medical/page-2/")
    get_items_urls(file_path="source-page.html")
    
if __name__ == "__main__":
    main()  