import lxml.html
import config
import models
import extracter
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(config.DATABASE_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()


def database_operations():
    product_body = s.query(models.ProductBody)

    for value in product_body:
        response = lxml.html.fromstring(value.body)
        url = value.url
        title = extracter.extract_title(response)
        description = extracter.extract_description(response)
        breadcrumbs = extracter.extract_breadcrumbs(response)

        product_data = models.ProductData(url=url, title=title, description=description, breadcrumbs=breadcrumbs)
        s.add(product_data)
    s.commit()
    s.close()


database_operations()


