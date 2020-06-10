import json
import os
import math
import re
import pandas as pd
from Preprocesamiento import generateTokens

'''
tablaInicial = {'Termino': ['Clima', 'Biblioteca', 'Universidad', 'España', 'Libros'],
                'Doc1': [1452, 0, 2122, 4123, 0],
                'Doc2': [0, 2093, 0, 4245, 1234],
                'Q': [0, 1345, 1453, 0, 2133]
                }

df = pd.DataFrame(tablaInicial, columns=['Termino', 'Doc1', 'Doc2', 'Q'], index=['Clima', 'Biblioteca', 'Universidad', 'España', 'Libros'])

df.to_csv(r'tabla_inicial.csv', index=False, header=True)
data = pd.read_csv('tabla_inicial.csv')

#print(data)
'''

def generateIndex(numTotalTweets):
    dirName = 'data'
    listTerm = generateTokens(dirName)
    print("-- Generate Index --")
    listDocument = os.listdir(dirName)
    indexDb = {}
    for term in listTerm:
        indexDb[term] = [0, {}]
    for document in listDocument:
        print("--------------------------")
        print("Analysing document: ", document)
        print("--------------------------")
        fjson = open(dirName + "/" + document, encoding="utf-8")
        listTweetsDoc = json.load(fjson)
        for tweet in listTweetsDoc:
            numTotalTweets += 1
            if tweet['retweeted'] is True:
                text = tweet['RT_text']
            else:
                text = tweet['text']
            text = text.strip()
            text = text.lower()
            text = re.sub('[¿|?|$|.|,|:|;|!|º|«|»|(|)|@|¡|"|😆|/|#]', '', text)
            text = text.split()
            for word in text:
                if word in listTerm:    ## si es keyword
                    if tweet['id'] in indexDb[word][1]:
                        indexDb[word][1][tweet['id']] += 1      # Update tf de keyword (word) en tweetId
                    else:
                        indexDb[word][1][tweet['id']] = 1       # init tf de keyword (word) en tweetId
                        indexDb[word][0] += 1  # Update Document Frequency
        fjson.close()
    print(indexDb)
    return [indexDb, numTotalTweets]


def genIdf_tfIdf(indexDb, numTotalDocs):
    print("genIDF_TFIDF")
    for term in indexDb:
        idf = math.log(numTotalDocs/(indexDb[term][0]), 10)
        indexDb[term][0] = idf
        for doc in range(1,len(indexDb[term])):
            #print(indexDb[term][doc][1])
            tf = indexDb[term][doc][1]
            tfIdf = math.log(1+tf, 10) * idf
            indexDb[term][doc][1] = tfIdf
    return indexDb


def genQuerytfIdf(query, indexDb, numTotalTweets):
    print(" -- Generate TF_IDF from Query --")
    print(numTotalTweets)
    squareQuery = 0
    queryDictfIdf = {}
    for term in query:
        if term in indexDb:
            df = indexDb[term][0]
            tf = 1
            tfidf = math.log(1 + tf, 10) * math.log(numTotalTweets/df, 10)
            queryDictfIdf[term] = tfidf
            squareQuery += tfidf**2
    squareQuery = math.sqrt(squareQuery)
    print("queryDictfIdf -> ", queryDictfIdf)
    print("squareQuery ->", squareQuery)
    return [queryDictfIdf, squareQuery]


def genDocsTfIdf(query, indexDb, numTotalTweets):
    print(" -- Generate DOCS_TF_IDF --")
    # Generate List Docs
    dicTweetsId_tf_idf = {}
    for term in query:
        for tweetNum in range(1,len(indexDb[term])):
            tweetId = indexDb[term][tweetNum][0]
            tf_term = indexDb[term][tweetNum][1]
            tf_Norm = math.log(1 + tf_term)
            df_term = indexDb[term][0]
            idf = math.log(numTotalTweets/df_term)
            tf_idf = tf_Norm * idf
            if tweetId not in dicTweetsId_tf_idf:
                dicTweetsId_tf_idf[tweetId] = []
            dicTweetsId_tf_idf[tweetId].append((term, tf_idf))
    print(dicTweetsId_tf_idf)
    return dicTweetsId_tf_idf

def genSquareByDoc(dicTweetsId_tf_idf):
    print(" -- Generate Square Docs --")
    dicTweetIdSquares = {}
    for tweetId in dicTweetsId_tf_idf:
        squareTweetId = 0
        for termNum in range(len(dicTweetsId_tf_idf[tweetId])):
            tf_idf = dicTweetsId_tf_idf[tweetId][termNum][1]
            squareTweetId += tf_idf**2
        squareTweetId = math.sqrt(squareTweetId)
        dicTweetIdSquares[tweetId] = squareTweetId
    print(dicTweetIdSquares)
    return dicTweetIdSquares


def genScoreCoseno(dicTweetsId_tf_idf, dicTweetIdSquares, querytfIdf_square_par):
    print(" -- genScoreCoseno -- ")
    query_tf_idf = querytfIdf_square_par[0]
    Square_query = querytfIdf_square_par[1]
    dicCosenos = {}
    for tweetId in dicTweetsId_tf_idf:
        cosenoTweetId = 0
        for numTerm in range(len(dicTweetsId_tf_idf[tweetId])):
            tf_idf = dicTweetsId_tf_idf[tweetId][numTerm][1]
            squareTweetId = dicTweetIdSquares[tweetId]
            tf_idf_norm = tf_idf/squareTweetId
            term_tweet = dicTweetsId_tf_idf[tweetId][numTerm][0]
            tf_idf_Q = query_tf_idf[term_tweet]
            tf_idf_Q_norm = tf_idf_Q / Square_query
            cosenoTweetId += (tf_idf_norm * tf_idf_Q_norm)
        dicCosenos[tweetId] = cosenoTweetId
    print(dicCosenos)
    print({k: v for k, v in sorted(dicCosenos.items(), key=lambda item: -item[1])})
    return dicCosenos


def inicial(numTotalTweets):
    #listDocument = os.listdir('prueba')
    # listTerm = ["espina", "corrupto", "fujimorista", "moral", "candidato", "miedo"]
    listResult = generateIndex(numTotalTweets)
    indexDb = listResult[0]
    numTotalTweets = listResult[1]
    for term in indexDb:
        print(term, "-->", indexDb[term])
    return listResult


def queryIndex(indexDb, query, numTotalTweets):
    print("-- Searching Query in IndexDb --")
    listDocument = os.listdir('prueba')
    querytfIdf_square_par = genQuerytfIdf(query, indexDb, numTotalTweets)
    dicTweetsId_tf_idf = genDocsTfIdf(query, indexDb, numTotalTweets)
    dicTweetIdSquares = genSquareByDoc(dicTweetsId_tf_idf)
    genScoreCoseno(dicTweetsId_tf_idf, dicTweetIdSquares, querytfIdf_square_par)
    #listCoseno = genScoreCoseno(indexDb, listDocument, queryItdf, squareByDoc)
    #print(listCoseno)
    #return listCoseno

