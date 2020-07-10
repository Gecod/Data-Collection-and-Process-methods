# 3*)Написать функцию, которая будет добавлять в вашу базу данных только
# новые вакансии с сайта

from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacancies_db']

collection = db.vacancies_collection

vac_name = input('Введите наименование вакансии для поиска: ')
main_link = 'https://samara.hh.ru'

params = {'st': 'searchVacancy', 'text': vac_name, 'search_field': 'name', 'area': '1', 'only_with_salary': 'false',
          'order_by': 'publication_time', 'items_on_page': '100'}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/83.0.4103.97 Safari/537.36', 'Accept': '*/*'}

response = requests.get(main_link + '/search/vacancy', params=params, headers=headers)

soup = bs(response.text, 'lxml')

vacancies_block = soup.find('div', {'class': 'vacancy-serp'})

vacancies_list = vacancies_block.findChildren(recursive=False)

vacancies = []
num_steps = 0

while True:
    for vacancy in vacancies_list:
        vacancy_data = {}

        try:
            tag_link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})
            link = tag_link['href']
            name = tag_link.text

            _id = link.split('?')[0].split('/')[-1]
            # try:
            #     if _id == list(collection.find({'_id': str(_id)}))[0]['_id']:
            #         continue
            # except IndexError:
            #     continue

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

            vacancy_data['_id'] = _id
            vacancy_data['name'] = name
            vacancy_data['link'] = link
            vacancy_data['company'] = company
            vacancy_data['company_link'] = link_c
            vacancy_data['city'] = city
            # vacancy_data['city_zone1'] = city_zone1   починить, дает лишние данные 'Показать на карте'
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_curr'] = salary_curr

            try:
                if _id == list(collection.find({'_id': str(_id)}))[0]['_id']:
                    collection.update_one({'_id': str(_id)}, {'$set': vacancy_data})
                    continue
            except IndexError:
                vacancies.append(vacancy_data)
                collection.insert_one(vacancy_data)
                # continue

            # vacancies.append(vacancy_data)

            # collection.insert_one(vacancy_data)
            # pprint(vacancy_data)
            num_steps += 1
        except TypeError:
            continue
    try:
        if soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}).text == 'дальше':
            next_link = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})['href']
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

# pprint(vacancies)
print(f'Найдено {num_steps} новых вакансий на сайте {main_link}')

# with open('vacancies.json', 'w', encoding='utf-8') as f:
#     f.write(str(vacancies))

for vacancy in collection.find({}):
    pprint(vacancy)

print(f'Всего в базе данных {collection.count_documents({})} вакансий')

# collection.drop()
