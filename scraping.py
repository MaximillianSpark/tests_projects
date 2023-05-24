import requests
from bs4 import BeautifulSoup
import lxml
import os, time
import json
from datetime import datetime

# Создаем папку data для хранения json файлов
directory = "data"
new_dir = "./"
path = os.path.join(new_dir, directory)

if os.path.exists(path):
    print("Папка уже существует")
else:
    os.mkdir(path)
    
directory = "data/pagenation_products"
new_dir = "./"
path = os.path.join(new_dir, directory)

if os.path.exists(path):
    print("Папка уже существует")
else:
    os.mkdir(path)

date = datetime.now()
print(date)
# Создадим Headers, для get запросов
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
    "Accept-Language" : "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept" : "*/*",
    "content-type" : "text/html; charset=UTF-8"
}
url = "https://www.dns-shop.kz/catalog/"
rec = requests.get(url=url, headers=headers)
scrap = rec.text
soup = BeautifulSoup(scrap, "lxml")
first_catalogs = soup.find_all("a", class_="subcategory__childs-item")



first_catalogs_dict = {}
for item in first_catalogs:
    ftext_item = item.text
    flink_item = "https://www.dns-shop.kz" + item.get("href")
    first_catalogs_dict.setdefault(ftext_item, flink_item)
    
    
with open("data/catalogs_dict.json", "a", encoding="utf-8") as file:
    json.dump(first_catalogs_dict, file, indent=4, ensure_ascii=False)
    

second_catalogs_dict = {}
for key, value in first_catalogs_dict.items():
    src = requests.get(url=value, headers=headers)
    second_scrap = src.text
    # time.sleep(2)
    soup = BeautifulSoup(second_scrap, "lxml")
    second_catalog = soup.find_all(class_="subcategory__item")
    
    
    for item in second_catalog:
        s_text_item = item.find(class_="subcategory__title").text
        s_link_item = "https://www.dns-shop.kz" + item.get("href")
        second_catalogs_dict.setdefault(s_text_item, s_link_item)
    


with open("data/catalogs_dict.json", "a", encoding="utf-8") as file:
    json.dump(second_catalogs_dict, file, indent=4, ensure_ascii=False)
    
    
third_catalogs_dict = {}
for key, value in second_catalogs_dict.items():
    src = requests.get(url=value, headers=headers)
    # time.sleep(2)
    third_scrap = src.text
    soup = BeautifulSoup(third_scrap, "lxml")
    third_catalog = soup.find_all(class_="subcategory__item")
    
    
    for item in third_catalog:
        t_text_item = item.find(class_="subcategory__title").text
        t_link_item = "https://www.dns-shop.kz" + item.get("href")
        third_catalogs_dict.setdefault(t_text_item, t_link_item)


with open("data/catalogs_dict.json", "a", encoding="utf-8") as file:
    json.dump(third_catalogs_dict, file, indent=4, ensure_ascii=False)
    

fourth_catalogs_dict = {}
for key, value in third_catalogs_dict.items():
    src = requests.get(url=value, headers=headers)
    # time.sleep(2)
    fourth_scrap = src.text
    soup = BeautifulSoup(fourth_scrap, "lxml")
    fourth_catalog = soup.find_all(class_="subcategory__item")
    
    
    for item in fourth_catalog:
        f_text_item = item.find(class_="subcategory__title").text
        f_link_item = "https://www.dns-shop.kz" + item.get("href")
        fourth_catalogs_dict.setdefault(f_text_item, f_link_item)


with open("data/catalogs_dict.json", "a", encoding="utf-8") as file:
    json.dump(fourth_catalogs_dict, file, indent=4, ensure_ascii=False)
    
    
with open("data/catalogs_dict.json", encoding="utf-8") as file:
    cd = file.read()
    con = json.loads(cd)
    

first_pagen_products = {}
final_parse = {}
# Циклом соберем товары из каталога
for key, value in con.items():
    src = requests.get(url=value, headers=headers)
    # time.sleep(2)
    pagen_first = src.text
    soup = BeautifulSoup(pagen_first, "lxml")
    pagen_catalog = soup.find_all("div", class_="catalog-product")
    
   
    for item in pagen_catalog[:5]:
        product_name = item.find(class_="catalog-product__name").text
        product_link = "https://www.dns-shop.kz" + item.find("a").get("href")
        product_price = item.find(class_="product-buy__price")
        final_parse.setdefault(product_name.rsplit(' [')[0], {"Наименование": product_name, "Ссылка": product_link, "Цена": product_price})
        first_pagen_products.setdefault(key, final_parse)
       
    final_parse = {}
        
with open(f"data/pagenation_products/products.json", "w", encoding="utf-8") as file:
    json.dump(first_pagen_products, file, indent=4, ensure_ascii=False)
    
date1 = datetime.now()
print(date1)
        