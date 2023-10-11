import pickle
import numpy as np
import pandas as pd


def get_file_content(filename):
    with open(filename, 'rb') as f:
        SSR_data = pickle.load(f)
    return SSR_data


def get_df(data):
    df = pd.DataFrame(data, columns=['path', 'pred', 'truth', 'arrays'])  # Original df: 114 lines
    df['path'] = df.apply(
        lambda row: row['path'][0].replace('C:\\projects\\Collected_SSR_Data\\EMG_only_082223\\sentences\\', ''),
        axis=1)
    return df


def append_list(curr_i, curr_pred, curr_truth, i, pred, truth):
    pred.append(curr_pred)
    truth.append(curr_truth)
    i.append(curr_i)


def get_wrong_pred(df):
    df_idx, pred, truth = [], [], []  # DO NOT write as [[]]*2 cuz it will be linked lists
    for i in range(len(df)):
        curr_pred, curr_truth = df['pred'][i], df['truth'][i]
        if (len(curr_pred) != len(curr_truth)) or ((curr_pred != curr_truth).any()):
            append_list(i, curr_pred, curr_truth, df_idx, pred, truth)
    return df_idx, pred, truth


def get_wrong_word_idx(pred, truth):
    arr = (pred == truth)
    wrong_idx = [i for i, val in enumerate(arr) if not val]
    return wrong_idx


def find_kth_smallest_dist_classes(shot_classes, arr, k):
    idx = np.argpartition(arr, k)[:k]
    # print('idx:', idx)
    class_values = list(shot_classes[idx])
    # print(class_values)
    return class_values


def get_word_candidates(shot_classes, arr, top5=5):
    k = 0
    num_of_elements = 1
    while num_of_elements < top5:
        k += 1
        class_values = find_kth_smallest_dist_classes(shot_classes, arr, k)
        num_of_elements = len(set(class_values))
    return set(class_values)

    # class_values = find_kth_smallest_dist(SSR_data, arr, k)
    # curr_word_pred = []
    # idx = np.argpartition(arr, 4)[:4]


def delete_conti_rep(arr):
    remove_idx = []
    for i in range(len(list(arr))):
        if i < len(arr) - 1:
            if arr[i + 1] == arr[i]:
                # arr.pop(i+1)
                remove_idx.append(i + 1)
    return np.delete(arr, remove_idx)


def tidy_df(df):
    tidied_df = pd.DataFrame()
    tidied_df['pred'] = df.apply(lambda row: delete_conti_rep(row.pred), axis=1)
    tidied_df['truth'] = df.apply(lambda row: delete_conti_rep(row.truth), axis=1)
    return tidied_df


def figure_out_whats_wrong_in_df(df):
    df2 = tidy_df(df)  # Delete continuous repetitive words
    idx_in_df, tidied_pred, tidied_truth = get_wrong_pred(df2)  # Get misclassified pairs
    df2 = pd.DataFrame()  # Create a new df
    df2['idx_in_df'], df2['tidied_pred'], df2['tidied_truth'] = idx_in_df, tidied_pred, tidied_truth
    print(df2)
    return df2


# def break_into_words(arrays):
#     arr_list = []
#     for arr in arrays:
#         arr_list


def output(filename = 'SSR_data.pkl'):
    SSR_data = get_file_content('SSR_data.pkl')
    data, shot_classes = SSR_data.get('data'), SSR_data['shot_classes']
    df = get_df(data)
    # df = df.drop(columns=['path'])

    df2 = figure_out_whats_wrong_in_df(df)  # Figure out what was wrong in the dataset
    df3 = df.iloc[df2['idx_in_df']].reset_index()
    df3['tidied_pred'], df3['tidied_truth'] = df2['tidied_pred'], df2['tidied_truth']
    # df = df.drop(columns=['arrays','path'])
    # df3.to_csv('wrong_pred.csv')
    return df3

    # i=0
    # arrays = df3.arrays[i]
    # break_into_words(arrays)

    # pred = df.pred[i]
    # truth = df.truth[i]
    # wrong_idx = get_wrong_word_idx(pred, truth)
    # # print(wrong_idx)
    # # for idx in wrong_idx:
    # #     print(df.arrays[i][idx])
    # arr = df_wrong.arrays[i][0]
    #
    # # k = 7
    # # class_values = find_kth_smallest_dist(SSR_data, arr, k)
    # # print(len(set(class_values)))
    # # print(SSR_data['shot_classes'])
    # print(get_word_candidates(shot_classes, arr, 5))

    # get_wrong_idx(pred, truth)

    # np.argpartition(arr,4)[:4]
