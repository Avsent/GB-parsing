# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def process_price(value):
    try:
        value = int(value)
        return value
    except:
        return value


def specific_values(value):
    value = value.replace('\n', '').replace(' ', '')
    return value


class LmparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    priсe = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(process_price))
    specific = scrapy.Field()
    specific_values = scrapy.Field(input_processor=MapCompose(specific_values))
    parameter = scrapy.Field()
    _id = scrapy.Field()