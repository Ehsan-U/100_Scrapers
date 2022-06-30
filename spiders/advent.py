import scrapy
from scrapy.selector import Selector

class AdventSpider(scrapy.Spider):
    name = 'advent'
    allowed_domains = ['adventinternational.com']
    start_urls = ['https://www.adventinternational.com/investments/']

    def parse(self, response):
        sel = Selector(text=response.text)
        for c_name,c_year,c_type in zip(sel.xpath("//td[@class='company-name']"),sel.xpath("//td[@class='type']/span[2]/text()").getall(),sel.xpath("//td[@class='date']/span[2]/text()").getall()):
            if c_name.xpath("./a/text()").get():
                c_name = c_name.xpath("./a/text()").get()
            else:
                c_name = c_name.xpath("./text()").get()
            yield {'Company':c_name.strip(),'Year-Invested':c_year.strip(),'Type':c_type.strip()}