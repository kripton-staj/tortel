from tortel.extractor.crud import get_ean_group
from tortel.similarity_checker.pipeline import (jaccard_similarity, n_grams,
                                                remove_stop_words_and_puncts,
                                                stemming, tokenization)


def similarity_calculator():
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
            first_n_gram, second_n_gram = n_grams(stemming_product_text)
            similarity = jaccard_similarity(first_n_gram, second_n_gram)
            similarity_list.append(similarity)
    return similarity_list


def accuracy_calculator(similarity_list):
    """
    Reports on how much of the similarity rates exceeded 80%
    :param similarity_list: list of similarity ratios
    :return: None
    """
    accuracy = 0
    for similarity_ratio in similarity_list:
        if similarity_ratio >= 0.8:
            accuracy += 1
    print("There are %d similarities and %d of them are greater than 0.8"
          % (len(similarity_list), accuracy))


similarities = similarity_calculator()
accuracy_calculator(similarities)
