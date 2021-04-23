import spacy


def tokenization(set_product_text):
    """
    Tokenization, remove punctuation and stop words
    :param set_product_text: set of all extraction data for each url
    :return: set of tokens for all extracted data
    :rtype: class 'set'
    """

    nlp = spacy.load("nl_core_news_sm")

    set_tokenization = set({})
    for product_text in set_product_text:
        doc1 = nlp(product_text[0])
        doc2 = nlp(product_text[1])

        tokens_without_sw1 = [token.text for token in doc1
                              if not token.is_stop and not token.is_punct]
        tokens_without_sw2 = [token.text for token in doc2
                              if not token.is_stop and not token.is_punct]
        tokens_without_sw = (str(tokens_without_sw1), str(tokens_without_sw2))
        set_tokenization.add(tokens_without_sw)

    return set_tokenization


def check_cosine_similarity(set_tokenization):
    """
    WP
    """
    nlp = spacy.load('nl_core_news_lg')
    for tokens_tuple in set_tokenization:
        doc1 = nlp(tokens_tuple[0])
        doc2 = nlp(tokens_tuple[1])
        for token1 in doc1:
            for token2 in doc2:
                if not token1.is_punct and not token2.is_punct:
                    print(token1.text, token2.text, token1.similarity(token2))