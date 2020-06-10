import json
import os
import math
import re
import pandas as pd
from Preprocesamiento import generateTokens
from nltk.stem import SnowballStemmer

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
    dirName = 'prueba'
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
            text = re.sub('[¿|?|$|.|,|:|;|!|º|«|»|(|)|@|¡|"|😆|“|/|#|%]', '', text)
            text = text.split()
            stemmer = SnowballStemmer('spanish')
            for word in text:
                red_word = stemmer.stem(word)
                if red_word in listTerm:    ## si es keyword
                    if tweet['id'] in indexDb[red_word][1]:
                        indexDb[red_word][1][tweet['id']] += 1      # Update tf de keyword (word) en tweetId
                    else:
                        indexDb[red_word][1][tweet['id']] = 1       # init tf de keyword (word) en tweetId
                        indexDb[red_word][0] += 1  # Update Document Frequency
        fjson.close()
    print(indexDb)
    return [indexDb, numTotalTweets]


def stemQuery(text):
    query_result = []
    stemmer = SnowballStemmer('spanish')
    text = text.strip()
    text = text.lower()
    text = re.sub('[¿|?|$|.|,|:|;|!|º|«|»|(|)|@|¡|"|😆|“|/|#|%]', '', text)
    text = text.split()
    for term in text:
        query_result.append(stemmer.stem(term))
    return query_result


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
        for tweetId in indexDb[term][1]:
            tf_term = indexDb[term][1][tweetId]
            tf_norm = math.log(1 + tf_term)
            df_term = indexDb[term][0]
            idf = math.log(numTotalTweets / df_term)
            tf_idf = tf_norm * idf
            if tweetId not in dicTweetsId_tf_idf:
                dicTweetsId_tf_idf[tweetId] = {}
            dicTweetsId_tf_idf[tweetId][term] = tf_idf
    print(dicTweetsId_tf_idf)
    return dicTweetsId_tf_idf


def genSquareByDoc(dicTweetsId_tf_idf):
    print(" -- Generate Square Docs --")
    dicTweetIdSquares = {}
    for tweetId in dicTweetsId_tf_idf:
        squareTweetId = 0
        for term in dicTweetsId_tf_idf[tweetId]:
            tf_idf = dicTweetsId_tf_idf[tweetId][term]
            squareTweetId += tf_idf**2
        squareTweetId = math.sqrt(squareTweetId)
        dicTweetIdSquares[tweetId] = squareTweetId
    print(dicTweetIdSquares)
    return dicTweetIdSquares


def genScoreCoseno(dicTweetsId_tf_idf, dicTweetIdSquares, querytfIdf_square_par):
    print(" -- genScoreCoseno -- ")
    query_tf_idf = querytfIdf_square_par[0]     # return dict -> query_tf_idf
    Square_query = querytfIdf_square_par[1]
    dicCosenos = {}
    for tweetId in dicTweetsId_tf_idf:
        cosenoTweetId = 0
        for term in dicTweetsId_tf_idf[tweetId]:
            tf_idf = dicTweetsId_tf_idf[tweetId][term]
            squareTweetId = dicTweetIdSquares[tweetId]
            tf_idf_norm = tf_idf/squareTweetId
            tf_idf_Q = query_tf_idf[term]
            tf_idf_Q_norm = tf_idf_Q / Square_query
            cosenoTweetId += (tf_idf_norm * tf_idf_Q_norm)
        dicCosenos[tweetId] = round(cosenoTweetId, 4)
    dicCosenos = {k: v for k, v in sorted(dicCosenos.items(), key=lambda item: -item[1])}
    return dicCosenos


def inicial(numTotalTweets):
    listResult = generateIndex(numTotalTweets)
    indexDb = listResult[0]
    numTotalTweets = listResult[1]
    for term in indexDb:
        print(term, "-->", indexDb[term])
    return listResult


def queryIndex(indexDb, query_str, numTotalTweets):
    print("-- Searching Query in IndexDb --")
    listDocument = os.listdir('prueba')
    query = stemQuery(query_str)
    querytfIdf_square_par = genQuerytfIdf(query, indexDb, numTotalTweets)
    dicTweetsId_tf_idf = genDocsTfIdf(query, indexDb, numTotalTweets)
    dicTweetIdSquares = genSquareByDoc(dicTweetsId_tf_idf)
    dicScoreCoseno = genScoreCoseno(dicTweetsId_tf_idf, dicTweetIdSquares, querytfIdf_square_par)
    print(dicScoreCoseno)
    return dicScoreCoseno

