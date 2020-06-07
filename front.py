from flask import Flask, render_template, request
from tweets import tweets

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route("/search")
def search():
    consulta = request.args.get("query").lower()
    result = []
    for re in tweets:
        if consulta in re['text'].lower():
            result.append(re)
    return render_template("resultado.html", consulta=consulta, result=result)


if __name__ == "__main__":
    app.run(debug=True)
