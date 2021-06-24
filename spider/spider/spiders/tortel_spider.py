import scrapy
from common.config import DATABASE_URI
from common.models import Base, ProductPage
from spider.items import SpiderItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Spider(scrapy.Spider):
    name = "tortel_spider"

    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    s = Session()

    def get_urls_for_requests(self):
        """
        Read url names from the database. If the html column in the row
         where the url is located is empty, this means url has not been
          scraped before.(Or couldn't successfully scraped.)
          Creating url_list array and append urls which haven't scraped.
        :return: url_list:
        :rtype: <class 'list'>
        """
        product_page = self.s.query(ProductPage)
        url_list = []
        for row in product_page:
            if not row.html:
                url_list.append(row.url)
        return url_list

    def start_requests(self):
        url_list = self.get_urls_for_requests()
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0)'
                                 ' Gecko/20100101 Firefox/48.0'}
        for url in url_list:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        product = SpiderItem()
        url = response.url
        html = str(response.body)

        product_page = self.s.query(ProductPage).filter_by(url=url).first()
        if product_page:
            product_page.html = html
            self.s.add(product_page)
        self.s.commit()
        self.s.close()

        yield product
