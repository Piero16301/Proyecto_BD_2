import json
import os
from nltk.stem import SnowballStemmer
import re
import codecs


def generateTokens(dirName):
    print("-- Generate Tokens --")
    listaArchivos = os.listdir(dirName)
    tokensTotales = list()
    stopwords = list()

    # Se cargan los stopwords

    stopFile = codecs.open("stoplist.txt", "r", "utf-8")
    for line in stopFile:
        line = line.strip()
        line = line.lower()
        words = line.split(" ")
        for word in words:
            if word not in stopwords:
                stopwords.append(word)

    for archivo in listaArchivos:
        with open(dirName + '/' + archivo, encoding="utf-8") as json_file:
            print("Check json File: ", json_file)
            tweets = json.load(json_file)
            for tweet in tweets:
                if tweet['retweeted'] is True:
                    texto = tweet['RT_text']
                else:
                    texto = tweet['text']
                texto = texto.strip()
                texto = re.sub('[¿|?|$|.|,|:|;|!|º|«|»|(|)|@|¡|"|😆|“|/|#|%]', '', texto)
                texto = texto.lower()
                tokens = texto.split()
                keywords = []
                for token in tokens:
                    if token in stopwords:
                        continue
                    if "http" in token:
                        continue
                    keywords.append(token)
                stemmer = SnowballStemmer('spanish')
                for token in keywords:
                    tokensTotales.append(stemmer.stem(token))
        tokensTotales = list(dict.fromkeys(tokensTotales))
    return tokensTotales

