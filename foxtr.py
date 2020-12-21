import json

import requests
from bs4 import BeautifulSoup

URL = 'https://www.foxtrot.com.ua'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'
}


def parse():
    mainHtml = get_html(URL)
    categUrls = get_categories_list(mainHtml)

    for url in categUrls:
        categHtml = get_html(url)
        itemUrls = get_items_list(categHtml)

        for url in itemUrls:
            itemHtml = get_html(url)
            fetchReviews(itemHtml)


def get_html(url):
    html = requests.get(url, headers=HEADERS)
    return html


def get_categories_list(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('li', class_='catalog__category-item jslink')[5:8]
    lst = list(map(lambda item: URL + item.find('div', class_='catalog-sub__body-row').find('a').get('href'), items))

    return lst


def get_items_list(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', class_='card')[:3]
    categ_urls_list = list(map(lambda item: URL + item.find('div', class_='card__image').find('a').get('href'), items))

    return categ_urls_list


def fetchReviews(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', class_='product-comment__item')
    item_title = soup.find('h1', class_='page__title').get_text(strip=True)
    lst = list(map(lambda item: {
        'author': item.find('div', class_='product-comment__item-title').get_text(strip=True),
        'date': item.find('div', class_='product-comment__item-date').get_text(strip=True),
        'text': item.find('div', class_='product-comment__item-text').get_text(strip=True)
    }, items))

    with open(f'{item_title[:30]}.json', 'w') as file:
        json.dump(lst, file, indent=2)

    return lst


parse()