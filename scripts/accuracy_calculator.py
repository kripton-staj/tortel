from tortel.scripts.similarity_calculator import (
    similarity_calculator_for_different_products,
    similarity_calculator_for_same_products)


def conf_matrix_calculator():
    """
    Calculates confusion matrix
    :return: true positive, true negative, false positive, false negative
    :rtype: int, int, int, int
    """
    similarity_list = similarity_calculator_for_same_products()
    similarity_list2 = similarity_calculator_for_different_products()
    tp, fn, tn, fp = 0, 0, 0, 0
    for similarity in similarity_list:
        if similarity >= 0.5:
            tp += 1
        else:
            fn += 1
    for different_similarity in similarity_list2:
        if different_similarity < 0.5:
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
    :param fn: number of false negative
    :return: accuracy score
    :rtype: float
    """
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total
    return accuracy


t_pos, t_neg, f_pos, f_neg = conf_matrix_calculator()
accuracy_score = accuracy_calculator(t_pos, t_neg, f_pos, f_neg)
print("accuracy: ", accuracy_score)
