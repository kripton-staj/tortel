import scrapy
import json
from ..items import ProductItem
import config
import models
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ProductSpider(scrapy.Spider):
    name = "product"

    engine = create_engine(config.DATABASE_URI)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    s = Session()

    def start_requests(self):
        with open("url_list.txt", "r") as f:
            urls = [line.rstrip() for line in f.readlines()]
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def extract_description(self, response):
        description = ""
        desc_data = response.xpath("//script[contains(., 'description')]/text()").extract()

        for data in desc_data:
            if not data:
                continue
            else:
                try:
                    data_dict = json.loads(data)
                    if data_dict['@type'] == 'Product':
                        description = data_dict['description']
                        break
                except KeyError as e:
                    print(e)
                    continue

        # TO DO : Clean data below with BeautifulSoup

        ext_array = ['//div[@class="fg-box bpx0 bpy1 bsx3 bsy1 mpx0 mpy1 msx3 msy1 spx0 spy1 ssx3 ssy1"]',
                     '//div[@class="product-description"]/p/text()', '//div[@class="product-description"]/text()',
                     '//div[@class="std product-description"]', '//div[@class="product attribute description"]//p',
                     '//div[@class="product-information__wrapper"]/p/text()', '//div[@class="product__description "]',
                     '//div[@class="description body-font-size"]/text()']

        if not description:
            for class_name in ext_array:
                description = response.xpath(class_name).extract()
                if description:
                    break

        return description

    def extract_breadcrumbs(self, response):    # WP
        breadcrumbs = []

        brd_array = ['//nav[@class="breadcrumbs-nav"]//a/@href', '//div[@class="fluid-grid__item fluid"]//a/@href',
                     '//nav//ol[@class="breadcrumbs"]//li//a/@href']

        for brd in brd_array:
            breadcrumbs = response.xpath(brd).extract()
            if breadcrumbs:
                break
        if not breadcrumbs:
            brd_data = response.xpath('//script[@type="application/ld+json"]//text()').extract_first()
            json_data = json.loads(brd_data)
            for i in range(len(json_data['itemListElement'])):
                breadcrumbs.append(json_data['itemListElement'][i]['item']['@id'])

        return breadcrumbs

    def parse(self, response):
        product = ProductItem()

        url = response.url
        title = response.xpath('//title/text()').get()
        description = self.extract_description(response)
        # breadcrumbs = self.extract_breadcrumbs(response)
        breadcrumbs = ""

        product['url'] = url
        product['title'] = title
        product['description'] = description
        product['breadcrumbs'] = breadcrumbs

        product_db = self.s.query(models.ProductPage).filter(models.ProductPage.url.ilike(url)).first()
        if not product_db:
            product_db = models.ProductPage(url=url, title=title, description=description, breadcrumbs=breadcrumbs)
            self.s.add(product_db)
        else:
            product_db.title = title
            product_db.description = description
            product_db.breadcrumbs = breadcrumbs
            self.s.add(product_db)

        self.s.commit()
        self.s.close()

        yield product
