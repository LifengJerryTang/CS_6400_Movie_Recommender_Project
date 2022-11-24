from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

import ast
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)


def get_db_connection(host_name, username, password, database_name=None):
    return mysql.connector.connect(
        host=host_name,
        user=username,
        passwd=password,
        database=database_name
    )


def close_db_connection(db, cursor):
    db.close()
    cursor.close()


def connect_to_milvus(alias, host, port):
    print(f"Connecting to milvus; host: {host}, port: {port}")
    connections.connect(alias=alias, host=host, port=port)


def get_movie_data_from_mysql(cursor, movie_name):
    cursor.execute("SELECT * FROM movie_feature WHERE original_title = '{0}'".format(movie_name))
    return my_cursor.fetchall()[0]


def get_all_movies_from_mysql(cursor):
    cursor.execute("SELECT * FROM movie_feature")
    all_movie_data = my_cursor.fetchall()

    return all_movie_data


connect_to_milvus("default", "localhost", 19530)
movie_feature_collection = Collection("movie_feature_collection")
movie_feature_collection.load()
user_feature_collection = Collection("user_feature_collection")
user_feature_collection.load()

mysql_db = get_db_connection("localhost", "root", "kktt12345", "recommendation_features")
my_cursor = mysql_db.cursor()

all_movies_from_mysql = get_all_movies_from_mysql(my_cursor)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/mysql/<movie_name>", methods=["GET"])
def mysql_similar_movies(movie_name):
    movie_like_data = get_movie_data_from_mysql(my_cursor, movie_name)
    movie_like_feature = ast.literal_eval(movie_like_data[len(movie_like_data) - 1])

    movie_idx_similarities = []

    for i in range(len(all_movies_from_mysql)):
        curr_movie = all_movies_from_mysql[i]
        curr_movie_feature = ast.literal_eval(curr_movie[len(curr_movie) - 1])
        similarity_score = cosine_similarity([movie_like_feature], [curr_movie_feature])
        curr_movie_name = curr_movie[10]
        movie_idx_similarities.append((curr_movie_name, similarity_score[0][0]))

    movie_idx_similarities.sort(key=lambda x: x[1], reverse=True)
    print("The following movies are the movies you might like:")
    for name, _ in movie_idx_similarities[1:11]:
        print(name)

    return "Thank you!"


@app.route("/mysql/<movie_name>", methods=["GET"])
def milvus_similar_movies(movie_name):
    res = movie_feature_collection.query(
        expr="original_title in [{0}]".format(movie_name),
        output_fields=["original_title", "movie_feature"],
        consistency_level="Strong"
    )

    movie_like_feature = res[0]['movie_feature']

    search_res = movie_feature_collection.search(
        data=[movie_like_feature],
        anns_field="movie_feature",
        param={},
        offset=0,
        limit=11,
        output_fields=["original_title"],
        consistency_level="Strong"
    )

    for movie_id in search_res[0].ids:
        movie_data = movie_feature_collection.query(
            expr="id in [{0}]".format(movie_id),
            output_fields=["original_title", "movie_feature"],
            consistency_level="Strong"
        )

        print(movie_data[0]['original_title'])

    return "Thank you"

if __name__ == "__main__":
    app.run(debug=True)
