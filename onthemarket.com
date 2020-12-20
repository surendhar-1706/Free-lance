import scrapy
from scrapy.http import request
import pandas as pd
import re
from ..items import OnthemarketItem
class MarketSpider(scrapy.Spider):
    name = 'market'
    headers = {
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    all_address =[]
    all_title =[]
    all_price =[]
    all_agent =[]
    all_phone =[]
    all_image_url =[]   
    
    
    url = 'https://www.onthemarket.com/for-sale/property/london/'
    scroll_url = ''
    base_url = 'https://www.onthemarket.com'
    next = []
    def start_requests(self):
        
        yield scrapy.Request(MarketSpider.url,headers = self.headers,callback=self.parse)
    def parse(self,response):
        items = OnthemarketItem()
        self.log('hey there this is the status '+str(response.status))
        address = response.css('.address a::text').extract()
        title = response.css('.title').css('a::text').extract()
        price = response.xpath("//meta[@itemprop='price']/@content").extract()
        description = response.css('.description::text').extract()
        agent = response.css('.marketed-by-link::text').extract()
        phone = response.css('.actions').css('.telephone').css('::text').extract()
        #img_link = response.xpath("//img[@type='image/jpeg']/@srcset").extract()
        #img_link = response.css('picture').css('img::attr(src)').getall() or None
        img_link = response.css('.media').css('img::attr(src)').extract()
        ''' yield {
            'title':title,
            'img_link':img_link
        } '''
        print(img_link)
        for variables in title:
            MarketSpider.all_title.append(variables)
        for variables in address:
            MarketSpider.all_address.append(variables)
        for variables in phone:
            MarketSpider.all_phone.append(variables)
        for variables in img_link:
            MarketSpider.all_image_url.append(variables)
        for variables in price:
            MarketSpider.all_price.append(variables)
        for variables in agent:
            MarketSpider.all_agent.append(variables)
        
        MarketSpider.next = response.css('a.arrow').css('::attr(href)').extract()
        for variables in MarketSpider.next:
            print('Here we print the next list fully',MarketSpider.next)
            MarketSpider.scroll_url = MarketSpider.base_url+ str(variables) 
            print('Here we are printing the scroll url',MarketSpider.scroll_url)
            
            if MarketSpider.next is not None:   
                yield scrapy.Request(MarketSpider.scroll_url,headers =self.headers,callback =self.parse)
            
        df = pd.DataFrame({
           
            'title':MarketSpider.all_title,
            'address':MarketSpider.all_address,
            'price':MarketSpider.all_price,
            'agent':MarketSpider.all_agent,
            'phone':MarketSpider.all_phone,
            'img_url':MarketSpider.all_image_url,
            
            })
        print(df) 
        df.to_csv('finalitem.csv')  
         
        
        
             
            
