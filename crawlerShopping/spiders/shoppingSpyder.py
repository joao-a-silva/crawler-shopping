import scrapy
import logging
#from items import CrawlershoppingItem


class UOLSpyder(scrapy.Spider):

	name = "uol"
	allowed_domains = ["uol.com.br"]
	start_urls = [ "http://shopping.uol.com.br/celular-e-smartphone.html", 
			"http://shopping.uol.com.br/tv.html" ,
	                "http://shopping.uol.com.br/notebook.html",
			"http://shopping.uol.com.br/tablet.html",
			"http://shopping.uol.com.br/impressora.html",
			"http://shopping.uol.com.br/fone-de-ouvido-headset.html",
			"http://shopping.uol.com.br/aparelho-de-telefone.html", 
			"http://shopping.uol.com.br/carregador-para-celular-e-smartphone.html",
			"http://shopping.uol.com.br/geladeira-refrigerador.html",
			"http://shopping.uol.com.br/fogao.html",
			"http://shopping.uol.com.br/maquina-de-lavar-roupas.html",
			"http://shopping.uol.com.br/microondas.html",
			


	]
	DOWNLOAD_DELAY = 1    # 1s of delay
	
	def parse(self, response):
		logging.info("Crawler Products List")
		for href in response.css("ul.offers-list__items > li > a::attr('href')"):
			url = response.urljoin(href.extract())
		        print(url)
			yield scrapy.Request(url, callback=self.parse_dir_products)
		
		next_page = response.css("ul.pagination__list > li > a::attr('href') ")
#		print("Next page", next_page)
#		print(len(next_page))
  		if next_page:
			url = response.urljoin(next_page[len(next_page)-1].extract())
			#print("Next page url:", url)
		        yield scrapy.Request(url, callback=self.parse)



	def parse_dir_products(self, response):		        
		f = open('cells', 'a')
		logging.info("\n\tCrawler Product %s", response.url.split("/")[-1])			

		for sel in response.xpath('/html/body/main/div/div/section[3]/div/div/div[1]/div/ul/li'):
			
#			print("")
	                print("\n\n\t\tProduct: ", sel )
#			print("")
			logging.info("\n\tExtracting Product" )
			offerId = sel.css("li::attr('data-id')").extract()
			print("Offer id: ", offerId)
			if len(offerId) > 0:
				description = sel.css("li>div>a::text").extract()
				print("Product Description: ", description[0])							
				f.write(str(offerId[0])+"; "+ description[0].encode('utf-8')+"\n")
				print()
		f.close()
		next_page = response.css("ul.pagination__list > li > a::attr('href') ")
#		print("Next page", next_page)
#		print(len(next_page))
  		if next_page:
			url = response.urljoin(next_page[len(next_page)-1].extract())
#			print("Next page url:", url)
	                yield scrapy.Request(url, callback=self.parse_dir_products)


