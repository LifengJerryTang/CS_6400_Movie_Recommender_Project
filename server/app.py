from flask import Flask, render_template, url_for, request, redirect
import db_services.mysql_service as mysql_service
import db_services.milvus_service as milvus_service
import ast
import time
import json
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

milvus_service.connect_to_milvus("default", "localhost", 19530)
movie_feature_collection = milvus_service.get_collection("movie_feature_collection")
user_feature_collection = milvus_service.get_collection("user_feature_collection")

db = mysql_service.get_connection("localhost", "root", "kktt12345", "recommendation_features")
my_cursor = db.cursor()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/similar_movies/mysql/<movie_name>", methods=["GET"])
def mysql_similar_movies(movie_name):
    start_time = time.time()

    all_movies_from_mysql = mysql_service.get_all_movies(my_cursor)
    movie_like_data = mysql_service.get_movie_data_by_name(my_cursor, movie_name)
    movie_like_feature = ast.literal_eval(movie_like_data[len(movie_like_data) - 1])

    similar_movies_with_score = []
    similar_movies_data = []

    for i in range(len(all_movies_from_mysql)):
        curr_movie = all_movies_from_mysql[i]
        curr_movie_feature = ast.literal_eval(curr_movie[len(curr_movie) - 1])
        similarity_score = cosine_similarity([movie_like_feature], [curr_movie_feature])
        curr_movie_name = curr_movie[10]
        curr_movie_casts = curr_movie[0]
        curr_movie_keywords = curr_movie[2]
        curr_movie_genres = curr_movie[6]
        movie_data = {
            "name": curr_movie_name,
            "genres": curr_movie_genres,
            "casts": curr_movie_casts,
            "keywords": curr_movie_keywords
        }
        similar_movies_with_score.append((movie_data, similarity_score[0][0]))

    similar_movies_with_score.sort(key=lambda x: x[1], reverse=True)

    for movie_data, _ in similar_movies_with_score[1:11]:
        similar_movies_data.append(movie_data)

    runtime = time.time() - start_time

    return_data = {
        "runtime": runtime,
        "movies": similar_movies_data
    }

    return return_data


@app.route("/similar_movies/milvus/<movie_name>", methods=["GET"])
def milvus_similar_movies(movie_name):
    start_time = time.time()

    movie_like_id = mysql_service.get_movie_data_by_field(my_cursor, "id", "original_title", movie_name)[0]

    res = milvus_service.query_collection(movie_feature_collection, query_string="id in [{0}]".format(movie_like_id),
                                          output_fields=["original_title", "movie_feature"])

    movie_like_feature = res[0]['movie_feature']
    similar_movies_data = []

    search_res = milvus_service.perform_similarity_search(collection=movie_feature_collection,
                                                          feature_vector=movie_like_feature,
                                                          anns_field="movie_feature",
                                                          output_fields=["original_title"],
                                                          offset=0, limit=11)
    for movie_id in search_res[0].ids:
        movie_all_data = milvus_service.query_collection(movie_feature_collection,
                                                     query_string="id in [{0}]".format(movie_id),
                                                     output_fields=["original_title", "movie_feature",
                                                                    "genres", "cast", "keywords"])

        if movie_id == movie_like_id:
            continue

        print(movie_all_data)

        movie_data = {
            "name":  movie_all_data[0]['original_title'],
            "genres":  movie_all_data[0]['genres'],
            "casts": movie_all_data[0]['cast'],
            "keywords":movie_all_data[0]['keywords']
        }

        similar_movies_data.append(movie_data)

    runtime = time.time() - start_time

    return_data = {
        "runtime": runtime,
        "movies": similar_movies_data
    }

    return return_data


@app.route("/similar_users/mysql/<user_id>", methods=["GET"])
def mysql_similar_users(user_id):
    start_time = time.time()

    all_users_from_mysql = mysql_service.get_all_users(my_cursor)
    user_data = mysql_service.get_user_data_by_id(my_cursor, user_id)
    user_feature = ast.literal_eval(user_data[len(user_data) - 1])
    user_ids = []
    user_idx_similarities = []

    for i in range(len(all_users_from_mysql)):
        curr_user = all_users_from_mysql[i]
        curr_user_feature = ast.literal_eval(curr_user[len(curr_user) - 1])
        similarity_score = cosine_similarity([user_feature], [curr_user_feature])
        curr_user_id = curr_user[0]
        user_idx_similarities.append((curr_user_id, similarity_score[0][0]))

    user_idx_similarities.sort(key=lambda x: x[1], reverse=True)

    for curr_user_id, _ in user_idx_similarities[1:11]:
        if curr_user_id == user_id:
            continue

        user_ids.append(curr_user_id)

    runtime = time.time() - start_time

    return_data = {
        "runtime": runtime,
        "user_ids": user_ids
    }

    return return_data


