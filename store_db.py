import mysql.connector
import csv
import ast


def store_ratings(db, cursor):
    cursor.execute("""
        DROP TABLE IF EXISTS rating
    """)

    cursor.execute(
        """
        CREATE TABLE rating(
            userId INT NOT NULL,
            movieId INT NOT NULL,
            rating INT NOT NULL,
            timestamp BIGINT,
            CONSTRAINT ratingPK PRIMARY KEY (userId, movieId),
            CONSTRAINT moveIdFK FOREIGN KEY (movieId) REFERENCES movie(id)
        )
        """
    )

    csv_file_path = "data/ratings.csv"

    with open(csv_file_path, encoding='utf8', newline='') as csvfile:
        ratings = csv.reader(csvfile)
        next(ratings, None)  # skips the header

        for userId, movieId, rating, timestamp in ratings:
            query = '''INSERT INTO rating VALUES ({0}, {1}, {2}, {3});'''.format(userId, movieId, rating, timestamp)

            try:
                cursor.execute(query)
                print(query)
                db.commit()
            except:
                continue


def store_movies(db, cursor):
    cursor.execute("""
        DROP TABLE IF EXISTS movie
    """)

    cursor.execute(
        """
        CREATE TABLE movie (
            genres VARCHAR(255),
            id INT PRIMARY KEY,
            imdb_id VARCHAR(50),
            language VARCHAR(5),
            title VARCHAR(255) NOT NULL,
            popularity REAL,
            release_date VARCHAR(12),
            runtime INT,
            tagline VARCHAR(255)
        )
        """
    )

    csv_file_path = "data/movies_metadata.csv"

    with open(csv_file_path, encoding='utf8', newline='') as csvfile:

        movies = csv.reader(csvfile)
        next(movies, None)

        for movie in movies:

            if len(list(movie)) < 9:
                continue

            print(list(movie))

            genres_list = ast.literal_eval(movie[0])
            genres_name_list = [genre['name'] for genre in genres_list]
            genres_names_csv = ','.join(genres_name_list)

            runtime = movie[7]

            if runtime == '':
                runtime = 0

            tagline = movie[8].replace('''"''', "'")

            query = '''INSERT INTO movie VALUES ("{0}", {1}, "{2}", "{3}", "{4}", {5}, "{6}", {7}, "{8}");''' \
                .format(genres_names_csv, movie[1], movie[2], movie[3],
                        movie[4], movie[5], movie[6],
                        runtime, tagline)

            try:
                cursor.execute(query)
                print(query)
                db.commit()
            except:
                continue


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
my_cursor.execute("CREATE DATABASE IF NOT EXISTS movie_database")
close_db_connection(db, my_cursor)

db = get_db_connection("localhost", "root", "kktt12345", "movie_database")

my_cursor = db.cursor()

store_movies(db, my_cursor)
store_ratings(db, my_cursor)
close_db_connection(db, my_cursor)
