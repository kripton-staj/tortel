import argparse
import json

from common.config import DATABASE_URI
from common.models import Base, ProductPage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def write_file_to_database(json_list):
    """
    Write url and ean to the ProductPage table into the database.
    Update values if the url already exists in database.
    :param json_list: list object
     that contains url and ean contents of json file
    :return:None
    """
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)
    s = session()

    for key in json_list:
        url = key['url']
        ean = key['ean']
        product_page = s.query(ProductPage).\
            filter(ProductPage.url.ilike(url)).first()
        if not product_page:
            product_page = ProductPage(url=url, ean=ean)
            s.add(product_page)
        else:
            product_page.url = url
            product_page.ean = ean
            s.add(product_page)

    s.commit()
    s.close()


def main():
    """
    Parsing JSON input file which entered with the -f parameter,
    load the contents keys and values and call write_file_to_database function
    to write that contents into the database
    :input: None
    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file',
        help='JSON input file',
        type=argparse.FileType('r'),
    )

    args = parser.parse_args()
    json_list = json.load(args.file)
    write_file_to_database(json_list)


if __name__ == '__main__':
    main()
