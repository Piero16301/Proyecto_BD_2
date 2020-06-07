import json
import os
import math

#listDocument = os.listdir('data')
listDocument = ['tweets_2018-08-07.json', 'tweets_2018-08-08.json', 'tweets_2018-08-09.json']

def generateIndex(listTerm):
    indexDb = {}
    for term in listTerm:
        indexDb[term] = [0]
    for document in listDocument:
        print("--------------------------")
        print("Analysing document: ", document)
        print("--------------------------")
        fjson = open('data/' + document, )
        listTweetsDoc = json.load(fjson)
        for term in listTerm:
            tf = 0
            df = 0
            for tweet in listTweetsDoc:
                if tweet['retweeted'] is True:
                    rtText = tweet['RT_text']
                    if term in rtText:
                        tf += 1
                else:
                    textTweet = tweet['text']
                    if term in textTweet:
                        tf += 1
            if tf > 0:
                indexDb[term][0] += 1   # Update Document Frequency
                indexDb[term].append((document,tf))
        fjson.close()
    return indexDb

listTerm = ["espina", "corrupto", "fujimorista", "moral", "candidato", "miedo"]
indexDb = generateIndex(listTerm)
for term in indexDb:
    print(term, "-->", indexDb[term])


def genScore():
    print("test")
