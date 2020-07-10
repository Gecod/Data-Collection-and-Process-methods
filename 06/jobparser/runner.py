from scrapy.crawler import CrawlerProcess  # Импортируем класс для создания процесса
from scrapy.settings import Settings  # Импортируем класс для настроек

from jobparser import settings  # Наши настройки
from jobparser.spiders.hhru import HhruSpider  # Класс паука
from jobparser.spiders.sjru import SjruSpider  # Класс второго паука
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
# db = client['vacancies_db']
# collection = db.vacancies_collection
mongo_base = client.vacancy_scrapy
collection_hh = mongo_base['hhru']
collection_sj = mongo_base['sjru']

if __name__ == '__main__':
    crawler_settings = Settings()  # Создаем объект с настройками
    crawler_settings.setmodule(settings)  # Привязываем к нашим настройкам

    process = CrawlerProcess(settings=crawler_settings)  # Создаем объект процесса для работы
    process.crawl(HhruSpider)  # Добавляем HH паука
    process.crawl(SjruSpider)  # Добавляем SJ паука

    process.start()  # Пуск

for vacancy in collection_hh.find({}):
    pprint(vacancy)
for vacancy in collection_sj.find({}):
    pprint(vacancy)
print(f'Всего в базе данных HH {collection_hh.count_documents({})} вакансий')
print(f'Всего в базе данных SJ {collection_sj.count_documents({})} вакансий')
# collection_hh.drop()  # удаляем БД для очистки памяти ! Опционально - в целях обучения
# collection_sj.drop()  # удаляем БД для очистки памяти ! Опционально - в целях обучения
# print(f'Всего в базе данных HH {collection_hh.count_documents({})} вакансий')
# print(f'Всего в базе данных SJ {collection_sj.count_documents({})} вакансий')
