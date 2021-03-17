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
        # breadcrumbs = response.xpath('//nav[@class="breadcrumbs-nav"]//a/@href').extract()
        # description = response.xpath('//div[contains(@class, "description")]').extract()

        items = response.xpath("//script[contains(., 'description')]/text()")
        txt = items.extract_first()
        start = txt.find('description') + 14
        finish = txt[start::].find('",')
        description = txt[start:start+finish]

        """"
        # mediamarkt
        # description = response.xpath('//div[@class="fg-box bpx0 bpy1 bsx3 bsy1 mpx0 mpy1 msx3 msy1 spx0 spy1 ssx3 ssy1"]').extract()
        description = response.xpath('//div[@class="product-details"]/p[last()]/text()').get()
        if not description:
            # bol.com
            # description = response.xpath('//div[@class="product-description"]').getall()
            description = response.xpath('//div[contains(@class, "description")]').extract()
            if not description:
                # coolblue.nl
                description = response.xpath('//div[@class="cms-content hide@md-down"]/p[last()]/text()').getall()
                if not description:
                    # wehkamp.nl
                    description = response.xpath("//script[contains(., 'description')]/text()").extract_first()
                    # description = response.xpath('/html//div/*[contains(@class, "description")]').extract()
        """
        product['url'] = url
        product['title'] = title
        product['description'] = description

        product_db = self.s.query(models.ProductPage).filter(models.ProductPage.url.ilike(url)).first()
        if not product_db:
            product_db = models.ProductPage(url=url, title=title, description=description)
            self.s.add(product_db)
        else:
            product_db.title = title
            self.s.add(product_db)

        self.s.commit()
        self.s.close()

        yield product
