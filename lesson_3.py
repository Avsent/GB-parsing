# 3.2. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

import json
from pymongo import MongoClient

# Произведен новый парсинг сайтов написанным на 2-м уроке парсером и результат сохранен в json.
# Функция сравнивает ранее добавленные в Mongodb вакансии с новыми из файла json.

client = MongoClient('localhost', 27017)['gb_3_mongo']
db = client['some_collection']
with open('pars_job.json', 'r', encoding='utf-8') as f:
    data_ = json.load(f)

counter = 0

for item in data_:
    # Поиск соответствующей вакансии по url
    test = db.find_one({'link': item['link']})

    if test is None:
        db.insert_one(item)
        counter += 1

print(f'Из {len(data_)} вакансий переданных в db_insert_vacancy()\n\t{counter} добавлено в базу данных'
        f'\n\t{len(data_) - counter} совпадают с имеющимися в базе данных')

# 3.3. Написать функцию, которая выводит на экран вакансии с заработной платой больше введённой суммы.

client = MongoClient('localhost', 27017)['gb_3_mongo']
db = client['some_collection']

salary_min = db.find({
    '$or': [{
    'salary_min': {'$gte': 100000},
    'salary_max': {'$gte': 100000} }]
})

for i in salary_min:
    print(i)