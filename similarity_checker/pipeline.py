import spacy
from distance import jaccard
from nltk.stem.snowball import SnowballStemmer
from simhash import Simhash


def tokenization(product_text):
    """
    Separates product text into tokens.
    :param product_text: set of product_text for two url
    :return: tokens for two product texts
    :rtype: class 'list'
    """

    nlp = spacy.load("nl_core_news_sm")

    doc1 = nlp(str(product_text[0]))
    doc2 = nlp(str(product_text[1]))
    tokens1 = [token.text for token in doc1]
    tokens2 = [token2.text for token2 in doc2]
    tokens = [tokens1, tokens2]

    return tokens


def remove_stop_words_and_puncts(tokens):
    """
    Removes stop words and punctuations from list of tokens.
    :param tokens: tokens list for two product texts
    :return: tokens list without stop words and punctuations
    :rtype: class 'list'
    """

    nlp = spacy.load('nl_core_news_lg')
    tokens_without_sw_and_punct1 = [token for token in tokens[0]
                                    if not nlp.vocab[token].is_punct
                                    and not nlp.vocab[token].is_stop]
    tokens_without_sw_and_punct2 = [token for token in tokens[1]
                                    if not nlp.vocab[token].is_punct
                                    and not nlp.vocab[token].is_stop]
    tokens_without_sw_and_punct = [tokens_without_sw_and_punct1,
                                   tokens_without_sw_and_punct2]
    return tokens_without_sw_and_punct


def stemming(tokens_without_sw_and_punct):
    """
    Creates a new list of tokens after applying stemming into tokens.
    :param tokens_without_sw_and_punct: List of tokens without
                                        stop words and punctuations
    :return: list of tokens after applying stemming
    :rtype: class 'list'
    """

    stemmer = SnowballStemmer(language='dutch')
    tokens_after_stemming1 = [stemmer.stem(token) for token
                              in tokens_without_sw_and_punct[0]]
    tokens_after_stemming2 = [stemmer.stem(token) for token
                              in tokens_without_sw_and_punct[1]]
    tokens_after_stemming = [tokens_after_stemming1,
                             tokens_after_stemming2]
    return tokens_after_stemming


def sim_hash(tokens_after_stemming):
    vector1 = Simhash(tokens_after_stemming[0])
    vector2 = Simhash(tokens_after_stemming[1])
    vector1_value = float(vector1.value)
    vector2_value = float(vector2.value)

    if vector1_value > vector2_value:
        similarity = vector2_value/vector1_value
    else:
        similarity = vector1_value/vector2_value

    return similarity


def jaccard_similarity(tokens_after_stemming):
    similarity = jaccard(tokens_after_stemming[0],
                         tokens_after_stemming[1])

    return 1-similarity
