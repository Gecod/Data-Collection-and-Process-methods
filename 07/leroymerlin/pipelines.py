# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import os
from urllib.parse import urlparse


class DataBasePipeline:
    def __init__(self):  # Конструктор, где инициализируем подключение к СУБД
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lm_scrapy

    def add_to_db(self, item, collection_name):
        collection = self.mongo_base[collection_name]  # Выбираем коллекцию по имени паука
        collection.insert_one(item), {'upsert': True}  # Добавляем в базу данных
        pass

    def process_item(self, item, spider):
        collection_name = spider.name  # Выбираем коллекцию по имени паука
        product = {
            '_id': item['_id'],
            'name': item['name'],
            'photos': item['photos'],
            'parameters': item['parameters'],
            'link': item['link'],
            'price': item['price']
        }

        self.add_to_db(product, collection_name)

        return item


class LeroymerlinPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img, meta=item)  # Скачиваем фото и передает item через meta
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        item = request.meta
        pathname = item['_id']+'_'+item["name"][:16]
        return pathname + '/' + os.path.basename(urlparse(request.url).path)

    # def item_completed(self, results, item, info):
    #     if results:
    #         item['photos'] = [itm[1] for itm in results if itm[0]]
    #     return item


