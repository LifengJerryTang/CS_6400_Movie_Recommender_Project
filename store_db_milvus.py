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
# 2. create collection
# We're going to create a collection with 3 fields.
# +-+------------+------------+------------------+------------------------------+
# | | field name | field type | other attributes |       field description      |
# +-+------------+------------+------------------+------------------------------+
# |1|    "pk"    |   VarChar  |  is_primary=True |      "primary field"         |
# | |            |            |   auto_id=False  |                              |
# +-+------------+------------+------------------+------------------------------+
# |2|  "random"  |    Double  |                  |      "a double field"        |
# +-+------------+------------+------------------+------------------------------+
# |3|"embeddings"| FloatVector|     dim=8        |  "float vector with dim 8"   |
# +-+------------+------------+------------------+------------------------------+

"""
    Example:
    
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
    FieldSchema(name="cast", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="crew", dtype=DataType.VARCHAR, max_length=10000),#<class 'str'>
    FieldSchema(name="keywords", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="adult", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="belongs_to_collection", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="budget", dtype=DataType.INT64), #<class 'int'>
    FieldSchema(name="genres", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="homepage", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False), #<class 'int'>
    FieldSchema(name="original_language", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="original_title", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="overview", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="popularity", dtype=DataType.INT64), #<class 'int'>
    FieldSchema(name="poster_path", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="production_companies", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="production_countries", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="release_date", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="release_date_timestamp", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="have_release_date", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="revenue", dtype=DataType.INT64), #<class 'int'>
    FieldSchema(name="runtime", dtype=DataType.INT64), #<class 'int'>
    FieldSchema(name="spoken_languages", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="status", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="tagline", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=10000), #<class 'str'>
    FieldSchema(name="vote_average", dtype=DataType.INT64), #<class 'int'>
    FieldSchema(name="vote_count", dtype=DataType.INT64), #<class 'int'>
    FieldSchema(name="movie_feature", dtype=DataType.FLOAT_VECTOR,  dim=128) #<class 'list'>

]

utility.drop_collection("movie_feature_collection")
movie_feature_schema = CollectionSchema(movie_feature_fields, "Description: schema for movie feature data")
movie_feature_collection = Collection("movie_feature_collection", movie_feature_schema, consistency_level="Strong")

user_feature_fields = [
    FieldSchema(name="user_id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="user_feature_20230101", dtype=DataType.VARCHAR, max_length=1000),
    FieldSchema(name="user_feature_20220101", dtype=DataType.VARCHAR, max_length=1000),
    FieldSchema(name="user_feature_20200101", dtype=DataType.VARCHAR, max_length=1000),
    FieldSchema(name="user_feature_20150101", dtype=DataType.VARCHAR, max_length=1000),
    FieldSchema(name="user_feature_20100101", dtype=DataType.FLOAT_VECTOR,  dim=1),
]

utility.drop_collection("rating_feature_collection")
user_feature_schema = CollectionSchema(user_feature_fields, "Description: schema for movie rating feature data")
user_feature_collection = Collection("rating_feature_collection", user_feature_schema, consistency_level="Strong")

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
# rng = np.random.default_rng(seed=19530)
# stuff = rng.random((num_entities, 4))
#
# for s in stuff:
#     print(s)

# print(len([-19.515625, 87.9375, -96.5625, -54.09375, 86.8125, 8.8359375, -18.328125, -21.828125, -38.25, -3.833984375, -37.75, 19.15625, -11.875, -63.5625, -58.78125, -26.71875, -43.0625, -25.296875, 1.353515625, 1.0546875, -23.34375, 23.140625, 6.0546875, -34.34375, 26.375, -54.4375, -26.4375, 55.03125, 33.84375, -44.40625, 63.78125, -21.65625, -63.65625, 53.96875, 12.296875, 3.572265625, -6.0546875, 20.625, -13.984375, 30.9375, 53.0625, 4.421875, -18.5, -51.75, 96.875, 31.875, -40.9375, -39.3125, 11.453125, 76.5, 39.09375, -0.68896484375, 5.61328125, 15.359375, 9.828125, -41.8125, 22.734375, -1.5390625, -28.546875, 17.265625, 3.35546875, -71.75, 11.546875, 48.75, -33.59375, -7.50390625, -53.59375, -24.828125, -12.1484375, 17.515625, 16.65625, -48.25, -51.65625, -16.015625, -75.125, -28.140625, -47.96875, -45.34375, 57.4375, 39.15625, -84.3125, -47.5625, 17.1875, 2.8046875, 19.359375, -82.4375, 48.875, -2.802734375, 20.921875, 31.421875, 69.6875, 37.1875, 36.71875, 86.625, -20.96875, 27.359375, 28.28125, -1.5966796875, 26.90625, -23.125, -37.6875, 18.921875, 2.3515625, 70.125, 56.34375, 20.015625, 23.421875, 86.0, -52.71875, -19.140625, -7.84375, -81.9375, -12.2421875, -50.71875, 21.71875, 18.90625, -15.3125, 3.421875, -23.484375, -58.09375, -28.671875, -14.4609375, -46.6875, -46.8125, 33.65625, -28.09375, 50.40625, 19.28125]))
#
# movie_feature_collection.insert([
#     ["dsd"],
#     ["dsd"],
#     ["dsd"],
#     ["dsd"],
#     ["dsd"],
#     [2],
#     ["dsd"],
#     ["dsd"],
#     [1],
#     ["dsd"],
#     ["dsd"],
#     ["dsd"],
#     [3],
#     ["dsd"],
#     ["dsd"],
#     ["dsd"],
#     ["dsd"],
#     [2],
#     ["dsd"],
#     [4],
#     [5],
#     ["dsd"],
#     ["dsd"],
#     ["dsd"],
#     ["dsd"],
#     [2],
#      [9],
#     [[-19.515625, 87.9375, -96.5625, -54.09375, 86.8125, 8.8359375, -18.328125, -21.828125, -38.25, -3.833984375, -37.75, 19.15625, -11.875, -63.5625, -58.78125, -26.71875, -43.0625, -25.296875, 1.353515625, 1.0546875, -23.34375, 23.140625, 6.0546875, -34.34375, 26.375, -54.4375, -26.4375, 55.03125, 33.84375, -44.40625, 63.78125, -21.65625, -63.65625, 53.96875, 12.296875, 3.572265625, -6.0546875, 20.625, -13.984375, 30.9375, 53.0625, 4.421875, -18.5, -51.75, 96.875, 31.875, -40.9375, -39.3125, 11.453125, 76.5, 39.09375, -0.68896484375, 5.61328125, 15.359375, 9.828125, -41.8125, 22.734375, -1.5390625, -28.546875, 17.265625, 3.35546875, -71.75, 11.546875, 48.75, -33.59375, -7.50390625, -53.59375, -24.828125, -12.1484375, 17.515625, 16.65625, -48.25, -51.65625, -16.015625, -75.125, -28.140625, -47.96875, -45.34375, 57.4375, 39.15625, -84.3125, -47.5625, 17.1875, 2.8046875, 19.359375, -82.4375, 48.875, -2.802734375, 20.921875, 31.421875, 69.6875, 37.1875, 36.71875, 86.625, -20.96875, 27.359375, 28.28125, -1.5966796875, 26.90625, -23.125, -37.6875, 18.921875, 2.3515625, 70.125, 56.34375, 20.015625, 23.421875, 86.0, -52.71875, -19.140625, -7.84375, -81.9375, -12.2421875, -50.71875, 21.71875, 18.90625, -15.3125, 3.421875, -23.484375, -58.09375, -28.671875, -14.4609375, -46.6875, -46.8125, 33.65625, -28.09375, 50.40625, 19.28125]]
# ])

#



with open('data/movie_feature_calculated.csv', encoding='utf8', newline='') as csvfile:
    movie_features = csv.reader(csvfile)
    next(movie_features, None)

    it = 0

    for movie_feature in movie_features:

        data_arr = list(movie_feature)
        if len(data_arr) < 29:
            continue

        if it > 1000000:
            break

        data_arr.pop(0)

        insert_data = []

        print("Iteration\n\n", it)

        try:
            for i in range(len(data_arr)):
                data = str(data_arr[i])

                if data.isnumeric():
                    data = int(data)

                data_arr[i] = data
        except:
            continue

        data_arr[len(data_arr) - 1] = ast.literal_eval(data_arr[len(data_arr) - 1])

        for data in data_arr:
            insert_data.append([data])

        try:
            movie_feature_collection.insert(insert_data)
            it += 1
        except:
            continue

# movie_feature_collection.insert(movie_feature_data)

# user_feature_data = np.array(pd.read_csv('data/user_feature_calculated.csv').iloc[:, 1:])
# user_feature_collection.insert(user_feature_data)

################################################################################
# 4. create index
# We are going to create an IVF_FLAT index for hello_milvus collection.
# create_index() can only be applied to `FloatVector` and `BinaryVector` fields.
"""
    Example:
    print(fmt.format("Start Creating index IVF_FLAT"))
    index = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128},
    }

