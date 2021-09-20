# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['vac_job']

    def process_item(self, item, spider):

        if spider.name == 'hhru':
            salary = item['salary_min'].replace('\xa0', '').replace('\u202f', '')
            salary_max, salary_min, currency = None, None, None
            if 'до' in salary and 'от' in salary:
                salary_min = int(salary.split(' ')[1])
                salary_max = int(salary.split(' ')[3])
                currency = salary.split(' ')[-1]
            elif 'от' in salary:
                salary_min = int(salary.split(' ')[1])
                currency = salary.split(' ')[-1]
            elif 'до' in salary:
                salary_max = int(salary.split(' ')[1])
                currency = salary.split(' ')[-1]
            item['salary_min'] = salary_min
            item['salary_max'] = salary_max
            item['currency'] = currency

        elif spider.name == 'sjru':
            salary = item['salary_min']
            salary_split = salary[-1].split('\xa0')

            if salary[0] == 'По договорённости':
                salary_min, salary_max, currency = None, None, None
            elif salary[0] == 'до':
                salary_min = None
                currency = salary_split.pop()
                salary_max = float(''.join(salary_split))

            elif salary[0] == 'от':
                currency = salary_split.pop()
                salary_min = float(''.join(salary_split))
                salary_max = None
            else:
                currency = salary.pop()
                salary_min = float(''.join(salary[0].split('\xa0')))
                try:
                    salary_max = float(''.join(salary[1].split('\xa0')))
                except (ValueError, IndexError):
                    salary_max = salary_min

            item['salary_min'] = salary_min
            item['salary_max'] = salary_max
            item['currency'] = currency

        collection = self.mongo_base[spider.name]
        if collection.count_documents({}):
            collection.update_one(
                {'url': item['url']},
                {'$set': item},
                upsert=True
            )
        else:
            collection.insert_one(item)

        return item