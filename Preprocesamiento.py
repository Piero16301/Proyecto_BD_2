import json
import os
import nltk

listaArchivos = os.listdir('prueba')

for archivo in listaArchivos:
    with open('prueba/' + archivo) as json_file:
        tweets = json.load(json_file)
        for tweet in tweets:
            if tweet['retweeted'] is True:
                print('Texto: ' + tweet['RT_text'])
            else:
                print('Texto: ' + tweet['text'])
print("Test")
