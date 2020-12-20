import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://www.youtube.com/c/ZHcomicart/videos']
    base_url = 'https://www.youtube.com'
    driver = webdriver.Chrome()  
    updated_link =[]
    def parse(self,response):
        urls = 'https://www.youtube.com/c/ZHcomicart/videos'
        self.driver.get(urls) 
        for variables in range(5):
            self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(3)
        #self.driver.get(response.url)
        print(response.url,'\n')
        res = response.replace(body=self.driver.page_source)
        video_title = res.css('#video-title::text').extract()
        self.driver.quit()
        video_link = res.css('#video-title::attr(href)').extract()
        for variables in video_link:
            self.updated_link.append(self.base_url+variables)
        video_views = res.css('#metadata-line .ytd-grid-video-renderer:nth-child(1)').css('::text').extract()
        print(video_views,self.updated_link)
        df = pd.DataFrame({
            'title': video_title,
            'video_link':self.updated_link,
            'views': video_views
        })
        print(df)
        df.to_csv('final_items.csv')
