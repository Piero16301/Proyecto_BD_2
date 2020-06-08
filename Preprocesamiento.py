import json
import os
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re

listaArchivos = os.listdir('prueba')

tokensTotales = list()

for archivo in listaArchivos:
    with open('prueba/' + archivo) as json_file:
        tweets = json.load(json_file)
        for tweet in tweets:
            if tweet['retweeted'] is True:
                texto = tweet['RT_text']
            else:
                texto = tweet['text']
            texto = texto.strip()
            texto = re.sub('[¿|?|$|.|,|:|;|!|º|«|»|(|)|@|¡|"|😆|/|#]', '', texto)
            texto = texto.lower()
            tokens = texto.split()
            sr = stopwords.words('spanish')
            for token in tokens:
                if token in stopwords.words('spanish'):
                    tokens.remove(token)
                if token.find("http") == 0:
                    tokens.remove(token)
            spanish_stemmer = SnowballStemmer('spanish')
            for token in tokens:
                tokensTotales.append(spanish_stemmer.stem(token))

            tokensTotales = list(dict.fromkeys(tokensTotales))

print(tokensTotales)
