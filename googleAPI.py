import requests
import urllib

def runQuery(query, start_year=2000, end_year=2019, corpus=26, smoothing=2):

    # converting a regular string to
    # the standard URL format
    # eg: "geeks for,geeks" will
    # convert to "geeks%20for%2Cgeeks"
    query = urllib.parse.quote(query)

    # creating the URL
    url = 'https://books.google.com/ngrams/json?content=' + query + '&year_start=' + str(start_year) + '&year_end=' + \
    str(end_year) + '&corpus=' + str(corpus) + '&smoothing=' + \
    str(smoothing) + '' + '&case_insensitive=true'

    #The smoothing value specifies the number of years on either side of a data point to use for smoothing. For example,
    #with a smoothing of 3, the data point for 1995 would be an average of the frequencies for the years 1992, 1993, 1994,
    # 1995, 1996, 1997, and 1998. This helps to reduce the effect of year-to-year fluctuations and make broader trends more visible.

    # requesting data from the above url
    response = requests.get(url)

    # extracting the json data from the response we got
    output = response.json()

    # creating a list to store the ngram data
    return_data = []

    if len(output) == 0:
        # if no data returned from site,
        # print the following statement
        # return "No data available for this Ngram."
        return 0
    else:
        # if data returned from site,
        # store the data in return_data list
        for num in range(len(output)):

              # getting the name
            return_data.append((output[num]['ngram'],
                                # getting ngram data
                                output[num]['timeseries'])
                               )
    return return_data[0][1][-1]
#
#
#
