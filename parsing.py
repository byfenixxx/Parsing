from datetime import datetime
import csv
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

def get_html(url):
    response = requests.get(url)
    return response.text

def write_data_to_csv(data):
    with open("wildberries.csv", "a") as data_file:
        writer = csv.writer(data_file, delimiter="/")
        writer.writerow((data["title"], data["description"], data["price"]))

def get_data_from_html(html):
    soup = BeautifulSoup(html, "lxml")
    products_list = soup.find_all("div", class_="dtList-inner")
    for product in products_list:
        try:
            title = product.find("strong", class_="brand-name c-text-sm").text
        except:
            title = ""
        
        try:
            price = product.find("ins", class_="lower-price")
            print(price)
        except:
            price = ""

        try:
            description = product.find("div", class_="dtlist-inner-brand-name").find("span", class_="goods-name c-text-sm").text
        except:
            description = ""
        
        data = {"title": title, "description": description, "price": price}
        write_data_to_csv(data)

def get_last_page(html):
    soup = BeautifulSoup(html, "lxml")
    last_page = soup.find("div", class_="pageToInsert").find_all("a")[-2].text
    return int(last_page)

def speed_up(url):
    html = get_html(url)
    data = get_data_from_html(html)

def main():
    start = datetime.now()
    url = "https://kg.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki"
    pages = "?sort=popular&page="
    last_page = get_last_page(get_html(url))
    urls = [url + pages + str(page) for page in range(1, last_page + 1)]
    # with Pool(10) as p:
    #     p.map(speed_up, urls)
    # print(urls)
    # print(datetime.now() - start)
    # for page in range(1, last_page + 1):
    #     new_url = url + pages + str(page)
    #     get_data_from_html(get_html(new_url))
    data = get_data_from_html(get_html(url))
    print(data)

if __name__ == "__main__":
    main()
