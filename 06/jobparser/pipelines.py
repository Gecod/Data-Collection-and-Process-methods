# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient, errors


class JobparserPipeline:                            # Класс для обработки item'a
    def __init__(self):                             # Конструктор, где инициализируем подключение к СУБД
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy_scrapy

    def process_item(self, item, spider):           # Метод, куда прилетает сформированный item
        if spider.name == 'hhru':                   # Направляем item на обработку в зависимости от имени паука
            self.process_hh_item(item, spider.name)
        if spider.name == 'sjru':                   # Направляем item на обработку в зависимости от имени паука
            self.process_sj_item(item, spider.name)
        return item

    def add_to_db(self, vacancy, collection_name):
        collection = self.mongo_base[collection_name]  # Выбираем коллекцию по имени паука
        collection.insert_one(vacancy), {'upsert': True}  # Добавляем в базу данных

    # Headhunter processing

    def process_hh_item(self, item, collection_name):
        vacancy = {
            '_id': 'hh_'+item['link'].split('?')[0].split('/')[-1],
            'name': item['name'],
            'salary_min': self.get_hh_salary_min(item),
            'salary_max': self.get_hh_salary_max(item),
            'currency': self.get_hh_currency(item),
            'link': item['link'].split('?')[0],
            'source_site': 'https://hh.ru/'
        }

        self.add_to_db(vacancy, collection_name)

    def get_hh_salary_min(self, item):
        if 'salary' not in item:
            return None

        salary = item['salary']

        if len(salary) < 2:
            return None

        if 'от ' in salary[0]:
            return int(salary[1].replace(' ', '').replace('\xa0', ''))

    def get_hh_salary_max(self, item):
        if 'salary' not in item:
            return None

        salary = item['salary']

        if len(salary) < 2:
            return None

        if ' до ' in salary:
            return int(salary[3].replace(' ', '').replace('\xa0', ''))

    def get_hh_currency(self, item):
        if 'salary' not in item:
            return None

        salary = item['salary']

        if len(salary) < 2:
            return None

        if 'от ' in salary[0] and ' до ' in salary[2]:
            return salary[5].replace(' ', '').replace('\xa0', '')

        if 'от ' in salary[0]:
            return salary[3].replace(' ', '')

    # Superjob processing

    def process_sj_item(self, item, collection_name):
        vacancy = {
            '_id': 'sj_'+item['link'].split('-')[-1].split('.')[0],
            'name': item['name'],
            'salary_min': self.get_sj_salary_min(item),
            'salary_max': self.get_sj_salary_max(item),
            'currency': self.get_sj_currency(item),
            'link': item['link'],
            'source_site': 'https://superjob.ru/'
        }

        self.add_to_db(vacancy, collection_name)

    def get_sj_salary_min(self, item):
        if 'salary' not in item:
            return None

        salary = item['salary']

        if len(salary) < 2:
            return None

        if 'от' in salary:
            return int(''.join(salary[-1].replace('\xa0', ' ').split(' ')[:-1]))
        elif 'до' not in salary:
            return int(salary[0].replace('\xa0', ''))
        else:
            return None

    def get_sj_salary_max(self, item):
        if 'salary' not in item:
            return None

        salary = item['salary']

        if len(salary) < 2:
            return None

        if 'до' in salary:
            return int(''.join(salary[-1].replace('\xa0', ' ').split(' ')[:-1]))
        elif 'от' not in salary:
            return int(salary[1].replace('\xa0', ''))
        else:
            return None

    def get_sj_currency(self, item):
        if 'salary' not in item:
            return None

        salary = item['salary']

        if len(salary) < 2:
            return None

        if 'от' or 'до' in salary:
            return salary[-1].replace('\xa0', ' ').split(' ')[-1]
        else:
            return salary[-1].replace('\xa0', ' ')
