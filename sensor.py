# Get sensor scores
def find_list_sensordist(word_dicts, allowed):
    list_sensordist = []
    dict_sensordist= {}


    for sent in allowed.keys():
        print(sent)

        j = allowed[sent][1]  # swapped_idx
        print("swapped_idx j = ", j)

        sensor_dist = 0
        for i in range(len(sent)):
            word = sent[i]
            print('current word ', i, ': ', word)

            if j == False:  # Not swapped
                print('Adding (no swap):', word_dicts[i][word])
                sensor_dist += word_dicts[i][word] * 0.5
            else:
                if i == j:
                    print('Adding (at j)', word_dicts[i+1][word])
                    sensor_dist += word_dicts[i+1][word]  # Find dist in the next column
                elif i == j+1:
                    print('Adding (after j)', word_dicts[i-1][word])
                    sensor_dist += word_dicts[i-1][word]  # Find dist in the previous column
                else:
                    print('Adding (not j):', word_dicts[i][word])
                    sensor_dist += word_dicts[i][word]

        # the smaller distance, the better
        # NORMALIZE distance with # of words, since longer phrase tends to have longer distance
        sensor_dist = sensor_dist/len(sent)

        dict_sensordist[sent] = sensor_dist
        list_sensordist.append(sensor_dist)

    return dict_sensordist, list_sensordist


def sort_by_sensor(word_dicts, allowed):
    dict_sensordist, list_sensordist = find_list_sensordist(word_dicts, allowed)

    sensor_list = []
    for i, sent in enumerate(allowed.keys()):
        sensor_score = 1 - list_sensordist[i] / sum(list_sensordist)  # smaller distance = higher probability
        sensor_list.append((sent, sensor_score))
    sensor_dict = dict(sensor_list)
    sorted_sensor = {k: v for k, v in sorted(sensor_dict.items(), reverse=True, key=lambda item: item[1])}

    return dict_sensordist, sensor_dict, sorted_sensor
