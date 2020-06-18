# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД. Магазины
# можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')

time.sleep(5)
button = driver.find_element_by_class_name('btn-approve-city')
button.click()

# time.sleep(5)
actions = ActionChains(driver)
# actions.move_by_offset(360, 50).click()
actions.move_by_offset(360, 100).perform()
time.sleep(5)
actions.click().perform()

driver.execute_script('window.scrollTo(0, 2000)')

button = driver.find_element_by_class_name('sel-hits-button-next')
button.click()

# elem = driver.find_element_by_class_name("close")
# elem.send_keys(Keys.ESCAPE)


# button = Keys.ESCAPE
# button.

# button = driver.find_element_by_class_name('close')
# button.click()

# button = WebDriverWait(driver, 5).until(
#     EC.element_to_be_clickable((By.CLASS_NAME, 'store-notification__button--submit'))
# )

# button.click()
#
# driver.execute_script('window.scrollTo(0, 2000)')
#
# button = WebDriverWait(driver, 5).until(
#     EC.element_to_be_clickable((By.CLASS_NAME, 'cookie-usage-notice__button'))
# )
# button.click()
#
# while True:
#     try:
#         button = WebDriverWait(driver, 5).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, 'catalog-grid-container__pagination-button'))
#         )
#         # driver.execute_script('window.scrollHeight')
#         button.click()
#     except:
#         break
