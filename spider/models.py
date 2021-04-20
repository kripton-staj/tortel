from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductBody(Base):
    __tablename__ = 'product_body'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    body = Column(String)
    ean = Column(String)

    def __repr__(self):
        return "<ProductBody(url='{}', body='{}', ean='{}')>" \
            .format(self.url, self.body, self.ean)
