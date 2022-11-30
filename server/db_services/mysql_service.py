import mysql.connector


def get_connection(host_name, username, password, database_name=None):
    db = mysql.connector.connect(
        host=host_name,
        user=username,
        passwd=password,
        database=database_name
    )

    return db


def get_user_data_by_field(cursor, field_1, field_2, field_2_data):
    query = """SELECT {0} FROM user_feature WHERE {1} = '{2}' """.format(field_1, field_2, field_2_data)
    cursor.execute(query)

    return cursor.fetchall()[0]


def get_all_users(cursor):
    cursor.execute("SELECT * FROM user_feature")
    all_users_data = cursor.fetchall()

    return all_users_data


def get_user_data_by_id(cursor, user_id):
    cursor.execute("SELECT * FROM user_feature WHERE userId = {0}".format(user_id))

    return cursor.fetchall()[0]


def get_movie_data_by_field(cursor, field_1, field_2, field_2_data):
    query = """SELECT {0} FROM movie_feature WHERE {1} = '{2}' """.format(field_1, field_2, field_2_data)
    cursor.execute(query)

    return cursor.fetchall()[0]


def get_movie_data_by_name(cursor, movie_name):
    cursor.execute("SELECT * FROM movie_feature WHERE original_title = '{0}'".format(movie_name))
    return cursor.fetchall()[0]


def get_all_movies(cursor):
    cursor.execute("SELECT * FROM movie_feature")
    all_movie_data = cursor.fetchall()

    return all_movie_data


def close_db_connection(db, cursor):
    db.close()
    cursor.close()
