from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    breadcrumbs = Column(String)
    specifications = Column(String)

    def __repr__(self):
        return "<Product(title='{}', description='{}', breadcrumbs={}, specifications={})>" \
            .format(self.title, self.description, self.breadcrumbs, self.specifications)
