import preprocessing
import mycombination
import ngram
import sensor


def get_sorted_final(ngram_dict, sensor_dict):
    # Find the same key

    final_dict = {}
    for sent in ngram_dict.keys():
        ngram_score = ngram_dict[sent]
        sensor_score = sensor_dict[sent]

        final_dict[sent] = sensor_score  # Question: how to integrate ngram into this eqn; how to compare 2gram vs 3gram
    # print(final_dict)
    sorted_final = {k: v for k, v in sorted(final_dict.items(), reverse=True, key=lambda item: item[1])}
    # print(sorted_final)

    return sorted_final


def one_data_point(data, word_index, class_dict, data_num, googlengram, swap=False):
    # data, word_index, class_dict, df = preprocessing.output(filename)
    word_dicts, sentences, full_rank = mycombination.get_combo(data, word_index, class_dict, data_num)

    ngram_dict, googlengram = ngram.ngram_selection(sentences, googlengram, swap)  # ngram_dict is allowed

    dict_sensordist, sensor_dict, sorted_sensor = sensor.sort_by_sensor(word_dicts, ngram_dict)

    # sorted_final = get_sorted_final(ngram_dict, sensor_dict)
    sorted_final = sorted_sensor

    if sorted_final != {}:
        output_sent = list(sorted_final.keys())[0]
        correction = ngram.create_query(output_sent)  # No repeating words
    else:
        correction = ''

    print('correction for current sentence:', correction)

    output = [full_rank, ngram_dict, dict_sensordist, sorted_sensor, correction]

    return output, googlengram
