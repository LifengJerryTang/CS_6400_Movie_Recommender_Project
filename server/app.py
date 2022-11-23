from flask import Flask, render_template
import mysql.connector
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

import ast

app = Flask(__name__)

@app.route("/")
def index():
    print("Hello")
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)