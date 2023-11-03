# import numpy as np
import re
from nltk.util import ngrams
import pandas as pd
import numpy as np
from csv import DictWriter
import pickle as pkl


def read_file(filename):
    with open(filename, 'r', encoding = 'utf-8') as f:
        data = []
        for para in f:
            data += re.findall(r"[\w']+|[.,!?;\*-]", para.upper())
        print(data)
    return data


def create_ngram(train, n):
    ngram_tup = list(ngrams(train, n))
    ngram = []
    for tup in ngram_tup:
        phrase = ''
        for word in tup:
            phrase += word + ' '
        phrase = phrase.rstrip()
        ngram.append(phrase)
    d = dict((x, ngram.count(x)) for x in set(ngram))
    d_norm = {k: v/sum(d.values()) for k, v in d.items()}
    return d_norm


# def dict2csv(d):
#     df = pd.DataFrame.from_dict(d, orient='index', columns=['ngram_score'])
#     df = df.reset_index()
#     df = df.rename(columns={'index': 'query'})
#     print(df)
#     # df['mini_dict'] = df.apply(lambda row: {row['query'].value(): np.float(row['ngram_score'].value())})
#     # for minid in df['mini_dict'].values():
#     for i in range(len(df)):
#         query = df['query'].iloc[i]
#         ngram_score = df['ngram_score'].iloc[i]
#         minid = {'query': query, 'ngram_score': ngram_score}
#         with open('localngram.csv', 'a', newline='') as f:
#             DictWriter(f, fieldnames=['query', 'ngram_score']).writerow(minid)
#             f.close()


def create_pickel(filename):
    data = read_file(filename) # long list of separated words

    final_d = {}
    for n in range(4):
        n += 2
        print(n)
        d = create_ngram(data, n)
        # dict2csv(d)
        final_d.update(d)

    with open('localngram.pkl', 'wb') as f:
        pkl.dump(final_d, f)
