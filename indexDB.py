import json
import os
import math
import pandas as pd

listDocument = os.listdir('data')
#listDocument = ['tweets_2018-08-07.json', 'tweets_2018-08-08.json', 'tweets_2018-08-09.json']
numTotalDocs = len(listDocument)

tablaInicial = {'Termino': ['Clima', 'Biblioteca', 'Universidad', 'España', 'Libros'],
                'Doc1': [1452, 0, 2122, 4123, 0],
                'Doc2': [0, 2093, 0, 4245, 1234],
                'Q': [0, 1345, 1453, 0, 2133]
                }

df = pd.DataFrame(tablaInicial, columns=['Termino', 'Doc1', 'Doc2', 'Q'], index=['Clima', 'Biblioteca', 'Universidad', 'España', 'Libros'])

df.to_csv(r'tabla_inicial.csv', index=False, header=True)


data = pd.read_csv('tabla_inicial.csv')
print(data)

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

def genIdf_tfIdf():
    print("genIDF_TFIDF")
    for term in indexDb:
        idf = math.log(numTotalDocs/(indexDb[term][0]), 10)
        indexDb[term][0] = idf
        for doc in range(1,len(indexDb[term])):
            #print(indexDb[term][doc][1])
            tf = indexDb[term][doc][1]
            tfIdf = math.log(1+tf, 10) * idf
            indexDb[term][doc][1] = tfIdf

print("----")
genIdf_tfIdf()
for term in indexDb:
    print(term, "-->", indexDb[term])


query = ["espina"]

def genQuery(query):
    print(" -- Generate TF_IDF from Query --")
    queryDic = {}
    for term in indexDb:
        tf = 0
        if term not in query: continue
        df = 1
        for word in query:
            if term == word:
                tf += 1
        print("tf_query: ", tf)
        tfIdf = math.log(1+tf,10) * indexDb[term][0]
        queryDic[term] = tfIdf
    print(queryDic)
    return queryDic

queryItdf = genQuery(query)

def genSquareByDoc():
    print("-- Gen SquareByDoc --")
    squareByDoc = {}
    for doc in listDocument:
        squaretfIdfDoc = 0
        print("check doc: ", doc)
        for term in indexDb:
            print("check term: ", term)
            for docNum in range(1,len(indexDb[term])):
                if indexDb[term][docNum][0] == doc:
                    tfIdfDoc = indexDb[term][docNum][1]
                    squaretfIdfDoc += tfIdfDoc**2
        squaretfIdfDoc = math.sqrt(squaretfIdfDoc)
        squareByDoc[doc] = squaretfIdfDoc
    # Square Query
    print("-- Square Query --")
    querySquare = 0
    for term in queryItdf:
        querySquare += queryItdf[term]**2
    squareByDoc['query'] = math.sqrt(querySquare)
    print(squareByDoc)
    return squareByDoc


squareByDoc = genSquareByDoc()

'''
def genNormalizacion():
    print("-- Gen Normlization --")
    dicCoseno = {}
    for document in listDocument:
        for term in indexDb:
            normalizadoTerm = 0
            for docNum in range(1,len(indexDb[term])):
                if document == indexDb[term][docNum][0]:
                    print("term: ", term,  "document:", indexDb[term][docNum], " tfIdf: ", indexDb[term][docNum][1])
                    tfIdf = indexDb[term][docNum][1]
                    normalizadoTerm = tfIdf/squareByDoc[document]

#genNormalizacion()

'''

'''
def genDataFrame():
    tablaInicial = {}
    tablaInicial['Termino'] = []
    for term in indexDb:
        tablaInicial['Termino'].append(term)


print("test")
qItdf = queryItdf['espina']
print(qItdf)

'''