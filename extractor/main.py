from tortel.extractor.crud import (get_product_page, print_report, s,
                                   write_product_text)
from tortel.extractor.extractor import extract_product_text


def main():
    """
    Calling print_report() to see how much html and
    product data are in the database.(optional)
    Calling get_product_page() function for get product pages from the database.
    In the for loop, all products are read line by line from the database.
    In each product object, its html has given as a parameter into the
    extract_product_text() function, and this function returns its product text.
    The write_product_text() function is called to write this product_text
    to the database.
    This for loop is repeated for every product object in the database.
    After all product texts are written to the database, the session is closed.
    :return: None
    """
    print_report()
    product_page = get_product_page()
    for product in product_page:
        product_text = extract_product_text(product.html)
        write_product_text(product, product_text)
    s.close()


if __name__ == '__main__':
    main()
