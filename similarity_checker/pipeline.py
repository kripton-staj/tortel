import spacy
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.util import everygrams
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def tokenization(product_text):
    """
    Separates product text into tokens.
    :param product_text: set of product_text for two url
    :return: tokens for two product texts
    :rtype: class 'list'
    """
    tokenizer = RegexpTokenizer(r'\w+')

    tokens1 = tokenizer.tokenize(product_text[0])
    tokens2 = tokenizer.tokenize(product_text[1])
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


def create_n_grams(tokens_with_stemming):
    """
    Join tokens from the tokens list and creates a two text(type string)
     without a space. Then, creates n_grams from that texts. Max_len of
      n_grams indicates as a parameter.
    :param tokens_with_stemming: List of tokens after stemming
    :return: two n_grams list for two text
    :rtype: class 'list'
    """
    tokens_without_space1 = ""
    tokens_without_space2 = ""
    max_len = 3

    for token in tokens_with_stemming[0]:
        tokens_without_space1 += token
    for token in tokens_with_stemming[1]:
        tokens_without_space2 += token

    n_grams_1 = list(everygrams(tokens_without_space1,
                                max_len=max_len))
    n_grams_2 = list(everygrams(tokens_without_space2,
                                max_len=max_len))
    n_grams = [n_grams_1, n_grams_2]
    return n_grams


def tfidf_vectorizer(n_grams):
    """
    Creates vectors for the n_grams by using tfidf vectorizer.
    :param n_grams: n_grams for the product texts
    :return: tfidf: tfidf vectors for the n_grams
    :rtype: class 'scipy.sparse.csr.csr_matrix'
    """
    vectorizer = TfidfVectorizer(analyzer=lambda x: x)

    tfidf = vectorizer.fit_transform(n_grams)
    return tfidf


def check_cosine_distance(tfidf):
    """
    Calculates cosine distance between vectors by using linear kernel.
    :param tfidf: vectors for the n_grams
    :return: cosine_distance: calculated cosine distance between vectors
    :rtype: class 'numpy.ndarray'
    """
    cosine_distance = linear_kernel(tfidf[0], tfidf[1]).flatten()
    return cosine_distance
