import json
import os
import math
import pandas as pd

# listDocument = os.listdir('data')
listDocument = ['tweets_2018-08-07.json', 'tweets_2018-08-08.json', 'tweets_2018-08-09.json']

tablaInicial = {'Termino': ['Clima', 'Biblioteca', 'Universidad', 'España', 'Libros'],
                'Doc1': [1452, 0, 2122, 4123, 0],
                'Doc2': [0, 2093, 0, 4245, 1234],
                'Q': [0, 1345, 1453, 0, 2133]
                }

df = pd.DataFrame(tablaInicial, columns=['Termino', 'Doc1', 'Doc2', 'Q'], index=['Clima', 'Biblioteca', 'Universidad', 'España', 'Libros'])

df.to_csv(r'tabla_inicial.csv', index=False, header=True)


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
                indexDb[term][0] += 1  # Update Document Frequency
                indexDb[term].append([document, tf])
        fjson.close()
    return indexDb


listTerm = ["espina", "corrupto", "fujimorista", "moral", "candidato", "miedo"]
indexDb = generateIndex(listTerm)
for term in indexDb:
    print(term, "-->", indexDb[term])

def genScore():
    for term in indexDb:
        idf = math.log(3/(indexDb[term][0]), 10)
        for doc in range(1,len(indexDb[term])):
            tf = indexDb[term][doc][1]
            tfIdf = math.log(1+tf, 10) * idf
            indexDb[term][0] = idf
            indexDb[term][doc][1] = tfIdf
print("----")
genScore()
for term in indexDb:
    print(term, "-->", indexDb[term])
