from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy1204

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            if item['salary']:
                salary = item['salary']
                item['salary'] = {}
                if salary[0] == 'з/п не указана':
                    item['salary'] = {'min': 'з/п не указана'}
                elif salary[0] == 'от ':
                    item['salary']['currency'] = salary[-2]
                    item['salary']['taxes'] = salary[-1]
                    item['salary']['min'] = int(salary[1].replace('\xa0', ''))
                    if salary[2] == ' ':
                        item['salary']['max'] = None
                    else:
                        item['salary']['max'] = int(salary[3].replace('\xa0', ''))
                elif salary[0] == 'до ':
                    item['salary']['currency'] = salary[-2]
                    item['salary']['taxes'] = salary[-1]
                    item['salary']['min'] = None
                    item['salary']['max'] = int(salary[1].replace('\xa0', ''))
        elif spider.name == 'sjru':
            if item['salary']:
                salary = item['salary']
                item['salary'] = {}
                if salary[0] == 'По договорённости':
                    item['salary'] = {'min': 'По договорённости'}
                elif salary[0] == 'от':
                    item['salary']['currency'] = salary[2].split('\xa0')[-1]
                    item['salary']['period'] = salary[-1]
                    item['salary']['min'] = int(''.join(salary[2].split('\xa0')[:2]))
                    item['salary']['max'] = None
                elif salary[0] == 'до':
                    item['salary']['currency'] = salary[2].split('\xa0')[-1]
                    item['salary']['period'] = salary[-1]
                    item['salary']['min'] = None
                    item['salary']['max'] = int(''.join(salary[2].split('\xa0')[:2]))
                else:
                    item['salary']['currency'] = salary[-3]
                    item['salary']['period'] = salary[-1]
                    item['salary']['min'] = int(''.join(salary[0].split('\xa0')))
                    if salary[2] == '-':
                        item['salary']['max'] = int(''.join(salary[4].split('\xa0')))
                    else:
                        item['salary']['max'] = None

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item
