from os import name
import requests
import logging
from bs4 import BeautifulSoup
from time import sleep


logging.basicConfig(filename='parser.log', level=logging.INFO)

headers = {
    "Accept":  "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
}

def get_html(page=1):
    '''Функция get_html возвращает первую страницу, если не возникает сетевых ошибок'''
    try:
        url = f"https://www.avito.ru/moskva/planshety_i_elektronnye_knigi/elektronnye_knigi-ASgBAgICAUSYAohO?cd=1&p={page}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except(requests.RequestException, ValueError):
        logging.error(f'Ошибка {response.status_code}')
        return False
    except Exception as er:
        logging.error(er)
        return False

def get_products_links():
    '''Функция get_products_links возвращает список ссылок на все товары категории'''
    main_page = get_html()
    if main_page:
        soup = BeautifulSoup(main_page, 'lxml')
        # Определяет количество страниц товаров данной категории
        count_pages = int(soup.find('div', class_="pagination-root-2oCjZ").find_all('span', class_="pagination-item-1WyVp")[-2].text)
        
        links = []
        for i in range(1, 3): # test 
            page = get_html(i)
            soup = BeautifulSoup(page, 'lxml')
            item_card = soup.find_all('div', class_="iva-item-content-m2FiN")
            for item in item_card:
                link = f"https://www.avito.ru{item.find('div', class_='iva-item-titleStep-2bjuh').find('a').get('href')}"
                links.append(link)
        return links
    return False

def get_product_html():
    '''Функция get_product_html возвращает список html-страниц по каждому товару категории'''
    links = get_products_links()
    if links:
        html_of_products = []
        for link in links:
            try:
                response = requests.get(link, headers=headers)
                response.raise_for_status()
            except(requests.RequestException, ValueError):
                logging.error(f'Ошибка {response.status_code}')
                continue
            except Exception as er:
                logging.error(er)
                continue
            html_of_products.append(response.text)
            sleep(5)
        return html_of_products
    return False

def get_product_info():
    '''Функция get_product_info выводит информацию по каждому товару'''
    html_of_products = get_product_html()
    if html_of_products:
        for html in html_of_products:
            soup = BeautifulSoup(html, 'lxml')

            name = soup.find('div', class_="item-view-content").find('span', class_="title-info-title-text").text.strip()
            id = soup.find('div', class_="item-view-content-right").find('div', class_="item-view-search-info-redesign").find('span').text.strip()[2:]
            published = soup.find('div', class_="title-info-actions").find('div', class_="title-info-metadata-item-redesign").text.strip()
            link_photo = soup.find('div', class_="item-view-content").find('div', class_="gallery-img-frame js-gallery-img-frame").get('data-url').strip()
            price = soup.find('div', class_="item-view-content-right").find('span', class_="js-item-price").text.strip()
            try:
                address = soup.find('div', class_="item-view-block item-view-map js-item-view-map").find('span', class_="item-address__string").text.strip()
            except AttributeError:
                address = '' 
            try:
                description = soup.find('div', class_="item-description").text.strip()
            except AttributeError:
                description = ''

            print(name)
            print(id)
            print(published)
            print(link_photo)
            print(address)
            print(price)
            print(description)
            print('----------')
    return False
     
if __name__ == "__main__":
    get_product_info()
