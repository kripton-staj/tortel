from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class ProductBody(Base):
    __tablename__ = 'product_body'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    body = Column(String)

    def __repr__(self):
        return "<ProductBody(url='{}', body='{}')>" \
            .format(self.url, self.body)