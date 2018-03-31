# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GanjiscrapyItem(scrapy.Item):
    # print(price + "##", im, "##" + title + "##" + dress + "##", hre)
    hre=scrapy.Field()
    title=scrapy.Field()
    im=scrapy.Field()
    dress=scrapy.Field()
    price=scrapy.Field()
    dirname=scrapy.Field()
    filename=scrapy.Field()
    carage=scrapy.Field()
    storename=scrapy.Field()
    info=scrapy.Field()
    phone=scrapy.Field()
    company=scrapy.Field()
    datatime=scrapy.Field()
    pass
