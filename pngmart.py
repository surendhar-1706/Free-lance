import scrapy


class MartSpider(scrapy.Spider):
    name = 'mart'
    start_urls = ['http://www.pngmart.com']
    all_url=[]
    base_url = 'http://www.pngmart.com'
    def parse(self, response):
       image_response = response.css('.gallery-item')
       #for variables in image_response:
       image_url =image_response.css('a::attr(href)').extract_first()
       MartSpider.all_url.append(image_url)
       category_url = MartSpider.base_url + MartSpider.all_url[0]
       print(MartSpider.all_url)
       yield scrapy.Request(category_url,callback=self.parse_category)
    def parse_category(self, response):
      category_response =response.css('.tag-link-position-1')
      url_from_category = category_response.css('a::attr(href)').extract_first()
      print(url_from_category)
      yield scrapy.Request(url_from_category,callback=self.parse_last_tag)
    def parse_last_tag(self, response):
      tag_response = response.css('.wp-post-image')
      #print(tag_response)
      tag_image_link = tag_response.css('img::attr(src)').extract()
      print(tag_image_link)
      yield{
      'image_urls':tag_image_link
        } 
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
       
      
