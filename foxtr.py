import json

import requests
from bs4 import BeautifulSoup


URL = 'https://www.foxtrot.com.ua'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'
}

def get_html(url):
    html = requests.get(url, headers=HEADERS)
    return html

def get_categories_list(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('li', class_='catalog__category-item jslink')[5:8]
    lst = []

    for item in items:
        lst.append(URL + item.find('div', class_='catalog-sub__body-row').find('a').get('href'))
    return lst


def get_items_list(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', class_='card')[:3]
    lst = []

    for item in items:
        lst.append(URL + item.find('div', class_='card__image').find('a').get('href'))
    return lst

def parce_reviews(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', class_='product-comment__item')
    lst = []

    for item in items:

        lst.append({
            'author': item.find('div', class_='product-comment__item-title').get_text(strip=True),
            'date': item.find('div', class_='product-comment__item-date').get_text(strip=True),
            'text': item.find('div', class_='product-comment__item-text').get_text(strip=True)
        })

    # for page in range(1, 10):
    #     with open(f'{page}.json', 'w') as file:
    #         json.dump(lst, file, indent=2)

    return lst

def parse():
    html = get_html(URL)
    # print(get_categories_list(html))
    s = get_categories_list(html)
    for i in s:
        html = get_html(i)
        a = get_items_list(html)
        for q in a:
            html = get_html(q)
            # parce_reviews(html)
            print(parce_reviews(html))

parse()
