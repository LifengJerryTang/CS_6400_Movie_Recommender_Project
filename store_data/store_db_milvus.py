# hello_milvus.py demonstrates the basic operations of PyMilvus, a Python SDK of Milvus.
# 1. connect to Milvus
# 2. create collection
# 3. insert data
# 4. create index
# 5. search, query, and hybrid search on entities
# 6. delete entities by PK
# 7. drop collection
import time
import csv
import ast

import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

import pandas as pd

fmt = "\n=== {:30} ===\n"
search_latency_fmt = "search latency = {:.4f}s"
num_entities, dim = 3000, 8

#################################################################################
# 1. connect to Milvus
# Add a new connection alias `default` for Milvus server in `localhost:19530`
# Actually the "default" alias is a buildin in PyMilvus.
# If the address of Milvus is the same as `localhost:19530`, you can omit all
# parameters and call the method as: `connections.connect()`.
#
# Note: the `using` parameter of the following methods is default to "default".
print(fmt.format("start connecting to Milvus"))
connections.connect("default", host="localhost", port="19530")

#################################################################################
# 2. create collection(s)
"""
    Example:
    
    We're going to create a collection with 3 fields.
    +-+------------+------------+------------------+------------------------------+
    | | field name | field type | other attributes |       field description      |
    +-+------------+------------+------------------+------------------------------+
    |1|    "pk"    |   VarChar  |  is_primary=True |      "primary field"         |
    | |            |            |   auto_id=False  |                              |
    +-+------------+------------+------------------+------------------------------+
    |2|  "random"  |    Double  |                  |      "a double field"        |
    +-+------------+------------+------------------+------------------------------+
    |3|"embeddings"| FloatVector|     dim=8        |  "float vector with dim 8"   |
    +-+------------+------------+------------------+------------------------------+
    
    fields = [
        FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
        FieldSchema(name="random", dtype=DataType.DOUBLE),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]
    
    schema = CollectionSchema(fields, "hello_milvus is the simplest demo to introduce the APIs")

    print(fmt.format("Create collection `hello_milvus`"))
    hello_milvus = Collection("hello_milvus", schema, consistency_level="Strong")
    
"""

movie_feature_fields = [
    FieldSchema(name="cast", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="crew", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="keywords", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="adult", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="belongs_to_collection", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="budget", dtype=DataType.INT64),  # <class 'int'>
    FieldSchema(name="genres", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="homepage", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),  # <class 'int'>
    FieldSchema(name="original_language", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="original_title", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="overview", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="popularity", dtype=DataType.INT64),  # <class 'int'>
    FieldSchema(name="poster_path", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="production_companies", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="production_countries", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="release_date", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="release_date_timestamp", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="have_release_date", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="revenue", dtype=DataType.INT64),  # <class 'int'>
    FieldSchema(name="runtime", dtype=DataType.INT64),  # <class 'int'>
    FieldSchema(name="spoken_languages", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="status", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="tagline", dtype=DataType.VARCHAR, max_length=10000),  # <class 'str'>
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=10000),
    FieldSchema(name="vote_average", dtype=DataType.INT64),
    FieldSchema(name="vote_count", dtype=DataType.INT64),
    FieldSchema(name="movie_feature", dtype=DataType.FLOAT_VECTOR, dim=128)

]

utility.drop_collection("movie_feature_collection")
movie_feature_schema = CollectionSchema(movie_feature_fields, "Description: schema for movie feature data")
movie_feature_collection = Collection("movie_feature_collection", movie_feature_schema, consistency_level="Strong")

user_feature_fields = [
    FieldSchema(name="user_id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="user_feature_20230101", dtype=DataType.VARCHAR, max_length=10000),
    FieldSchema(name="user_feature_20220101", dtype=DataType.VARCHAR, max_length=10000),
    FieldSchema(name="user_feature_20200101", dtype=DataType.VARCHAR, max_length=10000),
    FieldSchema(name="user_feature_20150101", dtype=DataType.VARCHAR, max_length=10000),
    FieldSchema(name="user_feature_20100101", dtype=DataType.FLOAT_VECTOR, dim=128)
]

utility.drop_collection("user_feature_collection")
user_feature_schema = CollectionSchema(user_feature_fields, "Description: schema for movie user feature data")
user_feature_collection = Collection("user_feature_collection", user_feature_schema, consistency_level="Strong")

################################################################################
# 3. insert data
# We are going to insert 3000 rows of data into `hello_milvus`
# Data to be inserted must be organized in fields.
#
# The insert() method returns:
# - either automatically generated primary keys by Milvus if auto_id=True in the schema;
# - or the existing primary key field from the entities if auto_id=False in the schema.
"""
    Example: 
    print(fmt.format("Start inserting entities"))
    rng = np.random.default_rng(seed=19530)
    entities = [
        # provide the pk field because `auto_id` is set to False
        [str(i) for i in range(num_entities)],
        rng.random(num_entities).tolist(),  # field random, only supports list
        rng.random((num_entities, dim)),    # field embeddings, supports numpy.ndarray and list
    ]

insert_result = hello_milvus.insert(entities)

print(f"Number of entities in Milvus: {hello_milvus.num_entities}")  # check the num_entites
"""

start_time = time.time()

print("Inserting movie feature data into milvus..")

with open('data/movie_feature_calculated.csv', encoding='utf8', newline='') as csvfile:
    movie_features = csv.reader(csvfile)
    next(movie_features, None)

    it = 0

    for movie_feature in movie_features:

        data_arr = list(movie_feature)
        if len(data_arr) < 29:
            continue

        if it > 20000:
            break

        data_arr.pop(0)

        insert_data = []
        long_data_exists = False
        numeric_columns_idx = [5, 8, 12, 19, 20, 25, 26]

        for col in range(len(data_arr)):
            data = str(data_arr[col])
            # The data has to be numeric and the current column is a column that contains number
            if data.isnumeric() and col in numeric_columns_idx:
                data = int(data)
            else:
                data = data.replace("'", " ")
                if len(data) > 10000:
                    long_data_exists = True
                    break

            data_arr[col] = data

        if long_data_exists:
            continue

        data_arr[len(data_arr) - 1] = ast.literal_eval(data_arr[len(data_arr) - 1])

        for data in data_arr:
            insert_data.append([data])

        movie_feature_collection.insert(insert_data)
        it += 1


print("Inserting user feature data into milvus")

with open("data/user_feature_calculated.csv", encoding='utf8', newline='') as csvfile:
    user_features = csv.reader(csvfile)
    next(user_features, None)  # skips the header

    it = 0

    for _, userId, user_feature_20230101, \
        user_feature_20220101, user_feature_20200101, \
        user_feature_20150101, user_feature_20100101 in user_features:

        if it > 20000:
            break

        userId = int(userId)

        user_feature_20100101 = ast.literal_eval(user_feature_20100101)
        insert_data = [[userId], [user_feature_20230101], [user_feature_20220101],
                       [user_feature_20200101], [user_feature_20150101], [user_feature_20100101]]

        user_feature_collection.insert(insert_data)
        it += 1


runtime = time.time() - start_time

print("Insertion runtime (milvus) ", runtime)