from urllib.parse import urljoin, urlparse
import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

class TestSpider(scrapy.Spider):
    name = 'accel'
    allowed_domains = ['accel-kkr.com']
    main = 'https://www.accel-kkr.com'
    
    def start_requests(self):
        with open('accel.csv','r') as f :
            comp_list = f.readlines()
        for company in comp_list:
            url = urljoin(base=self.main,url=company)
            yield SplashRequest(url=url,callback=self.parse)

    def parse(self,response):
        sel = Selector(text=response.body)
        try:
            title = sel.xpath("//h2[@class='elementor-heading-title elementor-size-default']/text()").get()
        except:
            title = ''
        try:
            year = sel.xpath("//span[@class='elementor-heading-title elementor-size-default']/text()").getall()[1]
        except:
            year = ''
        try:
            c_type = ','.join(sel.xpath("//h5[@class='terms-list']/span/text()").getall())
        except:
            c_type = ''

        yield {'Company':title,'Year-Invested':year,'Type':c_type}
        
        # for compny in sel.xpath("//div[@class='esg-cc eec']/div/a/@href").getall():
        #     print(compny,'a')
        #     yield {'accel':compny}
