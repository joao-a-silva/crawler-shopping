import scrapy
import logging

class UOLSpyder(scrapy.Spider):
	name = "uol"
	allowed_domains = ["uol.com.br"]
	start_urls = [ "http://shopping.uol.com.br/celular-e-smartphone.html" ,]

	def parse(self, response):
		logging.info("Crawler Products List")
		for href in response.css("ul.offers-list__items > li > a::attr('href')"):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_dir_products)


	def parse_dir_products(self, response):		

		logging.info("\n\tCrawler Product %s", response.url.split("/")[-1])			
		for href in response.css("li.offers-list__item > a::attr('href')"):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_dir_product)


	def parse_dir_product(self, response):		
		logging.info("\n\t\t	Crawler Product")	
		yield
	

		     


