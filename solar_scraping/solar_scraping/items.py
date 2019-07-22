# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SolarScrapingItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	name = scrapy.Field()
	year_established = scrapy.Field()
	year_active = scrapy.Field()
	states_active = scrapy.Field()
	headquarters_street = scrapy.Field()
	headquarters_city = scrapy.Field()
	headquarters_state = scrapy.Field()
	headquarters_zip = scrapy.Field()
	headquarters_country = scrapy.Field()
	headquarters_link = scrapy.Field()
	systems_res = scrapy.Field()
	systems_com = scrapy.Field()
	office_latlongs = scrapy.Field()