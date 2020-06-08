from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route("/search/<string:consulta>/<string:file>")
def searchTweet(consulta, file):
    consult_formated = consulta.lower()
    file_name = os.getcwd() + "/prueba/" + file
    json_f = open(file_name, "r", encoding="utf-8")
    tweets = json.load(json_f)
    result = []
    for tweet in tweets:
        if consult_formated in tweet['text'].lower():
            result.append(tweet)
    return render_template("tweets.html", consulta=consulta, result=result)


@app.route("/search")
def searchFile():
    file_name = [{'name': 'tweets_2018-08-07.json'}, {'name': 'tweets_2018-08-08.json'},
                 {'name': 'tweets_2018-08-08.json'}]
    consulta = request.args.get("query")
    return render_template("resultado.html", consulta=consulta, files=file_name)


if __name__ == "__main__":
    app.run(debug=True)
