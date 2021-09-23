import requests
from lxml import html
from pprint import pprint

url = 'https://lenta.ru/'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36'
}

response = requests.get(url, headers=header)

dom = html.fromstring(response.text)
items = dom.xpath('//section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"]/a')

news = []
for i in items:
    news_ = {}
    site = 'https://lenta.ru/'
    name = i.xpath('./text()')
    link = i.xpath('./@href')
    date = i.xpath('.//time/@title')

    news.append({
        'site': site,
        'name': name[0].replace('\xa0', ' '),
        'link': link[0] if 'http' in link[0] else url + link[0],
        'date': date[0]
        })

pprint(news)
