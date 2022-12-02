import mysql.connector
import csv


def store_user_features(db, cursor):
    cursor.execute("""
        DROP TABLE IF EXISTS user_feature
    """)

    cursor.execute(
        """
        CREATE TABLE user_feature(
            userId INT PRIMARY KEY,
            user_feature_20230101 TEXT,
            user_feature_20220101 TEXT,
            user_feature_20200101 TEXT,
            user_feature_20150101 TEXT,
            user_feature_20100101 TEXT
        )
        """
    )

    csv_file_path = "data/user_feature_calculated.csv"

    with open(csv_file_path, encoding='utf8', newline='') as csvfile:
        user_features = csv.reader(csvfile)
        next(user_features, None)  # skips the header

        i = 0

        for _, userId, user_feature_20230101, \
            user_feature_20220101, user_feature_20200101, \
            user_feature_20150101, user_feature_20100101 in user_features:

            if i > 20000:
                break

            query = '''INSERT INTO user_feature VALUES (%s, %s, %s, %s, %s, %s);'''

            cursor.execute(query, (userId, user_feature_20230101, user_feature_20220101, user_feature_20200101,
                                   user_feature_20150101, user_feature_20100101))
            db.commit()
            i += 1
            # try:
            #     cursor.execute(query, (userId, user_feature_20230101, user_feature_20220101, user_feature_20200101,
            #                            user_feature_20150101, user_feature_20100101))
            #     db.commit()
            #     i += 1
            # except:
            #     continue


def store_movie_features(db, cursor):
    cursor.execute("""
        DROP TABLE IF EXISTS movie_feature
    """)

    cursor.execute(
        """
        CREATE TABLE movie_feature (
            cast TEXT,
            crew TEXT,
            keywords TEXT,
            adult VARCHAR(5),
            belongs_to_collection TEXT,
            budget BIGINT,
            genres TEXT,
            homepage TEXT,
            id INT PRIMARY KEY,
            original_language VARCHAR(5),
            original_title VARCHAR(255),
            overview TEXT,
            popularity INT,
            poster_path TEXT,
            production_companies TEXT,
            production_countries TEXT,
            release_date VARCHAR(15),
            release_date_timestamp BIGINT,
            have_release_date VARCHAR(5),
            revenue BIGINT,
            runtime INT,
            spoken_languages TEXT,
            status VARCHAR(20),
            tagline TEXT,
            title VARCHAR(255),
            vote_average INT,
            vote_count INT,
            movie_feature TEXT
            
        )
        """
    )

    csv_file_path = "data/movie_feature_calculated.csv"

    with open(csv_file_path, encoding='utf8', newline='') as csvfile:

        movie_features = csv.reader(csvfile)
        next(movie_features, None)

        i = 0

        for movie_feature in movie_features:

            movie_feature = list(movie_feature)
            if len(movie_feature) < 29:
                continue

            if i > 20000:
                break

            long_data_exists = False

            for i in range(len(movie_feature)):
                if isinstance(movie_feature[i], str):
                    if len(movie_feature[i]) > 10000:
                        long_data_exists = True
                        break
                    movie_feature[i] = movie_feature[i].replace("'", " ")

            if long_data_exists:
                continue

            query = '''INSERT INTO movie_feature VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

            cursor.execute(query, (movie_feature[1], movie_feature[2], movie_feature[3], movie_feature[4],
                                   movie_feature[5], movie_feature[6], movie_feature[7], movie_feature[8],
                                   movie_feature[9], movie_feature[10], movie_feature[11], movie_feature[12],
                                   movie_feature[13], movie_feature[14], movie_feature[15], movie_feature[16],
                                   movie_feature[17], movie_feature[18], movie_feature[19], movie_feature[20],
                                   movie_feature[21], movie_feature[22], movie_feature[23], movie_feature[24],
                                   movie_feature[25], movie_feature[26], movie_feature[27], movie_feature[28]))
            db.commit()
            i += 1

            # try:
            #
            # except:
            #     continue


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


db = get_db_connection("localhost", "root", "kktt12345")
my_cursor = db.cursor()
my_cursor.execute("CREATE DATABASE IF NOT EXISTS recommendation_features")
close_db_connection(db, my_cursor)

db = get_db_connection("localhost", "root", "kktt12345", "recommendation_features")

my_cursor = db.cursor()

store_movie_features(db, my_cursor)
store_user_features(db, my_cursor)

close_db_connection(db, my_cursor)
