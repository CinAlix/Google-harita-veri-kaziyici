from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
from loguru import logger


print("""

 ██████╗  ██████╗  ██████╗  ██████╗ ██╗     ███████╗
██╔════╝ ██╔═══██╗██╔═══██╗██╔════╝ ██║     ██╔════╝
██║  ███╗██║   ██║██║   ██║██║  ███╗██║     █████╗  
██║   ██║██║   ██║██║   ██║██║   ██║██║     ██╔══╝  
╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗
 ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                                                    
@cinali   
""")

select = input("NE ARATMAK İSTİYORSUNUZ: ")
page = int(input("KAÇ SAYFA TARAMAK İSTERSİNİZ (LÜTFEN ÖNCEDEN KAÇ SAYFA OLDUĞUNA BAKINIZ): "))

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(f"https://www.google.com/search?q={select}&tbm=lcl")
time.sleep(3)

data = []

for a in range(page):
    html_main_page = driver.page_source

    soup = BeautifulSoup(html_main_page, 'html.parser')
    elements = soup.find_all(attrs={"jscontroller": "AtSb"})
    ids = [element.get('id') for element in elements]
    for b_id in ids:
        try:
            business_tag = driver.find_element(By.XPATH, f'//*[@id="{b_id}"]')
            business_tag.click()
            
            time.sleep(3)
            html = driver.page_source
            soup_phone = BeautifulSoup(html, 'html.parser')
            
            a = soup.find("div", id=b_id)
            star = a.find("span", class_="yi40Hd YrbPuc").text if a.find("span", class_="yi40Hd YrbPuc") else 'N/A'
            Review = a.find('span', class_='RDApEe YrbPuc').text.strip('()') if a.find('span', class_='RDApEe YrbPuc') else 'N/A'

            Phone_tag = soup_phone.find('a', {'data-dtype': 'd3ph'})
            phone_number = Phone_tag.find('span').text.strip() if Phone_tag and Phone_tag.find('span') else 'N/A'
            business_name = soup_phone.find('h2', {'data-attrid': 'title'}).find('span').text.strip() if soup_phone.find('h2', {'data-attrid': 'title'}) else 'N/A'
            address_span = soup_phone.find('span', class_='LrzXr').text.strip()
            
            logger.success(f"{business_name}, {address_span}, {phone_number}, {star}, {Review}")
            data.append({
                'İşletme İsmi': business_name,
                'Adres' : address_span,
                'İşletme Numarası': phone_number,
                'Yıldız': star,
                'Değerlendirme Sayısı': Review
            })
            
        except Exception as e:
            logger.error(f"Bir hata oluştu: {e}")
    next_page_btn = driver.find_element(By.XPATH, f'//*[@id="pnnext"]')
    next_page_btn.click()
    time.sleep(5)
driver.quit()

df = pd.DataFrame(data)

df.to_excel('data.xlsx', index=False)
logger.warning("Veriler 'data.xlsx' dosyasına kaydedildi.")
