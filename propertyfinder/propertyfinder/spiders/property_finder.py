import scrapy
import json



class PropertyFinder(scrapy.Spider):
    name = "prop"
    start_urls = ['https://www.onthemarket.com/property/#locations']

    handle_httpstatus_list = [403]

    headers = {
        'Referer': 'https://www.onthemarket.com/for-sale/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers, callback=self.parse)


    def parse(self, response):
        locations = response.css('.cjNmsL h4 a::attr(href)').extract()
        for location in locations:
            category = ['sale', 'rent']
            for cat in category:
                if cat == 'sale':
                    url = f'https://www.onthemarket.com/for-sale{location}?under-offer=true'

                elif cat == 'rent':
                    url = f'https://www.onthemarket.com/to-rent{location}?under-offer=true'

                yield scrapy.Request(url=url, headers=self.headers, callback=self.pagination)
    
    def pagination(self, response):
        total_pages = 0
        total_pages = response.css('#pagination-controls ul li:last-child a::text').get()
        if total_pages:
            total_pages = int(total_pages)
            if total_pages > 0:
                for page in range(1, total_pages+1):
                    url = response.url + f'&page={page}'
                    yield scrapy.Request(url=url, headers=self.headers, callback=self.list_page)


    def list_page(self, response):
        property_list = response.css('.otm-PropertyCardMedia div:nth-child(1) a::attr(href)').extract()
        for property in property_list:
            url = 'https://www.onthemarket.com'+property
            yield scrapy.Request(url=url, headers=self.headers, callback=self.detail_page)


    def detail_page(self, response):
        breakpoint()
        script_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        data = json.loads(script_data)
        print()