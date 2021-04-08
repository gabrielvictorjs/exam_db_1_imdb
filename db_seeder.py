import mysql.connector
import os
import json
from dotenv import load_dotenv
from mysql.connector import errorcode

load_dotenv()


def open_json_file(name: str) -> list:
    file = open('extracted/' + name + '.json',
                mode='r', encoding='utf-8').read()
    return json.loads(file)


def movies_seeder(cursor):
    movies = open_json_file('movies')
    sql = '''INSERT INTO movies (id, title, overview, rating, released_year, runtime) 
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            overview = VALUES(overview),
            rating = VALUES(rating),
            released_year = VALUES(released_year),
            runtime = VALUES(runtime)'''

    values = [(movie['id'], movie['title'], movie['overview'],
              movie['rating'], movie['released_year'], movie['runtime'])
              for movie in movies]

    cursor.executemany(sql, values)


def directors_seeder(cursor):
    directors = open_json_file('directors')
    sql = '''INSERT INTO directors (id, name) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
            name = VALUES(name)'''

    values = [(director['id'], director['name'])
              for director in directors]

    cursor.executemany(sql, values)


def actors_seeder(cursor):
    actors = open_json_file('actors')
    sql = '''INSERT INTO actors (id, name) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
            name = VALUES(name)'''

    values = [(actor['id'], actor['name'])
              for actor in actors]

    cursor.executemany(sql, values)


def genres_seeder(cursor):
    genres = open_json_file('genres')
    sql = '''INSERT INTO genres (id, title) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
            title = VALUES(title)'''

    values = [(genre['id'], genre['title'])
              for genre in genres]

    cursor.executemany(sql, values)


def movies_directors_seeder(cursor):
    movies_directors = open_json_file('movies_directors')
    sql = '''INSERT INTO movies_directors (id, movie_id, director_id) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            movie_id = VALUES(movie_id),
            director_id = VALUES(director_id)'''

    values = [(index + 1, field['movie_id'], field['director_id'])
              for index, field in enumerate(movies_directors)]

    cursor.executemany(sql, values)


def movies_actors_seeder(cursor):
    movies_actors = open_json_file('movies_actors')
    sql = '''INSERT INTO movies_actors (id, movie_id, actor_id) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            movie_id = VALUES(movie_id),
            actor_id = VALUES(actor_id)'''

    values = [(index + 1, field['movie_id'], field['actor_id'])
              for index, field in enumerate(movies_actors)]

    cursor.executemany(sql, values)


def movies_genres_seeder(cursor):
    movies_genres = open_json_file('movies_genres')
    sql = '''INSERT INTO movies_genres (id, movie_id, genre_id) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            movie_id = VALUES(movie_id),
            genre_id = VALUES(genre_id)'''

    values = [(index + 1, field['movie_id'], field['genre_id'])
              for index, field in enumerate(movies_genres)]

    cursor.executemany(sql, values)


try:
    db = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        port=os.getenv('PORT'),
        password=os.getenv('PASSWORD'),
        database="imdb"
    )

    cursor = db.cursor()

    movies_seeder(cursor)
    directors_seeder(cursor)
    actors_seeder(cursor)
    genres_seeder(cursor)
    movies_directors_seeder(cursor)
    movies_actors_seeder(cursor)
    movies_genres_seeder(cursor)

    db.commit()

    db.close()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    db.close()
