from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductPage(Base):
    __tablename__ = 'product_page'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    html = Column(String)
    ean = Column(String)
    product_text = Column(String)

    def __repr__(self):
        return "<ProductPage(url='{}', html='{}'," \
               " ean='{}', product_text='{}')>" \
            .format(self.url, self.html, self.ean, self.product_text)
