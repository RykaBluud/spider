# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebScrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

from scrapy.item import Item, Field

class Machine(Item):
    name = Field()
    image = Field()
    manufacturer = Field()
    model = Field()
    location = Field()
    year = Field()
    mileage = Field()
    machine_condition = Field()
    created_at = Field()
    url = Field()
    price = Field()
    main_category = Field()
    sub_category = Field()
