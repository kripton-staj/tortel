import config
import models
import extracter
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup


engine = create_engine(config.DATABASE_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()


def database_operations():
    product_body = s.query(models.ProductBody)

    for value in product_body:
        soup = BeautifulSoup(value.body, "lxml")
        url = value.url
        title = extracter.extract_title(soup)
        description = extracter.extract_description(soup)
        breadcrumbs = extracter.extract_breadcrumbs(soup)
        specifications = extracter.extract_specifications(soup)

        product_data = s.query(models.ProductData).filter(models.ProductData.url.ilike(url)).first()
        if not product_data:
            product_data = models.ProductData(url=url, title=title, description=description,
                                              breadcrumbs=breadcrumbs, specifications=specifications)
            s.add(product_data)
        else:
            product_data.title = title
            product_data.description = description
            product_data.breadcrumbs = breadcrumbs
            product_data.specifications = specifications

    s.commit()
    s.close()


database_operations()
