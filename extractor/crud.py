from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tortel.common.config import DATABASE_URI
from tortel.common.models import Base, ProductPage


engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()


def get_product_page():
    """
    Get product pages from the database.
    :return: product page: returns all rows in the database except rows
                           whose html column is an empty string or None
    """
    product_page = s.query(ProductPage).filter(
        ProductPage.html != '', ProductPage.html.isnot(None))
    return product_page


def write_product_text(product, product_text):
    """
    Writes the product text to the relevant product object in the database.
    :param product: This is a single row in the database that contains
                    url, html and product_text. This is taken as the parameter
                    to write product_text on the relevant row.
    :param product_text: Contains the product text to be written to the database
    :return: None
    """

    product.product_text = product_text
    s.add(product)
    s.commit()


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

