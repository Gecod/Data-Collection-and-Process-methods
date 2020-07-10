# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import MapCompose, TakeFirst, Compose      # Подключаем обработчики
import scrapy

def cleaner_price(value):
    price = float(value.replace(' ', ''))
    return price

def cleaner_id(value):
    _id = value.split(' ')[-1]
    return _id

def cleaner_link(value):
    link = 'https://samara.leroymerlin.ru'+value
    return link

def cleaner_parameters(value):
    # val = value.split('<sep>')
    params = {}
    steps = range(0, int(len(value) / 2))
    for step in steps:
        params[value[step]] = value[step + int(len(value) / 2)].replace('\n', '').replace('  ', '')
    return params

class LeroymerlinItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(cleaner_id))
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    parameters = scrapy.Field(output_processor=Compose(cleaner_parameters))
    link = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(cleaner_link))
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(cleaner_price))
