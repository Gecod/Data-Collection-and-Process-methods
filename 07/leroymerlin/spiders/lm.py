import scrapy
from scrapy.http import HtmlResponse        # Для подсказок объекта response
from leroymerlin.items import LeroymerlinItem   # Подключаем класс из items
from scrapy.loader import ItemLoader  # Подключаем ItemLoader

class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']
    # start_urls = ['http://leroymerlin.ru/']
    # Стартовая ссылка (точка входа)
    start_urls = ['https://samara.leroymerlin.ru/search/?q=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA']

    # def __init__(self, search):
    #     start_urls = [f'https://leroymerlin.ru/search/?q={param}&suggest=true' for param in search]

    def parse(self, response):
        # Ищем ссылку для перехода на следующую страницу
        next_page = response.css('a.paginator-button.next-paginator-button::attr(href)').extract_first()

        # Ищем на полученной странице ссылки на товары
        goods_links = response.css('a.black-link.product-name-inner::attr(href)').extract()
        for link in goods_links:  # Перебираем ссылки
            yield response.follow(link, callback=self.item_parse)  # Переходим по каждой ссылке и обрабатываем ответ методом item_parse

        yield response.follow(next_page,
                              callback=self.parse)  # Переходим по ссылке на следующую страницу и возвращаемся к началу метода parse

    def item_parse(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)      # Работаем через item loader
        loader.add_xpath('_id', '//span[@slot="article"]/text()')           # Получаем артикул товара
        loader.add_xpath('name', '//h1[@itemprop="name"]/text()')           # Получаем наименование товара
        loader.add_xpath('photos', '//source[contains(@media, "only screen")][@itemprop="image"][1]/@srcset')         # Все фото
        loader.add_xpath('parameters', ['//div[@class="def-list__group"]/dt/text()', '//div[@class="def-list__group"]/dd/text()'])   # Параметры товара в объявлении
        loader.add_xpath('link', '//link[@itemprop="url"]/@href')           # Ссылка
        loader.add_xpath('price', '//span[@slot="price"]/text()')           # Цена
        yield loader.load_item()
