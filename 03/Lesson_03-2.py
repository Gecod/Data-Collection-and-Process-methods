# 2) Написать функцию, которая производит поиск и выводит на экран
# вакансии с заработной платой больше введенной суммы

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacancies_db']
collection = db.vacancies_collection

min_salary = float(input('Укажите минимальную зарплату: '))

num = 0

for vacancy in collection.find({'$or': [{'salary_max': {'$gte': min_salary}}, {'salary_min': {'$gte': min_salary}}]}).sort([('salary_max', -1), ('salary_min', -1)]):
    num += 1
    pprint(vacancy)

print(f'Найдено {num} вакансий с зарплатой от {min_salary}')
print(f'Всего в базе данных {collection.count_documents({})} вакансий')
