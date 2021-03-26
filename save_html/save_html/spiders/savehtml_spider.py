import scrapy
from ..items import SaveHtmlItem
import config
import models
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SaveHtmlSpider(scrapy.Spider):
    name = "savehtml"

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

    def parse(self, response):
        product = SaveHtmlItem()
        url = response.url
        body = response.body
        # print(body)

        product_db = models.ProductBody(url=url, body=body)
        self.s.add(product_db)
        self.s.commit()
        self.s.close()

        # data.body returns hexadecimal
        db_data = self.s.query(models.ProductBody)
        for data in db_data:
            print("*******", data.body)

        yield product
