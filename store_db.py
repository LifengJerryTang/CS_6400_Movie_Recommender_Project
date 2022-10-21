import mysql.connector
import csv

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="kktt12345",
    database="movie_database"
)

my_cursor = db.cursor()


def store_ratings():
    my_cursor.execute(
        """
        CREATE TABLE rating(
            userId INT NOT NULL,
            movieId INT NOT NULL,
            rating INT NOT NULL,
            timestamp BIGINT,
            CONSTRAINT ratingPK PRIMARY KEY (userId, movieId) 
        )
        """
    )

    csv_file_path = "data/ratings.csv"

    with open(csv_file_path, encoding='utf8', newline='') as csvfile:
        movie_cast = csv.reader(csvfile)
        for row in movie_cast:
            name = row[2]
            date = row[3]
            if name:
                name = name.replace('''"''', "'")
                name = '''"''' + name + '''"'''
            else:
                name = "NULL"

            if date:
                date = date.replace('''"''', "'")
                date = '''"''' + date + '''"'''
            else:
                date = "NULL"
            query = '''INSERT INTO movie_cast VALUES ({0}, {1}, {2},{3},{4});'''.format(
                row[0], row[1], name, date, row[4])
            my_cursor.execute(query)



