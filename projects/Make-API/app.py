from flask import Flask
from flask.json import jsonify
import random
import os

app = Flask(__name__)

@app.route("/")
def life():
    fin = open("projects/Make-API/quote.txt", "r")
    Random_line = random.randint(0, 2)
    quote = fin.readlines()[Random_line]
    return jsonify(quote[0:-1])

@app.route("/test")
def pwd():
    pwd = os.getcwd()
    return pwd


if __name__ == "__main__":
    app.run(debug=True)
