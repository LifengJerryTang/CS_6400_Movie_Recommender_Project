import mysql.connector

from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
import ast

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Start connecting to milvus")
connections.connect("default", host="localhost", port="19530")

movie_feature_collection = Collection("movie_feature_collection")
movie_feature_collection.load()

movie_like = 'Batman'

res = movie_feature_collection.query(
    expr="original_title in [{0}]".format(movie_like),
    output_fields=["original_title", "movie_feature"],
    consistency_level="Strong"
)

batman_feature = res[0]['movie_feature']


search_res = movie_feature_collection.search(
	data=[batman_feature],
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

    if movie_id == 268:
        continue
    print(movie_data[0]['original_title'])

connections.disconnect("default")