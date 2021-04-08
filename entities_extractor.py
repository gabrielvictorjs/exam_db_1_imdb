import json

json_string = open('imdb_top_1000.json', mode='r', encoding='utf-8').read()
json_data = [{'id': index + 1, **item}
             for index, item in enumerate(json.loads(json_string))]


def extract_movies(json_data: list) -> list[dict]:
    keys = ['id', 'title', 'released_year', 'runtime', 'overview', 'rating']
    return list(map(lambda item: {key: item[key] for key in keys}, json_data))


def extract_directors(json_data: list) -> list[dict]:
    directors = set(map(lambda item: item['director'], json_data))
    return [{'id': index + 1, 'name': item} for index, item in enumerate(directors)]


def extract_genres(json_data: list) -> list[dict]:
    genres_splitted = [str(item['genre']).split(', ') for item in json_data]
    genres = set([item for sublist in genres_splitted for item in sublist])
    return [{'id': index + 1, 'title': item} for index, item in enumerate(genres)]


def extract_actors(json_data: list) -> list[dict]:
    actors_from_movies = [[item['Star1'], item['Star2'],
                           item['Star3'], item['Star4']] for item in json_data]
    actors = set([item for sublist in actors_from_movies for item in sublist])
    return [{'id': index + 1, 'name': item} for index, item in enumerate(actors)]


def extract_movies_actors(json_data: list[dict]) -> list:
    actors = extract_actors(json_data)
    movies_actors = []
    for actor in actors:
        for movie in json_data:
            if actor['name'] in movie.values():
                movies_actors.append({
                    'movie_id': movie['id'],
                    'actor_id': actor['id']
                })

    return movies_actors


def extract_movies_directors(json_data: list[dict]) -> list:
    directors = extract_directors(json_data)
    movies_directors = []
    for director in directors:
        for movie in json_data:
            if director['name'] == movie['director']:
                movies_directors.append({
                    'movie_id': movie['id'],
                    'director_id': director['id']
                })

    return movies_directors


def extract_movies_genres(json_data: list[dict]) -> list:
    genres = extract_genres(json_data)
    movies_genres = []
    for genre in genres:
        for movie in json_data:
            if genre['title'] in movie['genre']:
                movies_genres.append({
                    'movie_id': movie['id'],
                    'genre_id': genre['id']
                })

    return movies_genres


datasets = {
    'movies': extract_movies(json_data),
    'directors': extract_directors(json_data),
    'genres': extract_genres(json_data),
    'actors': extract_actors(json_data),
    'movies_actors': extract_movies_actors(json_data),
    'movies_directors': extract_movies_directors(json_data),
    'movies_genres': extract_movies_genres(json_data)
}

for key in datasets:
    with open('extracted/' + key + '.json', 'w+', encoding='utf-8') as opened_file:
        json.dump(datasets[key], opened_file, indent=2,
                  sort_keys=True, ensure_ascii=False)
