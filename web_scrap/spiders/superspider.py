import scrapy
from web_scrap.items import Machine
from datetime import datetime
from urllib.parse import urljoin


class MachinioSpider(scrapy.Spider):
    name = 'machinio'
    allowed_domains = ['machinio.com']
    start_urls = ['https://www.machinio.com']

    def parse(self, response):
        # Extract all main categories links from category-thumbnails
        for category in response.css("div.category-thumbnails > a"):
            yield response.follow(category, callback=self.parse_subcategories)
            print(category)

    def parse_subcategories(self, response):
        # Extract all subcategories links and add 50 pages to them
        for subcategory in response.css('ul.list-unstyled.list-underlined > li > a'):
            subcategory_url = subcategory.attrib['href']
            for page in range(1, 51):
                yield response.follow(f'{subcategory_url}?page={page}', callback=self.parse_listing_urls)
                print(response)

    def parse_listing_urls(self, response):
        # Extract all listing pages links from the subcategory pages
        for listing in response.css('li.c-card.c-card--link.c-listing-card > a'):
            yield response.follow(listing, callback=self.parse_listing)

    def parse_listing(self, response):
        try:
            name_list = response.xpath('//h1/text()').extract_first()
            image_links = response.css("li.current > img::attr(src)").extract_first()
            manufacturer = response.xpath('//dt[contains(text(),"Manufacturer")]/following-sibling::dd/a/text()').extract_first()
            model = response.xpath('//dt[contains(text(),"Model")]/following-sibling::dd/text()').extract_first(default='-')
            location = response.xpath('//dt[contains(text(),"Location")]/following-sibling::dd/text()').extract_first()
            year = response.xpath('//dt[contains(text(),"Year")]/following-sibling::dd/text()').extract_first(default='-')
            mileage = response.xpath('//dt[contains(text(),"Mileage")]/following-sibling::dd/text()').extract_first(default='-')
            machine_condition = response.xpath('//dt[contains(text(),"Condition")]/following-sibling::dd/text()').extract_first()
            price_list = response.xpath('//dt[contains(text(),"Price")]/following-sibling::dd/text()').extract_first()
            main_category = response.xpath('//*[@id="breadcrumb_1"]/a/text()').get()
            sub_category = response.xpath('//*[@id="breadcrumb_2"]/a/text()').get()
            url = response.url
            date_time = (str(datetime.now()))

            # Create an item with all the extracted information
            item = Machine()
            item['name'] = name_list
            item['image'] = image_links
            item['manufacturer'] = manufacturer
            item['model'] = model 
            item['location'] = location 
            item['year'] = year 
            item['mileage'] = mileage 
            item['machine_condition'] = machine_condition
            item['url'] = url
            item['created_at'] = date_time
            item['price'] = price_list
            item['main_category'] = main_category
            item['sub_category'] = sub_category

            yield item
            print(item)
        except Exception as e:
            self.logger.error("Error parsing listing: %s", e)

