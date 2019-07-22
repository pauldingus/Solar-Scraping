from scrapy import Spider, Request
from solar_scraping.items import SolarScrapingItem
from scrapy.shell import inspect_response
import re

class solar_spider(Spider):
	name = 'solar_spider'
	allowed_urls = ['https://www.energysage.com/']
	start_urls = ['https://www.energysage.com/supplier/search?selected_facets=technology_types:Solar%20PV&selected_facets=services:installers&page=1']

	def parse(self, response):
		print("=====> Start data extract ....")
		print("="*500)
		num_pages = int(response.xpath('//*[@id="search-results2"]/div[3]/div[2]/div[2]/ul/li[7]/a/text()').extract_first())
		
		urls = []
		for i in range(1,num_pages+1):
			urls = urls + ['https://www.energysage.com/supplier/search?selected_facets=technology_types:Solar%20PV&selected_facets=services:installers&page={}'.format(i)]

		for url in urls:
			print("Going to {}".format(url))
			yield Request(url = url, callback = self.parse_list_page)

	def parse_list_page(self, response):
		#parse page with list of companies

		#get list of urls of the company profiles
		profile_links = response.xpath('//*[@id="search-results2"]//a[@class="supplier-name"]/@href').extract()
		profile_links = ['https://www.energysage.com' + x for x in profile_links]
		
		for url in profile_links:
			print("Going to {}".format(url))
			yield Request(url = url, callback = self.parse_profile_page)

	def parse_profile_page(self, response):

		item = SolarScrapingItem()

		name = response.xpath('//span[@itemprop="name"]/text()').extract_first()

		try:
			year_established = int(response.xpath('//div[@itemprop="foundingDate"]/text()').extract_first())
		except:
			year_established = ''

		try:
			year_active = int(response.xpath('//div[@class="collapse-content"]//div[h4[.="Installing Solar PV since"]]/div[@class="value"]/text()').extract_first())
		except:
			year_active = ''

		try:
			states_active = response.xpath('//div[@class="collapse-content"]//div[@class = "module" and h4[.="Areas of Service"]]/div[1]/text()').extract()
			states_active = '|'.join(re.findall(r'\w\w',states_active[0]))
		except:
			states_active = ''
			# inspect_response(response, self)

		try:
			headquarters = response.xpath('//div[@class="collapse-content"]//div[h4[.="Headquarters"]]/div[@itemprop="address"]/div[@class="colB"]').extract()
			headquarters = re.sub('\n','',headquarters[0])
			headquarters = re.search(r'(\d+[^<]+).+Locality">([^<]+).+Region">([^<]+).+Code">(\d{5}).+Country">([^<]+)',headquarters)
			headquarters_street = headquarters.groups()[0]
			headquarters_city = headquarters.groups()[1]
			headquarters_state = headquarters.groups()[2]
			headquarters_zip = ',' + headquarters.groups()[3]
			headquarters_country = headquarters.groups()[4]
		
		except:
			headquarters_street = ''
			headquarters_city = ''
			headquarters_state = ''
			headquarters_zip = ''
			headquarters_country = ''

		try:
			headquarters_link = response.xpath('//div[@class="collapse-content"]//div[h4[.="Headquarters"]]/div[@itemprop="address"]/div[@class="colA"]/a/@href').extract()[0]
		except:
			headquarters_link = ''

		try:
			systems_res = response.xpath('//div[h4[.="Number of Solar PV systems installed"]]//p[starts-with(text(), " Residential")]/span/text()').extract()
			systems_res = int(re.sub(',','',systems_res[0]))
		except:
			systems_res = ''

		try:
			systems_com = response.xpath('//div[h4[.="Number of Solar PV systems installed"]]//p[starts-with(text(), " Commercial")]/span/text()').extract()
			systems_com = int(re.sub(',','',systems_com[0]))
		except:
			systems_com = ''

		try:
			offices = response.xpath('//div[@class="branch_list"]/div[@class="branch_container " or @class="branch_container lo_hidden"]')
			lats = [office.attrib['data-lat'] for office in list(offices)]
			longs = [office.attrib['data-lon'] for office in list(offices)]
			office_latlongs = [','.join(t) for t in list(zip(lats,longs))]
			office_latlongs = '|'.join(office_latlongs)
		except:
			office_latlongs = ''

		item['name'] = name
		item['year_established'] = year_established
		item['year_active'] = year_active
		item['states_active'] = states_active
		item['headquarters_street'] = headquarters_street
		item['headquarters_city'] = headquarters_city
		item['headquarters_state'] = headquarters_state
		item['headquarters_zip'] = headquarters_zip
		item['headquarters_country'] = headquarters_country
		item['headquarters_link'] = headquarters_link
		item['systems_res'] = systems_res
		item['systems_com'] = systems_com
		item['office_latlongs'] = office_latlongs

		print(item)
		yield item
		