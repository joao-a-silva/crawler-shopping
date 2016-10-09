import scrapy
import logging
	#from items import CrawlershoppingItem


class UOLSpyder(scrapy.Spider):

	name = "uol"
	allowed_domains = ["uol.com.br"]
	start_urls = [ "http://shopping.uol.com.br/livros.html",				


	]
	download_delay = 2    # 1s of delay
	
	def parse(self, response):
		logging.info("Crawler Products List")
		for li in response.css("ul.offers-list__items > li "):
		#	print(li)			
			entity = li.css("::attr('data-id')").extract()
			print(entity)
			href = li.css("a::attr('href')")
		#	print(len(href))
			
			if len(href) > 1:
				url = response.urljoin(href[0].extract())			
		#		print(url)
				yield scrapy.Request(url,  meta={'entityLabel': entity}, callback=self.parse_dir_products)
		
		next_page = response.css("ul.pagination__list > li > a::attr('href') ")
	#	print("Next page", next_page)
	#	print(len(next_page))
		if len(next_page) > 1:
			url = response.urljoin(next_page[len(next_page)-1].extract())
	#		print("Next page url:", url)
			yield scrapy.Request(url, callback=self.parse)
#body > main > div > div.small-12.large-9.columns > div > div.offers-list__container > ul > li:nth-child(1) > a
#/html/body/main/div/div[3]/div/div[1]/ul/li[1]/a

	def parse_dir_products(self, response):	
		#print(response.meta['entityLabel'])	        
		f = open('books', 'a')
		logging.info("\n\tCrawler Product %s", response.url.split("/")[-1])			

		for sel in response.xpath('/html/body/main/div/div/section[3]/div/div/div[1]/div/ul/li'):			
		    #print("\n\n\t\tProduct: ", sel)
#			print("")
			logging.info("\tExtracting Product" )
			offerId = sel.css("li::attr('data-id')").extract()
			logging.info("\tEntity id: %s",response.meta['entityLabel'])
			logging.info("\tOffer id: %s",offerId)

			if len(offerId) > 0:
				description = sel.css("li>div>a::text").extract()
				logging.info("\tEntity description: %s", description[0])							
				f.write(response.meta['entityLabel'][0].encode('utf-8')+"; "+str(offerId[0])+"; "+ description[0].encode('utf-8')+"\n")			
				print("\n")
		print("********************************************************************************************************")

		f.close()
		next_page = response.css("ul.pagination__list > li > a::attr('href') ")
	#	print("Next product url", next_page)
	#	print(len(next_page))
		if len(next_page) > 1:
			urlNext = response.urljoin(next_page[len(next_page)-1].extract())
		#	print("Next product page url:", urlNext)
			yield scrapy.Request(urlNext, meta={'entityLabel': response.meta['entityLabel']}, callback=self.parse_dir_products)


