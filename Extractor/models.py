from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TEXT

Base = declarative_base()


class ProductBody(Base):
    __tablename__ = 'product_body'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    body = Column(String)

    def __repr__(self):
        return "<ProductBody(url='{}', body='{}')>" \
            .format(self.url, self.body)


class ProductData(Base):
    __tablename__ = 'product_data'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    description = Column(TEXT)
    breadcrumbs = Column(String)
    specifications = Column(String)

    def __repr__(self):
        return "<ProductPage(url='{}', title='{}', description='{}', breadcrumbs={}, specifications={})>" \
            .format(self.url, self.title, self.description, self.breadcrumbs, self.specifications)