hello_milvus.create_index("embeddings", index)

"""

################################################################################
# 5. search, query, and hybrid search
# After data were inserted into Milvus and indexed, you can perform:
# - search based on vector similarity
# - query based on scalar filtering(boolean, int, etc.)
# - hybrid search based on vector similarity and scalar filtering.
#
"""
    Example:
    
    # Before conducting a search or a query, you need to load the data in `hello_milvus` into memory.
print(fmt.format("Start loading"))
hello_milvus.load()

# -----------------------------------------------------------------------------
# search based on vector similarity
print(fmt.format("Start searching based on vector similarity"))
vectors_to_search = entities[-1][-2:]
search_params = {
    "metric_type": "L2",
    "params": {"nprobe": 10},
}

start_time = time.time()
result = hello_milvus.search(vectors_to_search, "embeddings", search_params, limit=3, output_fields=["random"])
end_time = time.time()

for hits in result:
    for hit in hits:
        print(f"hit: {hit}, random field: {hit.entity.get('random')}")
print(search_latency_fmt.format(end_time - start_time))

# -----------------------------------------------------------------------------
# query based on scalar filtering(boolean, int, etc.)
print(fmt.format("Start querying with `random > 0.5`"))

start_time = time.time()
result = hello_milvus.query(expr="random > 0.5", output_fields=["random", "embeddings"])
end_time = time.time()

