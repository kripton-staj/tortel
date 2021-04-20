import scrapy
import json
from ..items import SpiderItem
import tortel.spider.config as config
import tortel.spider.models as models
from tortel.spider.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Spider(scrapy.Spider):
    name = "spider"

    engine = create_engine(config.DATABASE_URI)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    s = Session()

    with open("results.json", "r") as f:
        url_and_ean = {}
        json_list = json.load(f)
        for url_name in json_list:
            url_and_ean[url_name['url']] = url_name['ean']
    print(url_and_ean)

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for key in list(self.url_and_ean.keys()):
            yield scrapy.Request(url=key, headers=headers, callback=self.parse)

    def parse(self, response):
        product = SpiderItem()
        url = response.url
        body = str(response.body)
        ean = self.url_and_ean[url]

        product_db = self.s.query(models.ProductBody).filter(models.ProductBody.url.ilike(url)).first()
        if not product_db:
            product_db = models.ProductBody(url=url, body=body, ean=ean)
            self.s.add(product_db)

        self.s.commit()
        self.s.close()

        yield product
