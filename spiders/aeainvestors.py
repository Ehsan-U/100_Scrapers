import scrapy
from scrapy.selector import Selector
from urllib.parse import urljoin, urlparse
from scrapy_splash import SplashRequest

class AeainvestorsSpider(scrapy.Spider):
    name = 'aeainvestors'
    allowed_domains = ['aeainvestors.com']
    main = 'https://www.aeainvestors.com/portfolio/'
    def start_requests(self):
        with open('aeainvestors.csv','r') as f :
            comp_list = f.readlines()[1:]
        for company in comp_list:
            url = urljoin(base=self.main,url=company)
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        
        sel = Selector(text=response.body)
        try:
            title = urlparse(response.url).path[11:-1]
        except:
            title = ''
        try:
            year = sel.xpath("//div[@class='date cell shrink info']/text()").get()
        except:
            year = ''
        try:
            c_type = sel.xpath("//div[@class='industry cell shrink info']/text()").get()
        except:
            c_type = ''
        if ',' in c_type:
            c_types = c_type.split(',')
            c_type = ','.join([t.strip() for t in c_types])
        yield {'Company':title.strip(),'Year-Invested':year.strip(),'Type':c_type.strip()}
        # sel = Selector(text=response.text)
        # for url in sel.xpath("//a[@class='open-company open-company-modal']/@href").getall():
        #     yield {"aea":url}
