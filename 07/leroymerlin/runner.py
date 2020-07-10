from scrapy.crawler import CrawlerProcess           # Импортируем класс для создания процесса
from scrapy.settings import Settings                # Импортируем класс для настроек

from leroymerlin import settings                      # Наши настройки
from leroymerlin.spiders.lm import LmSpider         # Класс паука
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
mongo_base = client.lm_scrapy
collection_lm = mongo_base['lm']

if __name__ == '__main__':
    crawler_settings = Settings()                   # Создаем объект с настройками
    crawler_settings.setmodule(settings)            # Привязываем к нашим настройкам

    process = CrawlerProcess(settings=crawler_settings)      # Создаем объект процесса для работы
    # process.crawl(LmSpider, search=['молоток'])            # Добавляем нашего паука
    process.crawl(LmSpider)                                  # Добавляем нашего паука
    process.start()                                          # Пуск

for item in collection_lm.find({}):
    pprint(item)
print(f'Всего в базе данных {collection_lm.count_documents({})} позиций')
collection_lm.drop()  # удаляем БД для очистки памяти ! Опционально - в целях обучения