print(f"query result:\n-{result[0]}")
print(search_latency_fmt.format(end_time - start_time))

# -----------------------------------------------------------------------------
# hybrid search
print(fmt.format("Start hybrid searching with `random > 0.5`"))

start_time = time.time()
result = hello_milvus.search(vectors_to_search, "embeddings", search_params, limit=3, expr="random > 0.5", output_fields=["random"])
end_time = time.time()

for hits in result:
    for hit in hits:
        print(f"hit: {hit}, random field: {hit.entity.get('random')}")
print(search_latency_fmt.format(end_time - start_time))

"""
###############################################################################
# 6. delete entities by PK
# You can delete entities by their PK values using boolean expressions.
"""
Example:

ids = insert_result.primary_keys

expr = f'pk in ["{ids[0]}" , "{ids[1]}"]'
print(fmt.format(f"Start deleting with expr `{expr}`"))

result = hello_milvus.query(expr=expr, output_fields=["random", "embeddings"])
print(f"query before delete by expr=`{expr}` -> result: \n-{result[0]}\n-{result[1]}\n")

hello_milvus.delete(expr)

result = hello_milvus.query(expr=expr, output_fields=["random", "embeddings"])
print(f"query after delete by expr=`{expr}` -> result: {result}\n")
"""

###############################################################################
# 7. drop collection
# Finally, drop the hello_milvus collection
"""
Example:

print(fmt.format("Drop collection `hello_milvus`"))
utility.drop_collection("hello_milvus")

"""
