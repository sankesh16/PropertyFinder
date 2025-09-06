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
            category = ['rent','sale']
            for cat in category:
                if cat == 'sale':
                    url = f'https://www.onthemarket.com/for-sale{location}?under-offer=true'

                elif cat == 'rent':
                    url = f'https://www.onthemarket.com/to-rent{location}?under-offer=true'

                yield scrapy.Request(url=url, meta={'category':cat,'location':location.replace('/property','').replace('/','').title()}, headers=self.headers, callback=self.pagination)
    
    def pagination(self, response):
        location = response.meta['location']
        category = response.meta['category']
        total_pages = 0
        total_pages = response.css('#pagination-controls ul li:last-child a::text').get()
        if total_pages:
            total_pages = int(total_pages)
            if total_pages > 0:
                for page in range(1, total_pages+1):
                    url = response.url + f'&page={page}'
                    yield scrapy.Request(url=url, meta={'category':category,'location':location}, headers=self.headers, callback=self.list_page)


    def list_page(self, response):
        location = response.meta['location']
        category = response.meta['category']
        property_list = response.css('.otm-PropertyCardMedia div:nth-child(1) a::attr(href)').extract()
        for property in property_list:
            url = 'https://www.onthemarket.com'+property
            yield scrapy.Request(url=url, meta={'category':category,'location':location}, headers=self.headers, callback=self.detail_page)


    def detail_page(self, response):
        location = response.meta['location']
        category = response.meta['category']

        property_data = {
            "property_description": None,
            "labelText": None,
            "property_type": None,
            "bedroom": None,
            "bathroom": None,
            "address": None,
            "price": None,
            "property_title": None,
            "property_id": None,
            "lat": None,
            "long": None,
            "property_sub_type": None,
            "epc_rating": None,
            "property_features": None,
            "property_rooms": None,
            "property_date": None,
            "property_url": None,
            "property_image": None,
            "property_location": None,
            "property_category": None,
            "agent_name": None,
            "agent_telephone": None,
            "agent_logo": None
        }

        script_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        data = json.loads(script_data)

        property_data['property_description'] =  data['props']['initialReduxState']['property']['description']
        
        if 'labelText' in data['props']['initialReduxState']['property']:
            property_data['labelText'] = data['props']['initialReduxState']['property']['labelText']

        property_data['property_type'] = data['props']['initialReduxState']['property']['humanisedPropertyType']
        property_data['bedroom'] = data['props']['initialReduxState']['property']['bedrooms']
        property_data['bathroom'] = data['props']['initialReduxState']['property']['bathrooms']
        property_data['address'] = data['props']['initialReduxState']['property']['displayAddress']
        property_data['price'] = data['props']['initialReduxState']['property']['priceRaw']
        property_data['property_title'] = data['props']['initialReduxState']['property']['propertyTitle']
        property_data['property_id'] = data['props']['initialReduxState']['property']['id']
        property_data['lat'] = data['props']['initialReduxState']['property']['location']['lat']
        property_data['long'] = data['props']['initialReduxState']['property']['location']['lon']
        property_data['property_sub_type'] = data['props']['initialReduxState']['property']['propSubId']

        if 'epc' in data['props']['initialReduxState']['property']:
            if 'rating' in data['props']['initialReduxState']['property']['epc']:
                property_data['epc_rating'] = data['props']['initialReduxState']['property']['epc']['rating']
                
        property_data['property_features'] = [k['feature'] for k in data['props']['initialReduxState']['property']['features']]
        
        property_rooms = {k['name']:k['sizeText'] for k in data['props']['initialReduxState']['property']['rooms']['descriptions']}
        if property_rooms:
            property_data['property_rooms'] = property_rooms

        property_data['property_date'] = data['props']['initialReduxState']['property']['daysSinceAddedReduced']
        property_data['property_url'] = response.url
        property_data['property_image'] = [image['largeUrl'] for image in data['props']['initialReduxState']['property']['images']]
        property_data['property_location'] = location
        property_data['property_category'] = category

        property_data['agent_name'] = data['props']['initialReduxState']['agent']['name']
        property_data['agent_telephone'] = data['props']['initialReduxState']['agent']['telephone']
        property_data['agent_logo'] = "https://media.onthemarket.com" + data['props']['initialReduxState']['agent']['displayLogo']['url']

        yield property_data

