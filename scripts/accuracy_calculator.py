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
            first_n_gram, second_n_gram = n_grams(stemming_product_text)
            similarity = jaccard_similarity(first_n_gram, second_n_gram)
            similarity_list2.append(similarity)
    return similarity_list2


def conf_matrix_calculator(similarity_list, similarity_list2):
    """
    Calculates confusion matrix
    :param similarity_list: similarity ratios for the same products
    :param similarity_list2: similarity ratios for the different products
    :return: true positive, true negative, false positive, false negative
    :rtype: int, int, int, int
    """
    tp, fn, tn, fp = 0, 0, 0, 0
    for similarity in similarity_list:
        if similarity >= 0.3:
            tp += 1
        else:
            fn += 1
    for different_similarity in similarity_list2:
        if different_similarity <= 0.3:
            tn += 1
        else:
            fp += 1
    return tp, tn, fp, fn


def accuracy_calculator(tp, tn, fp, fn):
    """
    Calculates accuracy score
    :param tp: number of true positive
    :param tn: number of true negative
    :param fp: number of false positive
    :param fn: number of true negative
    :return: accuracy score
    :rtype: float
    """
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total
    return accuracy


list1 = similarity_calculator()
list2 = similarity_calculator_for_different_products()
t_pos, t_neg, f_pos, f_neg = conf_matrix_calculator(list1, list2)
accuracy_score = accuracy_calculator(t_pos, t_neg, f_pos, f_neg)
print(accuracy_score)
