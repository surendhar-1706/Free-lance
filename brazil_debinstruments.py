import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
class BotSpider(scrapy.Spider):
    name = 'bot'
    driver = webdriver.Chrome() 
    all_code =[]
    all_holders = []
    all_sector = []
    all_numbers = []
    start_urls =['https://data.anbima.com.br/debentures?page=1&size=20&field=codigo_cetip&order=desc&']
    def parse(self,response):
        for i in range(5):
            urls = 'https://data.anbima.com.br/debentures?page='+str(i)+'&size=20&field=codigo_cetip&order=desc&'
            self.driver.get(urls)
            time.sleep(3)
            res = response.replace(body=self.driver.page_source)
            all = res.css('.debentures-list-item')
            for variable in all:
                code = variable.css('.debentures-list-item__title::text').extract_first()
                holder = variable.css('.col-md-5 .col-no-padding:nth-child(1) .anbima-ui-output__value--small::text').extract_first()
                sector = variable.css('.col-xs-hidden .anbima-ui-output__value--small::text').extract_first()
                some_weird_nuber = variable.css('.debentures-list-item__remuneracao .anbima-ui-output__value--small::text').extract_first()
                self.all_code.append(code)
                self.all_holders.append(holder)
                self.all_sector.append(sector)
                self.all_numbers.append(some_weird_nuber)                
            
        df = pd.DataFrame({
                'code':self.all_code,
                'holder':self.all_holders,
                'sector':self.all_sector,
                'number':self.all_numbers,
            })
        print(df)
        df.to_csv('final_items.csv')
        self.driver.quit()
