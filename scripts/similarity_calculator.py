from tortel.extractor.crud import get_ean_group
from tortel.similarity_checker.pipeline import (check_cosine_distance,
                                                create_n_grams,
                                                remove_stop_words_and_puncts,
                                                stemming, tfidf_vectorizer,
                                                tokenization)


def similarity_calculator(text1, text2):
    """
    Calculate similarity ratio for two texts.
    :param text1: first product text
    :param text2: second product text
    :return: None
    """
    text = [text1] + [text2]
    stemming_product_text = stemming(
        remove_stop_words_and_puncts(tokenization(text)))
    n_grams = create_n_grams(stemming_product_text)
    tfidf = tfidf_vectorizer(n_grams)
    similarity = check_cosine_distance(tfidf)
    print(similarity)


def similarity_calculator_for_same_products():
    """
    Calculate similarity ratio for the two product that have the same ean.
     Append all similarity ratios into a list.
    :return: list of similarity ratios
    :rtype: class list
    """
    ean_group = get_ean_group()
    similarity_list = []
    for group in ean_group:
        first_product = group[0][0]
        second_product = group[0][1]
        if first_product and second_product:
            product_text = group[0]
            stemming_product_text = stemming(
                remove_stop_words_and_puncts(tokenization(product_text)))
            n_grams = create_n_grams(stemming_product_text)
            tfidf = tfidf_vectorizer(n_grams)
            similarity = check_cosine_distance(tfidf)
            similarity_list.append(similarity)
    return similarity_list


def similarity_calculator_for_different_products():
    """
    Calculate similarity ratio for the two different product.
     Append all similarity ratios into a list.
    :return: list of similarity ratios
    :rtype: class list
    """
    ean_group = get_ean_group()
    similarity_list2 = []
    for text in range(len(ean_group)-1):
        first_product = ean_group[text][0][0]
        second_product = ean_group[text+1][0][0]
        product_text = []
        if first_product and second_product:
            product_text.append(first_product)
            product_text.append(second_product)
            stemming_product_text = stemming(
                remove_stop_words_and_puncts(tokenization(product_text)))
            n_grams = create_n_grams(stemming_product_text)
            tfidf = tfidf_vectorizer(n_grams)
            similarity = check_cosine_distance(tfidf)
            similarity_list2.append(similarity)
    return similarity_list2


text_1 = "DUUX Sphere Ultrasonic Humidifier wit kopen?"
text_2 = "Duux Sphere Ultrasone Luchtbevochtiger"
similarity_calculator(text_1, text_2)
