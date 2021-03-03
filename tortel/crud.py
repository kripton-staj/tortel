import config
import extract_data
import models
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(config.DATABASE_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()

extracted_titles = extract_data.extracted_titles
for value in extracted_titles:
    product = s.query(models.ProductPage).filter(models.ProductPage.url.ilike(value)).first()
    if not product:
        product = models.ProductPage(url=value, title=extracted_titles[value])
        s.add(product)
    else:
        product.title = extracted_titles[value]
        s.add(product)

s.commit()
s.close()
