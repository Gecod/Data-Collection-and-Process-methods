# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.ru/news
# Для парсинга использовать xpath. Структура данных должна содержать:
# название источника,
# наименование новости,
# ссылку на новость,
# дата публикации

from pprint import pprint
from lxml import html
import requests
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['news_db']
collection = db.news_collection

main_link = 'https://news.mail.ru'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                         Chrome/83.0.4103.97 Safari/537.36'}

response = requests.get(main_link, headers=header)
dom = html.fromstring(response.text)
blocks = dom.xpath("//a[contains(@class, 'js-topnews__item')]")

# news_set = []
num = 0

for block in blocks:
    item = {}

    name = block.xpath(".//span[contains(@class, 'photo__title')]/text()")[0].replace('\xa0', ' ')
    link = main_link+block.xpath("./@href")[0]

    inner_response = requests.get(link, headers=header)
    inner_dom = html.fromstring(inner_response.text)
    source_name = inner_dom.xpath("//a[contains(@class, 'breadcrumbs__link')]/span[@class='link__text']/text()")[0]
    publication_date = inner_dom.xpath("//span[contains(@class, 'breadcrumbs__text')]/@datetime")[0].replace('T', ' ')

    item['source_name'] = source_name
    item['name'] = name
    item['url'] = link
    item['publication_date'] = publication_date

    # news_set.append(item)
    num += 1
    collection.insert_one(item)

time.sleep(3)
blocks = dom.xpath("//ul[@class='list list_type_square list_half js-module']/*")
for block in blocks:
    item = {}

    name = block.xpath(".//a[contains(@class, 'list__text')]/text()")[0].replace('\xa0', ' ')
    link = block.xpath(".//a[contains(@class, 'list__text')]/@href")[0]

    if 'sport' in link:
        link = link
    else:
        link = main_link+link

    inner_response = requests.get(link, headers=header)
    inner_dom = html.fromstring(inner_response.text)
    source_name = inner_dom.xpath("//a[contains(@class, 'breadcrumbs__link')]/span[@class='link__text']/text()")[0]
    publication_date = inner_dom.xpath("//span[contains(@class, 'breadcrumbs__text')]/@datetime")[0].replace('T', ' ')

    item['source_name'] = source_name
    item['name'] = name
    item['url'] = link
    item['publication_date'] = publication_date

    # news_set.append(item)
    num += 1
    collection.insert_one(item)

time.sleep(3)
blocks = dom.xpath("//div[@class='cols__wrapper']//a[contains(@class, 'link')]")
for block in blocks:
    item = {}

    name = block.xpath("./span/text()")[0].replace('\xa0', ' ')
    link = block.xpath("./@href")[0]

    if 'sport' in link:
        link = link
    else:
        link = main_link+link

    inner_response = requests.get(link, headers=header)
    inner_dom = html.fromstring(inner_response.text)
    source_name = inner_dom.xpath("//a[contains(@class, 'breadcrumbs__link')]/span[@class='link__text']/text()")[0]
    publication_date = inner_dom.xpath("//span[contains(@class, 'breadcrumbs__text')]/@datetime")[0].replace('T', ' ')

    item['source_name'] = source_name
    item['name'] = name
    item['url'] = link
    item['publication_date'] = publication_date

    # news_set.append(item)
    num += 1
    collection.insert_one(item)

# pprint(news_set)
print(f'Всего {num} новостей')

# for item in collection.find({}):
#     pprint(item)
# print(f'Всего в базе данных {collection.count_documents({})} новостей')
# collection.drop()
