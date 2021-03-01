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
    product = models.Product(title=value)
    s.add(product)

s.commit()
s.close()
