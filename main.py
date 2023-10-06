import balancescores
import preprocessing
import csv
import pandas as pd
import pickle as pkl

def trim(mylist, num):
    for i in range(num):
        mylist.pop()
    return mylist


def create_new_row(data_num, df, empty_cols, output):
    row = [data_num] + df.loc[data_num, :].values.tolist()
    row = trim(row, len(empty_cols))
    row = row + output
    return row


if __name__ == '__main__':
    empty_cols = ['full_rank',
                  'after_ngram_selection',
                  'candidate_sensor_distances',
                  # 'sortedby_ngramscore',
                  'sortedby_sensorscore',
                  # 'sortedby_weightedscore',
                  'ngram_correction']
    data, word_index, class_dict, df = preprocessing.output(empty_cols)

    # df.to_csv('original_data.csv')

    # output = balancescores.one_data_point(data, word_index, class_dict, 41)
    # # For debugging
    # list_data_num = [78, 97]
    # list_data_num = [0, 1]
    # df = df_ori.loc[list_data_num]
    # df = df.reset_index(drop=True)
    # print(df)

    filename = 'df.csv'
    df.to_csv(filename)

    df_googlengram = pd.read_csv("googlengram.csv")
    googlengram = {k: list(v.values())[0] for k, v in df_googlengram.set_index('query').to_dict('index').items()}

    for data_num in range(len(df)):
        print("Next data point:", data_num)

        output, googlengram = balancescores.one_data_point(data, word_index, class_dict, data_num, googlengram)
        row = create_new_row(data_num, df, empty_cols, output)

        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
            f.close()

    # df_googlengram = pd.DataFrame.from_dict(googlengram, orient='index')
    # df_googlengram.to_csv('googlengram.csv')

    dataset_size = len(df)
    df = pd.read_csv('df.csv')
    df = df.iloc[dataset_size:].reset_index(drop=True).drop(df.columns[0], axis=1)
    df['sensor_accu'] = df.apply(lambda row: 1 if row['pred'] == row['real_truth'] else 0, axis=1)

    df['sensor_accu'] = df.apply(lambda row: 1 if row['pred_decoded_norepeat'] == row['real_truth'] else 0, axis=1)
    df['ngram_accu'] = df.apply(lambda row: 1 if row['ngram_correction'] == row['real_truth'] else 0, axis=1)

    with open('df.pkl', 'wb') as f:
        pkl.dump(df, f)

    df.to_csv('df_final.csv')

    sensor_accu = df['sensor_accu'].sum()/len(df)
    ngram_accu = df['ngram_accu'].sum()/len(df)
    print("sentence accuracy without ngram", sensor_accu*100, '%')
    print("sentence accuracy with ngram", ngram_accu*100, '%')
