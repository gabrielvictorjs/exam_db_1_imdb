-- Selecionar todos os gêneros que um diretor trabalhou
select genre.title as "Genre",
       count(genre.title) as "Count",
       director.name as "Director"
from movies_directors movie_director
inner join movies movie on movie_director.movie_id = movie.id
inner join movies_genres movie_genre on movie.id = movie_genre.movie_id
inner join genres genre on movie_genre.genre_id = genre.id
inner join directors director on movie_director.director_id = director.id
where director.name like 'Christopher Nolan'
group by genre.title
order by count(genre.title) desc;


-- Selecionar todos os atores que trabalharam em um filme de guerra entre 2000 e 2005
select genre.title as "Genre",
       actor.name as "Actor",
       movie.released_year as "Year"
from movies_genres movie_genre
inner join movies movie on movie_genre.movie_id = movie.id
inner join genres genre on movie_genre.genre_id = genre.id
inner join movies_actors movie_actor on movie_actor.movie_id = movie.id
inner join actors actor on movie_actor.actor_id = actor.id
where genre.title like 'War' and movie.released_year >= 2000 and movie.released_year <= 2005
order by movie.released_year;


-- Top 10 atores que mais aparecem no top 1000 e seus melhores filmes
select actor.name as "Actor",
       count(min_rating_movie.title) as "Participations",
       min_rating_movie.title as "Best Movie",
       min_rating_movie.rating as "Rating"
from actors actor
inner join movies_actors movie_actor on actor.id = movie_actor.actor_id
inner join (
    select id, title, rating
    from movies
    group by id
    order by rating desc
    ) min_rating_movie on movie_actor.movie_id = min_rating_movie.id
group by actor.id
order by Participations desc
limit 10;


-- Selecionar atores que trabalharam com um diretor para cada gênero
select group_concat(actor.name separator ', ') as "Actors",
       genre.title as "Genre",
       director.name as "Director"
from directors director
inner join movies_directors movie_director on director.id = movie_director.director_id
inner join movies movie on movie_director.movie_id = movie.id
inner join movies_genres movie_genre on movie.id = movie_genre.movie_id
inner join genres genre on movie_genre.genre_id = genre.id
inner join movies_actors movie_actor on movie.id = movie_actor.movie_id
inner join actors actor on movie_actor.actor_id = actor.id
where director.name like 'Ang Lee'
group by genre.title
order by genre.title;


-- Top 10 diretores com mais filmes no top 1000 e seu melhor filme
select count(movie.title) as "Movies Count",
       movie.title as "Best Movie",
       movie.rating as "Rating",
       director.name as "Director"
from directors director
inner join movies_directors movie_director on movie_director.director_id = director.id
inner join movies movie on movie_director.movie_id = movie.id
group by director.name
order by count(movie.title) desc
limit 10;