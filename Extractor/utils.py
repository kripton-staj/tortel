import config
import models
import extractor
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
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
        ean = value.ean
        title = extractor.extract_title(soup)
        description = extractor.extract_description(soup)
        breadcrumbs = extractor.extract_breadcrumbs(soup)
        specifications = extractor.extract_specifications(soup)

        product_data = s.query(models.ProductData).filter(models.ProductData.url.ilike(url)).first()
        if not product_data:
            product_data = models.ProductData(url=url, title=title, description=description,
                                              breadcrumbs=breadcrumbs, specifications=specifications, ean=ean)
            s.add(product_data)
        else:
            product_data.ean = ean
            product_data.title = title
            product_data.description = description
            product_data.breadcrumbs = breadcrumbs
            product_data.specifications = specifications

    s.commit()
    s.close()

    result = s.query(func.array_agg(models.ProductData.url),
                     func.count(models.ProductData.ean)).group_by(models.ProductData.ean).all()
    print(result)


# This function has been written to see how much data we can extract from the given url
def database_query():
    result = s.query(models.ProductData).all()
    a, b, c, d = 0, 0, 0, 0

    for row in result:
        if row.title:
            a += 1
        if row.description:
            b += 1
        if row.breadcrumbs:
            c += 1
        if row.specifications:
            d += 1
    print('There are %d line in database and found %d title data, %d description data,'
          ' %d breadcrumbs data, %d specifications data' % (len(result), a, b, c, d))


database_operations()
# database_query()