@app.route("/similar_users/milvus/<user_id>", methods=["GET"])
def milvus_similar_users(user_id):
    start_time = time.time()
    res = milvus_service.query_collection(user_feature_collection, query_string="user_id in [{0}]".format(user_id),
                                          output_fields=["user_id", "user_feature_20100101"])

    user_feature = res[0]['user_feature_20100101']

    search_res = milvus_service.perform_similarity_search(collection=user_feature_collection,
                                                          feature_vector=user_feature,
                                                          anns_field="user_feature_20100101",
                                                          output_fields=["user_id"],
                                                          offset=0, limit=11)
    user_ids = list(search_res[0].ids)

    user_ids.pop(0)

    runtime = time.time() - start_time

    return_data = {
        "runtime": runtime,
        "user_ids": user_ids
    }

    return return_data


@app.route("/recommended_movies_for_user/mysql/<user_id>", methods=["GET"])
def mysql_recommended_movies_for_user(user_id):
    start_time = time.time()
    all_movies_from_mysql = mysql_service.get_all_movies(my_cursor)
    user_data = mysql_service.get_user_data_by_id(my_cursor, user_id)
    user_feature = ast.literal_eval(user_data[len(user_data) - 1])

    recommended_movies_data = []
    recommended_movies_with_Score = []

    for i in range(len(all_movies_from_mysql)):
        curr_movie = all_movies_from_mysql[i]
        curr_movie_feature = ast.literal_eval(curr_movie[len(curr_movie) - 1])
        similarity_score = cosine_similarity([user_feature], [curr_movie_feature])
        curr_movie_name = curr_movie[10]
        curr_movie_casts = curr_movie[0].split("name")
        curr_movie_keywords = curr_movie[2].split(",")
        curr_movie_genres = curr_movie[6].split(",")
        casts = []
        genres = []
        keywords = []


        for cast in curr_movie_casts:
            if 'order' in cast:
                idx_1 = cast.index(":")
                idx_2 = cast.index("order")
                casts.append(cast[idx_1 + 1: idx_2 - 3])

        for genre in curr_movie_genres:
            if 'name' in genre:
                idx_1 = genre.index(":")
                idx_2 = genre.index("}")
                genres.append(genre[idx_1 + 2: idx_2 - 1])

        for keyword in curr_movie_keywords:
            if 'name' in keyword:
                idx_1 = keyword.index(":")
                idx_2 = keyword.index("}")
                keywords.append(keyword[idx_1 + 2: idx_2 - 1])

        movie_data = {
            "name": curr_movie_name,
            "genres": genres,
            "casts": casts,
            "keywords": keywords
        }
        recommended_movies_with_Score.append((movie_data, similarity_score[0][0]))

    recommended_movies_with_Score.sort(key=lambda x: x[1], reverse=True)

    for movie_data, _ in recommended_movies_with_Score[1:11]:
        recommended_movies_data.append(movie_data)

    runtime = time.time() - start_time

    return_data = {
        "runtime": runtime,
        "movies": recommended_movies_data
    }

    return return_data


@app.route("/recommended_movies_for_user/milvus/<user_id>", methods=["GET"])
def milvus_recommended_movies_for_user(user_id):
    start_time = time.time()
    res = milvus_service.query_collection(user_feature_collection, query_string="user_id in [{0}]".format(user_id),
                                          output_fields=["user_id", "user_feature_20100101"])

    user_feature = res[0]['user_feature_20100101']

    recommended_movies_data = []

    search_res = milvus_service.perform_similarity_search(collection=movie_feature_collection,
                                                          feature_vector=user_feature,
                                                          anns_field="movie_feature",
                                                          output_fields=["original_title"],
                                                          offset=0, limit=11)
    for movie_id in search_res[0].ids:
        movie_all_data = milvus_service.query_collection(movie_feature_collection,
                                                     query_string="id in [{0}]".format(movie_id),
                                                     output_fields=["original_title", "movie_feature",
                                                                        "genres", "cast", "keywords"])

        movie_data = {
            "name": movie_all_data[0]['original_title'],
            "genres": movie_all_data[0]['genres'],
            "casts": movie_all_data[0]['cast'],
            "keywords": movie_all_data[0]['keywords']
        }

        recommended_movies_data.append(movie_data)

    runtime = time.time() - start_time

    return_data = {
        "runtime": runtime,
        "movies": recommended_movies_data
    }

    return return_data


if __name__ == "__main__":
    app.run(debug=True)
