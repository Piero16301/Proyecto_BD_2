import json


def saveIndex(indexDB):
    with open('indice/index.json', 'w', encoding="utf-8") as index:
        json.dump(indexDB, index)


def readIndex():
    with open('indice/index.json', 'r', encoding="utf-8") as json_file:
        index = json.load(json_file)
        return index
