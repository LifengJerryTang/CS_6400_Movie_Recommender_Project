import time
import csv
import ast
import mysql.connector
import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)


def get_db_connection(host_name, username, password, database_name=None):
    return mysql.connector.connect(
        host=host_name,
        user=username,
        passwd=password,
        database=database_name,
    )


def close_db_connection(db, cursor):
    db.close()
    cursor.close()


db = get_db_connection("localhost", "root", "kktt12345", "recommendation_features")

my_cursor = db.cursor()

# store_movie_features(db, my_cursor)
# store_user_features(db, my_cursor)


my_cursor.execute("SELECT * FROM user_feature WHERE userId = 1")
print(my_cursor.fetchall())

close_db_connection(db, my_cursor)

