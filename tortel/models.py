from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product_page'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    ean = Column(String)
    title = Column(String)
    description = Column(String)
    breadcrumbs = Column(String)
    specifications = Column(String)

    def __repr__(self):
        return "<Product(url='{}', ean='{}', title='{}', description='{}', breadcrumbs={}, specifications={})>" \
            .format(self.url, self.ean, self.title, self.description, self.breadcrumbs, self.specifications)
