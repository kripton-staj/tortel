import tortel.extractor.extractor as extractor
import tortel.extractor.models as models
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from tortel.extractor.config import DATABASE_URI
from tortel.extractor.models import Base

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()


def write_extracted_data():
    """
    Calls extractor.py and writes extracted data
     to product_data table in the database.
    :input: None
    :return: None
    """
    product_body = s.query(models.ProductBody)
    for value in product_body:
        soup = BeautifulSoup(value.body, "lxml")
        url = value.url
        ean = value.ean
        title = extractor.extract_title(soup)
        description = extractor.extract_description(soup)
        breadcrumbs = extractor.extract_breadcrumbs(soup)
        specifications = extractor.extract_specifications(soup)
        all_data = str(title) + " " + str(description) + " " + str(
            breadcrumbs) + " " + str(specifications)

        product_data = s.query(models.ProductData). \
            filter(models.ProductData.url.ilike(url)).first()
        if not product_data:
            product_data = models.ProductData(url=url, title=title,
                                              description=description,
                                              breadcrumbs=breadcrumbs,
                                              specifications=specifications,
                                              ean=ean, all_data=all_data)
            s.add(product_data)
        else:
            product_data.ean = ean
            product_data.title = title
            product_data.description = description
            product_data.breadcrumbs = breadcrumbs
            product_data.specifications = specifications
            product_data.all_data = str(title) + " " + str(
                description) + " " + str(
                breadcrumbs) + " " + str(specifications)

    s.commit()
    s.close()


def print_report():
    """
    This function has been written to see
     how much data we can extract from the given url.
    :input: None
    :return: None
    """

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
    print('There are %d line in database and found %d title data,'
          ' %d description data %d breadcrumbs data,'
          ' %d specifications data' % (len(result), a, b, c, d))


def get_data():
    """
    Get all extraction data of two urls grouped by ean
    :input: None
    :return: set of all extraction data for each url
    :rtype: class 'set'
    """

    query_test_data = s.query(func.array_agg(models.ProductData.url),
                              func.count(models.ProductData.ean)). \
        group_by(models.ProductData.ean).all()

    set_all_data = set({})

    for test_data in query_test_data:
        if test_data[1] == 2:  # check if the two urls are grouped by ean
            all_data = s.query(models.ProductData.all_data). \
                filter_by(url=test_data[0][0]).first()
            text1 = str(all_data)
            all_data2 = s.query(models.ProductData.all_data). \
                filter_by(url=test_data[0][1]).first()
            text2 = str(all_data2)
            set1 = (text1, text2)
            set_all_data.add(set1)

    return set_all_data
