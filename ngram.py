import googleAPI
import time
from csv import DictWriter


def erase_noise(sent):
    sent_nonoise = []
    for i, word in enumerate(sent):
        if word != "NOISE":
            sent_nonoise.append(word)
    sent_nonoise = tuple(sent_nonoise)
    return sent_nonoise


def create_query(sent):
    sent = erase_noise(sent)  # tuple

    # If NOISE at each position and have an empty sentence
    if sent == ():
        return ''

    # query_original = ""
    query_norepeat = sent[0]+' '  # 1st word
    for i, word in enumerate(sent):
        # query_original += word + " "  # Convert tuple into a string of complete sentence
        if i >0:  # Starting from the 2nd word, check repeating words
            if word != sent[i-1]:  # Append if not repeating the previous word
                query_norepeat += word + " "
    # if query_original != query_norepeat:
        # print("Repeating word detected! Original:", query_original, "; Modified:", query_norepeat)
    # query_original = query_original.rstrip() # Get rid of whitespace at the end of the string
    query_norepeat = query_norepeat.rstrip()
    return query_norepeat


def get_ngram_score(allowed, sent, googlengram, swapped_idx = False):
    query = create_query(sent)
    if query == '':  # All NOISE
        ngram_score = 0
    elif len(query.split()) > 5:  # Longer than 5gram, skip
        ngram_score = 0
    elif query in googlengram:
        ngram_score = googlengram[query]
    else:
        ngram_score = 0

        # # Write googlengram result into csv
        # ngram_score = googleAPI.runQuery(query)
        # googlengram[query] = ngram_score
        #
        # d = {'query': query, 'ngram_score': ngram_score}
        # field_names = ['query', 'ngram_score']
        # with open('googlengram.csv', 'a', newline='') as f:
        #     DictWriter(f, fieldnames=field_names).writerow(d)
        #     f.close()

    if ngram_score > 0:
        print("Score = ", ngram_score)
        allowed.append((sent, ngram_score, swapped_idx))
    return allowed, googlengram


def find_allowed(sentences, googlengram, swap=False):
    allowed = []
    delay = 0.2

    i = 0
    for sent in sentences:
        i += 1
        # print("Current sentence no.", i, ":", sent)
        while True:
            try:
                # your request code here
                allowed, googlengram = get_ngram_score(allowed, sent, googlengram)
                break  # if the request was successful, break the loop
            except Exception as e:
                time.sleep(delay)
                if delay > 5:
                    delay = 0.2

        if swap:
            # Swapping
            for j in range(len(sent)):
                if (j > 0) and (j < (len(sent)-1)):
                    # Create a copy of sent as a list
                    swapped = []
                    for ele in sent:
                        swapped.append(ele)

                    temp = swapped[j]
                    swapped[j] = swapped[j+1]
                    swapped[j+1] = temp
                    swapped = tuple(swapped)

                    # print("Swapped sentence no.", i, "-", j, ":", swapped)

                    while True:
                        try:
                            # your request code here
                            allowed, googlengram = get_ngram_score(allowed, swapped, googlengram, j)
                            break  # if the request was successful, break the loop
                        except Exception as e:
                            time.sleep(delay)
                            if delay > 5:
                                delay = 0.2

    allowed_dict = {}
    for ele in allowed:
        # print(ele)

        sent = ele[0]
        ngram_score = ele[1]
        swapped_idx = ele[2]

        allowed_dict[sent] = [ngram_score, swapped_idx]
    # allowed_dict = dict(allowed)
    return allowed_dict, googlengram


def ngram_selection(sentences, googlengram, swap):
    allowed, googlengram = find_allowed(sentences, googlengram, swap)
    # print("after ngram selection_unsort:", allowed)

    # P_big to P_small
    # sorted_ngram = {k: v for k, v in sorted(allowed.items(), reverse=True, key=lambda item: item[1])}
    # print("after ngram selection_sorted:", sorted_ngram)

    return allowed, googlengram
    # return allowed, sorted_ngram, googlengram  # Sorted by ngram score of query_norepeat

