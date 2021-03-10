import scrapy
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
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        product = ProductItem()

        url = response.url
        title = response.xpath('//title/text()').get()
        description = response.xpath('//div[@class="product-details"]/p[last()]/text()').get()
        breadcrumbs = response.xpath('//nav[@class="breadcrumbs-nav"]//a/@href').extract()

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
            self.s.add(product_db)

        self.s.commit()
        self.s.close()

        yield product
