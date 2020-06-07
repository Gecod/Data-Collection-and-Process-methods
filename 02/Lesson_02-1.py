# 1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input
# или через аргументы) с сайта superjob.ru и hh.ru. Приложение должно анализировать
# несколько страниц сайта(также вводим через input или аргументы). Получившийся список
# должен содержать в себе минимум:
#
#     *Наименование вакансии
#     *Предлагаемую зарплату (отдельно мин. и отдельно макс.)
#     *Ссылку на саму вакансию
#     *Сайт откуда собрана вакансия
# По своему желанию можно добавить еще работодателя и расположение. Данная структура
# должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с
# помощью dataFrame через pandas.
#
# !!!В первую очередь делаем сайт hh.ru - его обязательно. sj.ru можно попробовать
# сделать вторым. Он находится в очень странном состоянии и возможна некорректная работа.!!!

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from time import sleep
import json

# https://samara.hh.ru/search/vacancy?st=searchVacancy&text=NAME%3A%28Data+scien*+OR+Data+analys*+OR+Python+OR+%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA+%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85+OR+%D0%9F%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82*+%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA+OR+Big+Data+OR+Data+Engineer+OR+Product+Analys*+OR+ML+engineer+OR+Machine+learning+OR+Computer+scien*%29&area=1&area=78&area=2&area=53&area=237&area=88&area=99&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=&items_on_page=100&no_magic=true&L_save_area=true
# https://samara.hh.ru/search/vacancy?st=searchVacancy&text=NAME%3A%28Data+scien*+OR+Data+analys*+OR+Python+OR+%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA+%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85+OR+%D0%9F%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82*+%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA+OR+Big+Data+OR+Data+Engineer+OR+Product+Analys*+OR+ML+engineer+OR+Machine+learning+OR+Computer+scien*%29&area=1&area=78&area=2&area=53&area=237&area=88&area=99
# https://samara.hh.ru/search/vacancy?st=searchVacancy&text=NAME%3A%28Data+scien*+OR+Data+analys*+OR+Python+OR+%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA+%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85+OR+%D0%9F%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82*+%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA+OR+Big+Data+OR+Data+Engineer+OR+Product+Analys*+OR+ML+engineer+OR+Machine+learning+OR+Computer+scien*%29&area=1
# search_query = 'NAME:(Data scien* OR Data analys* OR Python OR Аналитик данных OR Продукт* аналитик OR Big Data OR Data Engineer OR Product Analys* OR ML engineer OR Machine learning OR Computer scien*)'

main_link = 'https://samara.hh.ru'
# params = {'st': 'searchVacancy',
#           'text': 'NAME%3A%28Data+scien*+OR+Data+analys*+OR+Python+OR+%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA+%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85+OR+%D0%9F%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82*+%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA+OR+Big+Data+OR+Data+Engineer+OR+Product+Analys*+OR+ML+engineer+OR+Machine+learning+OR+Computer+scien*%29',
#           'area': '1'}
params = {'st': 'searchVacancy', 'text': 'Data scientist', 'area': '1', 'order_by': 'publication_time', 'only_with_salary': 'false', 'items_on_page': '100'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Accept': '*/*'}

response = requests.get(main_link + '/search/vacancy', params=params, headers=headers)

# with open('vac_list.json', 'w') as f:
#     json.dump(response.json(), f)
#
# # data = response.json()
# data = open('vac_list.json', 'r')
# sleep(10)
soup = bs(response.text, 'lxml')

# with open('vac_list.txt', 'w') as f:
#     # f.write(soup.lxml)
#     json.dump(soup.json(), f)

vacancies_block = soup.find('div', {'class': 'vacancy-serp'})

vacancies_list = vacancies_block.findChildren(recursive=False)
# next_word = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}).text
# print(next_word)
# print(vacancies_list)
vacancies = []
# tag_link = soup.find('a', {'class': 'bloko-link HH-LinkModifier'})
# link = tag_link['href']
# print(link)
num_steps = 0
# num_steps = int(vacancies_list.find('a', {'data-qa': 'pager-next'}).text)
while True:
    for vacancy in vacancies_list:

        vacancy_data = {}

        try:
            tag_link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})
            # print(tag_link)
            link = tag_link['href']
            name = tag_link.text
            # print(name)

            tag_link_c = vacancy.find('a', {'class': 'bloko-link bloko-link_secondary'})
            link_c = main_link + tag_link_c['href']
            company = tag_link_c.text

            geo_tag = vacancy.find('span', {'class': 'vacancy-serp-item__meta-info'}).text
            geo_tag = geo_tag.replace(' Как добраться?', '')
            geo_tag = geo_tag.replace('Как добраться?', '')
            geo_tag = geo_tag.replace(' и', ',')
            geo_tag = geo_tag.split(', ')
            city = geo_tag[0]
            if len(geo_tag) > 1:
                city_zone1 = geo_tag[1]
            else:
                city_zone1 = None

            try:
                # salary = vacancy.find('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite'}).nextSibling.text
                salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            except AttributeError:
                salary = None

            if salary is None:
                salary_min = None
                salary_max = None
                salary_curr = None
            else:
                salary = salary.replace('\xa0', '')
                salary = salary.replace(' ', '-')
                salary = salary.split('-')
                if salary[0] == 'от':
                    salary_min = int(salary[1])
                    salary_max = None
                elif salary[0] == 'до':
                    salary_min = None
                    salary_max = int(salary[1])
                else:
                    salary_min = int(salary[0])
                    salary_max = int(salary[1])
                salary_curr = salary[2]

            vacancy_data['name'] = name
            vacancy_data['link'] = link
            vacancy_data['company'] = company
            vacancy_data['company_link'] = link_c
            vacancy_data['city'] = city
            vacancy_data['city_zone1'] = city_zone1
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_curr'] = salary_curr

            vacancies.append(vacancy_data)
            num_steps += 1
        except TypeError:
            continue
    try:
        if soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}).text == 'дальше':
            next_link = soup.find('a', {'class': 'bloko-link bloko-link_secondary'})['href']
            response = requests.get(main_link + next_link, headers=headers)
            soup = bs(response.text, 'lxml')
            vacancies_block = soup.find('div', {'class': 'vacancy-serp'})
            try:
                vacancies_list = vacancies_block.findChildren(recursive=False)
            except AttributeError:
                continue
            continue
        else:
            break
    except AttributeError:
        break
pprint(vacancies)
print(f'Найдено {num_steps} вакансий')
