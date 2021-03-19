import scrapy
from ..items import ProductItem
import config
import models
import json
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
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def extract_description(self, response):
        description = ""
        for i in range(5):
            desc_data = response.xpath("//script[$num][contains(., 'description')]/text()", num=i).extract_first()
            if not desc_data:
                continue
            else:
                try:
                    if json.loads(desc_data)['@type'] == 'Product':
                        description = json.loads(desc_data)['description']
                        break
                except:
                    print("Json doesnt contain a type")
                    continue

        # TO DO : Clean data below with BeautifulSoup

        ext_array = ['//div[@class="fg-box bpx0 bpy1 bsx3 bsy1 mpx0 mpy1 msx3 msy1 spx0 spy1 ssx3 ssy1"]',
                     '//div[@class="product-description"]/p/text()', '//div[@class="product-description"]/text()']

        if not description:
            for class_name in ext_array:
                description = response.xpath(class_name).extract()
                if description:
                    break

        return description

    def parse(self, response):
        product = ProductItem()

        url = response.url
        title = response.xpath('//title/text()').get()
        # breadcrumbs = response.xpath('//nav[@class="breadcrumbs-nav"]//a/@href').extract()
        description = self.extract_description(response)

        product['url'] = url
        product['title'] = title
        product['description'] = description

        product_db = self.s.query(models.ProductPage).filter(models.ProductPage.url.ilike(url)).first()
        if not product_db:
            product_db = models.ProductPage(url=url, title=title, description=description)
            self.s.add(product_db)
        else:
            product_db.title = title
            product_db.description = description
            self.s.add(product_db)

        self.s.commit()
        self.s.close()

        yield product
