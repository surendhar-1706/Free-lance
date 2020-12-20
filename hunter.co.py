import scrapy
from scrapy.http import headers
import pandas as pd
class JobSpider(scrapy.Spider):
    name = 'job'
    page_number = 2
    check_id=[]
    all_post_date=[]
    all_employer=[]
    all_country=[]
    all_address=[]
    headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
    'Sec-GPC': '1',
    'Origin': 'https://huntr.co',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://huntr.co/',
    'Accept-Language': 'en-US,en;q=0.9',
     }
    first_list=[]
    def start_requests(self):
        url_one = 'https://app.huntr.co/public/search/job-posts?page=1&bounds=%7B%22minLat%22:-77.84475133044103,%22minLng%22:-171.75834117212722,%22maxLat%22:76.57722006773034,%22maxLng%22:177.41667004988918%7D&zoom=1'
        yield scrapy.Request(url_one,callback=self.parse,headers=self.headers)
    def parse(self, response):
        base_url ='https://app.huntr.co/public/search/job-posts?page='+str(JobSpider.page_number)+'&bounds={"minLat":-77.84475133044103,"minLng":-171.75834117212722,"maxLat":76.57722006773034,"maxLng":177.41667004988918}&zoom=1'
        json_data = response.json()
        print(json_data.keys())
        
        for variables in json_data['results']:
            id = variables['_id']
            employer = variables['_employer']
            original_post_date = variables['postDate']
            #print('check',variables.keys())
           
            list2 = variables['places']
            #print('check_list 2',list2)
            list3 = list2[0]
            #print('check_list 3',list3.keys())
            country = list3['country']
            address = list3['address']
            if address:
                JobSpider.all_address.append(address)
            else:
               JobSpider. all_address.append(None) 
            if employer:
                  JobSpider.all_employer.append(employer)
            else:
               JobSpider.all_employer.append(None)
            if country:
                JobSpider.all_country.append(country)
            else:
                JobSpider.all_country.append(None)
            if original_post_date:
               JobSpider.all_post_date.append(original_post_date)
            else:
               JobSpider.all_post_date.append(None)
            if id:
              JobSpider.check_id.append(id)
            else:
               JobSpider.check_id.append(None)
            
        for i in range(3):
                JobSpider.page_number = JobSpider.page_number+1
                print(JobSpider.page_number)
                yield scrapy.Request(base_url,callback = self.parse,headers = self.headers)
                
        df = pd.DataFrame({
                'id':JobSpider.check_id,
                'post data':JobSpider.all_post_date,
                'country':JobSpider.all_country,
                'employer_id':JobSpider.all_employer,
                'address':JobSpider.all_address
            })
        print(df)
        df.to_csv('final_item.csv')
