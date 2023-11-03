from itertools import product
import numpy as np


def find_ave_dist(classname, class_dict, arr):
    idx = class_dict[classname]
    ave_dist = np.sum(arr[idx]) / len(idx)
    return ave_dist


def find_score_dict(class_dict, arr):
    score_dict = {}
    for classname in class_dict.keys():
        score_dict[classname] = find_ave_dist(classname, class_dict, arr)
    return score_dict


def get_candidates(score_dict):
    rank = sorted(score_dict.items(), key=lambda x: x[1])
    # print(rank)
    # return rank[:top_k_words]
    return rank


def one_data_point(data, class_dict, data_num, top_k_words=3, dist_idx=3):
    full_rank = []
    top_k_list = []
    for arr in data[data_num][dist_idx]:
        score_dict = find_score_dict(class_dict, arr)
        probs = get_candidates(score_dict)
        full_rank.append(probs)

        top_k = probs[:top_k_words]
        top_k_list.append(top_k)
    return full_rank, top_k_list


def get_combo(data, word_index, class_dict, data_num):
    # phrase_length = len(temp_list)  # number of words in the phrase
    # num_of_candidates = len(temp_list[0])  # number of candidates for each word

    full_rank, temp_list = one_data_point(data, class_dict, data_num)

    word_dicts = []
    for d in temp_list:
        temp_dict = dict(d)
        mydict = {}
        for k, v in temp_dict.items():
            mydict[word_index[k]] = v
        word_dicts.append(mydict)

    sentences = list(product(*[d.keys() for d in word_dicts]))

    return word_dicts, sentences, full_rank
