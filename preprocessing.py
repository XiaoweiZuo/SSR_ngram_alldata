import pickle
import pandas as pd
import numpy as np

def get_file_content(filename):
    with open(filename, 'rb') as f:
        SSR_data = pickle.load(f)
    return SSR_data


def decode(word_index, num_list):
    phrase = ''
    for num in num_list:
        phrase += word_index[num] + ' '
    phrase = phrase.rstrip() # Get rid of whitespace at the end of the string
    return phrase


def norepeat(mystring):
    mystring = mystring.split()
    norepeat = mystring[0]+' '  # 1st word
    for i, word in enumerate(mystring):
        if i >0:
            if word != mystring[i-1]:
                norepeat += word + " "
    norepeat = norepeat.rstrip()
    return norepeat


def get_df(data, word_index, empty_cols):
    df = pd.DataFrame(data, columns=['path', 'pred', 'truth', 'arrays'])  # Original df: 114 lines

    # Get real truth from file name
    df['real_truth'] = df.apply(
        lambda row: row['path'][0].replace('C:\\projects\\Collected_SSR_Data\\EMG_only_082223\\sentences\\', '').split('\\')[0],
        axis=1)

    df['pred_decoded'] = df.apply(lambda row: decode(word_index, row['pred']), axis=1)
    df['pred_decoded_norepeat'] = df.apply(lambda row: norepeat(row['pred_decoded']), axis=1)

    # df['sensor_accu'] = df.apply(lambda row: 1 if row['pred_decoded_norepeat'] == row['real_truth'] else 0, axis=1)

    for col in empty_cols:
        df[col] = ''

    return df


def find_index_for_one_class(classname, shot_classes):
    idx = []
    for i, x in enumerate(shot_classes):
        if x == classname:
            idx.append(i)
    return idx


def find_index_for_all_classes(class_arr, shot_classes):
    class_dict = {}
    for classname in class_arr:
        idx = find_index_for_one_class(classname, shot_classes)
        class_dict[classname] = idx
    return class_dict


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


def output(empty_cols, filename='SSR_data.pkl'):
    SSR_data = get_file_content(filename)
    data, word_index, shot_classes = SSR_data.get('data'), SSR_data['index'], SSR_data['shot_classes']

    word_index = {v: k for k, v in word_index.items()}  # Reverse key and value in the dictionary "word_index"
    # to become: {0: 'ASSISTANCE', 1: 'DO', ...}

    df = get_df(data, word_index, empty_cols)

    class_dict = find_index_for_all_classes(set(shot_classes), shot_classes)  # get indices of each class

    # wrong_idx = [0, 9, 15, 17, 18, 29, 33, 40, 41, 44, 48, 78, 104] # 29: ends at query no. 27

    return data, word_index, class_dict, df



