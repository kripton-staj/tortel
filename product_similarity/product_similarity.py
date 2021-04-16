import spacy
import tortel.Extractor.config as config
from tortel.Extractor.models import Base
import tortel.Extractor.models as models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


engine = create_engine(config.DATABASE_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()


def get_test_data():       # Get all extraction data of two urls grouped by ean
    query_test_data = s.query(func.array_agg(models.ProductData.url),
                              func.count(models.ProductData.ean)).group_by(models.ProductData.ean).all()

    set_all_data = set({})

    for test_data in query_test_data:
        if test_data[1] == 2:  # check if the two urls are grouped by ean
            all_data = s.query(models.ProductData.all_data).filter_by(url=test_data[0][0]).first()
            text1 = str(all_data)
            all_data2 = s.query(models.ProductData.all_data).filter_by(url=test_data[0][1]).first()
            text2 = str(all_data2)
            set1 = (text1, text2)
            set_all_data.add(set1)

    return set_all_data


def tokenization(set_all_data):       # Tokenization, remove punctuation and stop words
    nlp = spacy.load("nl_core_news_sm")

    for data in set_all_data:
        doc1 = nlp(data[0])
        doc2 = nlp(data[1])

        tokens_without_sw1 = [token.text for token in doc1 if not token.is_stop and not token.is_punct]
        print(tokens_without_sw1)

        tokens_without_sw2 = [token.text for token in doc2 if not token.is_stop and not token.is_punct]
        print(tokens_without_sw2)


tokenization(get_test_data())
