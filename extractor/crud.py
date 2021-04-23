from bs4 import BeautifulSoup
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from tortel.common.config import DATABASE_URI
from tortel.common.models import Base, ProductPage
from tortel.extractor.extractor import (extract_breadcrumbs,
                                        extract_description,
                                        extract_specifications, extract_title)

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
    product_page = s.query(ProductPage)
    for product in product_page:
        if product.html:
            soup = BeautifulSoup(product.html, "lxml")
            title = extract_title(soup)
            description = extract_description(soup)
            breadcrumbs = extract_breadcrumbs(soup)
            specifications = extract_specifications(soup)
            product_text = str(title) + " " + str(description) + " " + str(
                breadcrumbs) + " " + str(specifications)

            product.product_text = product_text
            s.add(product)

    s.commit()
    s.close()


def print_report():
    """
    This function has been written to see
     how much data we can extract from the given url.
    :input: None
    :return: None
    """

    result = s.query(ProductPage).all()
    number_of_product_text = 0
    number_of_html = 0

    for row in result:
        if row.html:
            number_of_html += 1
        if row.product_text:
            number_of_product_text += 1

    print('There are %d line in database and found'
          ' %d html body %d product_text data'
          % (len(result), number_of_html, number_of_product_text))


def get_data():
    """
    Get all extraction data of two urls grouped by ean
    :input: None
    :return: set of product text data for each url
    :rtype: class 'set'
    """

    query_test_data = s.query(func.array_agg(ProductPage.url),
                              func.count(ProductPage.ean)). \
        group_by(ProductPage.ean).all()

    set_product_text = set({})
    for test_data in query_test_data:
        if test_data[1] == 2:  # check if the two urls are grouped by ean
            product_text = s.query(ProductPage.product_text). \
                filter_by(url=test_data[0][0]).first()
            text1 = str(product_text)

            product_text2 = s.query(ProductPage.product_text). \
                filter_by(url=test_data[0][1]).first()
            text2 = str(product_text2)
            if text1 == '(None,)' or text2 == '(None,)':
                break
            set1 = (text1, text2)
            set_product_text.add(set1)

    return set_product_text
