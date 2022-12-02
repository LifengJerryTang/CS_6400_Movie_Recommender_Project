from flask import Flask, render_template, url_for, request, redirect
import db_services.mysql_service as mysql_service
import db_services.milvus_service as milvus_service
import ast
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

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
    all_movies_from_mysql = mysql_service.get_all_movies(my_cursor)
    movie_like_data = mysql_service.get_movie_data_by_name(my_cursor, movie_name)
    movie_like_feature = ast.literal_eval(movie_like_data[len(movie_like_data) - 1])

    similar_movies_with_score = []
    return_data = []

    for i in range(len(all_movies_from_mysql)):
        curr_movie = all_movies_from_mysql[i]
        curr_movie_feature = ast.literal_eval(curr_movie[len(curr_movie) - 1])
        similarity_score = cosine_similarity([movie_like_feature], [curr_movie_feature])
        curr_movie_name = curr_movie[10]
        similar_movies_with_score.append((curr_movie_name, similarity_score[0][0]))

    similar_movies_with_score.sort(key=lambda x: x[1], reverse=True)

    for name, _ in similar_movies_with_score[1:11]:
        return_data.append(name)

    return return_data


@app.route("/similar_movies/milvus/<movie_name>", methods=["GET"])
def milvus_similar_movies(movie_name):
    movie_like_id = mysql_service.get_movie_data_by_field(my_cursor, "id", "original_title", movie_name)[0]

    res = milvus_service.query_collection(movie_feature_collection, query_string="id in [{0}]".format(movie_like_id),
                                          output_fields=["original_title", "movie_feature"])

    movie_like_feature = res[0]['movie_feature']
    similar_movie_names = []

    search_res = milvus_service.perform_similarity_search(collection=movie_feature_collection,
                                                          feature_vector=movie_like_feature,
                                                          anns_field="movie_feature",
                                                          output_fields=["original_title"],
                                                          offset=0, limit=11)
    for movie_id in search_res[0].ids:
        movie_data = milvus_service.query_collection(movie_feature_collection,
                                                     query_string="id in [{0}]".format(movie_id),
                                                     output_fields=["original_title", "movie_feature"])

        if movie_id == movie_like_id:
            continue

        similar_movie_names.append(movie_data[0]['original_title'])

    return similar_movie_names


@app.route("/similar_users/mysql/<user_id>", methods=["GET"])
def mysql_similar_users(user_id):
    all_users_from_mysql = mysql_service.get_all_users(my_cursor)
    user_data = mysql_service.get_user_data_by_id(my_cursor, user_id)
    user_feature = ast.literal_eval(user_data[len(user_data) - 1])
    return_data = []
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

        return_data.append(curr_user_id)

    return return_data


@app.route("/similar_users/milvus/<user_id>", methods=["GET"])
def milvus_similar_users(user_id):
    res = milvus_service.query_collection(user_feature_collection, query_string="user_id in [{0}]".format(user_id),
                                          output_fields=["user_id", "user_feature_20100101"])

    user_feature = res[0]['user_feature_20100101']

    search_res = milvus_service.perform_similarity_search(collection=user_feature_collection,
                                                          feature_vector=user_feature,
                                                          anns_field="user_feature_20100101",
                                                          output_fields=["user_id"],
                                                          offset=0, limit=11)
    return_data = list(search_res[0].ids)

    return_data.pop(0)

    return return_data


@app.route("/recommended_movies_for_user/mysql/<user_id>", methods=["GET"])
def mysql_recommended_movies_for_user(user_id):
    all_movies_from_mysql = mysql_service.get_all_movies(my_cursor)
    user_data = mysql_service.get_user_data_by_id(my_cursor, user_id)
    user_feature = ast.literal_eval(user_data[len(user_data) - 1])

    return_data = []
    recommended_movies_with_Score = []

    for i in range(len(all_movies_from_mysql)):
        curr_movie = all_movies_from_mysql[i]
        curr_movie_feature = ast.literal_eval(curr_movie[len(curr_movie) - 1])
        similarity_score = cosine_similarity([user_feature], [curr_movie_feature])
        curr_movie_name = curr_movie[10]
        recommended_movies_with_Score.append((curr_movie_name, similarity_score[0][0]))

    recommended_movies_with_Score.sort(key=lambda x: x[1], reverse=True)

    for name, _ in recommended_movies_with_Score[1:11]:
        return_data.append(name)

    return return_data


if __name__ == "__main__":
    app.run(debug=True)
