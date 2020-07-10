# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить
# данные о письмах в базу данных
# * от кого,
# * дата отправки,
# * тема письма,
# * текст письма полный

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['letters_db']
collection = db.ai_172_collection

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mail.ru/')

assert "Mail.ru" in driver.title

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.RETURN)

elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NextPassword172')
elem.send_keys(Keys.RETURN)

driver.implicitly_wait(5)
first_letter = driver.find_element_by_class_name('js-letter-list-item')
driver.get(first_letter.get_attribute('href'))

assert "Почта Mail.ru" in driver.title

letters_total = int(driver.find_element_by_class_name("nav__item_active").get_attribute('title').split(' ')[1])
print(letters_total)
letters_quantity = int(input(f'Всего в ящике писем: {letters_total}. \n'
                             f'Сколько писем нужно просканировать начиная с самого позднего? \n'))

# letters_set = []
num = 0
i = 1
while i <= letters_quantity:
    item = {}

    sender = driver.find_element_by_xpath("//span[contains(@class, 'letter-contact')]").get_attribute('title')
    subject = driver.find_element_by_xpath("//h2[contains(@class, 'thread__subject')]").text
    date = driver.find_element_by_class_name("letter__date").text
    body = driver.find_element_by_class_name("letter__body").text  # текст сырой, необработанный, весь
    _id = driver.find_element_by_class_name('thread__letter').get_attribute('data-id')

    item['sender'] = sender
    item['subject'] = subject
    item['date'] = date
    item['body'] = body
    item['_id'] = _id

    collection.insert_one(item)
    num += 1
    i += 1

    if i > letters_quantity:
        break
    else:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'portal-menu-element_next')]"))
        )

        next_button.click()

    time.sleep(1)

driver.quit()

# pprint(letters_set)
print(f'Всего писем просканировано: {num}')

for item in collection.find({}):
    pprint(item)
print(f'Всего в базе данных {collection.count_documents({})} писем')
collection.drop()  # удаляю колекцию, чтобы не хранить БД
