# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД. Магазины
# можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pprint import pprint
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')

hits = driver.find_element_by_xpath(
    "//div[contains(text(),'Хиты продаж')]/ancestor::div[@data-init='gtm-push-products']")

while True:
    try:
        next_button = WebDriverWait(hits, 5).until(
            EC.presence_of_element_located((By.XPATH, ".//a[contains(@class, 'next-btn')][not(contains(@class, 'disabled'))]"))
        )

        next_button.click()
        time.sleep(1)

    except exceptions.TimeoutException:
        print('Сбор данных окончен')
        break

hits = hits.find_elements_by_xpath(".//li[contains(@class, 'gallery-list-item')]")

hits_set = []
num = 0
for hit in hits:
    item = {}

    data_product_info = hit.find_element_by_xpath(".//a[@class='sel-product-tile-title']").get_attribute('data-product-info').replace('\n', '').replace('\t', '')
    data_product_info = data_product_info.replace('{', '').replace('}', '').replace('"', '').replace(': ', ',').split(',')
    i = 0
    product_info = {}
    while i < len(data_product_info) - 1:
        product_info[data_product_info[i]] = data_product_info[i + 1]
        i += 2

    url = hit.find_element_by_xpath(".//a[@class='sel-product-tile-title']").get_attribute('href')

    item['_id'] = product_info.get('productId')
    item['title'] = product_info.get('productName')
    item['price'] = float(product_info.get('productPriceLocal'))
    item['url'] = url

    hits_set.append(item)
    num += 1

pprint(hits_set)
print(f'Всего {num} товаров')
