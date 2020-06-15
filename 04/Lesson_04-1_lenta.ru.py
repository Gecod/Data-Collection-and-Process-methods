# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.ru/news
# Для парсинга использовать xpath. Структура данных должна содержать:
# название источника,
# наименование новости,
# ссылку на новость,
# дата публикации

from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['news_db']
collection = db.news_collection

main_link = 'https://lenta.ru'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                         Chrome/83.0.4103.97 Safari/537.36'}

response = requests.get(main_link, headers=header)
dom = html.fromstring(response.text)
blocks = dom.xpath("//div[contains(@class, 'item news')][not(contains(@href, 'moslenta.ru'))]")

# news_set = []
num = 0

for block in blocks:
    item = {}

    name = block.xpath(".//a/span/text()")[0].replace('\xa0', ' ')
    link = main_link+block.xpath(".//a/@href")[0]
    source_name = 'Lenta Ru'
    publication_date = '-'.join(block.xpath(".//a/@href")[0].split('/')[2:5])

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
