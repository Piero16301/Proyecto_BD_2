from flask import Flask, render_template, request
from indexDB import inicial, queryIndex
from tweets import getTweet

app = Flask(__name__)

numTotalTweets = 0
listResult = inicial(numTotalTweets)
indice = listResult[0]
numTotalTweets = listResult[1]
print("Front: ", numTotalTweets)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route("/search")
def searchFile():
    query = request.args.get("query")
    tweets = queryIndex(indice, query, numTotalTweets)
    return render_template("resultado.html", consulta=query, tweets=tweets)


@app.route("/search/<string:consulta>/<int:tweet_id>")
def searchTweet(consulta, tweet_id):
    consult_formated = consulta.lower()
    tweet = getTweet(str(tweet_id))
    return render_template("tweets.html", consulta=consulta, tweet_id = tweet_id, tweet = tweet)


if __name__ == "__main__":
    app.run(debug=True, use_reloader = False)
