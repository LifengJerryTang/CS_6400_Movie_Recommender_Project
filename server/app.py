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


def get_movie_data_mysql(cursor, movie_name):
    cursor.execute("SELECT * FROM movie_feature WHERE original_title = '{0}'".format(movie_name))
    return my_cursor.fetchall()[0]


def get_all_movies_mysql(cursor):
    cursor.execute("SELECT * FROM movie_feature")
    all_movie_data = my_cursor.fetchall()

    return all_movie_data


def get_movie_data_by_field_mysql(cursor, field_1, field_2, field_2_data):
    query = """SELECT {0} FROM movie_feature WHERE {1} = '{2}' """.format(field_1, field_2, field_2_data)
    cursor.execute(query)

    return my_cursor.fetchall()[0]


connect_to_milvus("default", "localhost", 19530)
movie_feature_collection = Collection("movie_feature_collection")
movie_feature_collection.load()
user_feature_collection = Collection("user_feature_collection")
user_feature_collection.load()

mysql_db = get_db_connection("localhost", "root", "kktt12345", "recommendation_features")
my_cursor = mysql_db.cursor()

all_movies_from_mysql = get_all_movies_mysql(my_cursor)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/mysql/<movie_name>", methods=["GET"])
def mysql_similar_movies(movie_name):
    movie_like_data = get_movie_data_mysql(my_cursor, movie_name)
    movie_like_feature = ast.literal_eval(movie_like_data[len(movie_like_data) - 1])

    movie_idx_similarities = []

    for i in range(len(all_movies_from_mysql)):
        curr_movie = all_movies_from_mysql[i]
        curr_movie_feature = ast.literal_eval(curr_movie[len(curr_movie) - 1])
        similarity_score = cosine_similarity([movie_like_feature], [curr_movie_feature])
        curr_movie_name = curr_movie[10]
        movie_idx_similarities.append((curr_movie_name, similarity_score[0][0]))

    movie_idx_similarities.sort(key=lambda x: x[1], reverse=True)

    return_data = []

    for name, _ in movie_idx_similarities[1:11]:
        return_data.append(name)

    return return_data


@app.route("/milvus/<movie_name>", methods=["GET"])
def milvus_similar_movies(movie_name):
    movie_like_id = get_movie_data_by_field_mysql(my_cursor, "id", "original_title", movie_name)[0]

    res = movie_feature_collection.query(
        expr="id in [{0}]".format(movie_like_id),
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

    return_data = []

    for movie_id in search_res[0].ids:
        movie_data = movie_feature_collection.query(
            expr="id in [{0}]".format(movie_id),
            output_fields=["original_title", "movie_feature"],
            consistency_level="Strong"
        )

        if movie_id == movie_like_id:
            continue

        return_data.append(movie_data[0]['original_title'])

    return return_data


if __name__ == "__main__":
    app.run(debug=True)
