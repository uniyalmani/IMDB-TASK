from venv import create
import pytest
from sqlmodel import select
from sys import flags
from sqlalchemy import insert
from app.models.database_models import Genre, Movies, Roles, Users, Favourites

from app.utilities.helper import decode_token


@pytest.fixture
def movie_payload():
    movie_info = [
            {
            "popularity": 83.0,
            "director": "Victor Fleming",
            "genre": [
            "Adventure",
            "Family",
            "Fantasy",
            "Musical"
            ],
            "imdb_score": 8.3,
            "name": "The Wizard of Oz"
        },
        {
            "popularity": 88.0,
            "director": "George Lucas",
            "genre": [
            "Action",
            "Adventure",
            "Fantasy",
            "Sci-Fi"
            ],
            "imdb_score": 8.8,
            "name": "Star Wars"
        },
        {
            "popularity": 66.0,
            "director": "Giovanni Pastrone",
            "genre": [
            "Adventure",
            "Drama",
            "War"
            ],
            "imdb_score": 6.6,
            "name": "Cabiria"
        }]
    return movie_info


@pytest.fixture
def users_payload():
    users = [{
        "name":"Ashutosh",
        "email": "ashutoshuniyal21@gmail.com",
        "password":"9410197255",
        "role":"admin"
    }, {
        "name":"nitin",
        "email": "nitinuniyal21@gmail.com",
        "password":"9410197255",
        "role":"user"
    }]
    return users

def test_genre_single_insertion(database_session):

    genre_name = "family"

    genre = Genre.add_genre(database_session, genre_name)

    result = Genre.get_genre_by_name(database_session, genre_name)

    assert result.name == genre.name


def test_genre_multiple_insertion(database_session):

    genre_set_name = {"family", "action", "horror"}

    genre_query_lst1 = Genre.add_multiple_genre(database_session, genre_set_name)
    database_session.commit()

    genre_query_lst2 = Genre.get_multiple_genre(database_session)

    flag1 = True
    flag2 = True

    for ele in genre_query_lst1:
        if ele.name not in genre_set_name:
            flag1 = False
            break

    for ele in genre_query_lst2:
        if ele.name not in genre_set_name:
            flag2 = False
            break

    assert flag2 and flag1


def test_add_movies_insertion(database_session, movie_payload):

    movie_info = movie_payload[0]


    movie = Movies.add_movie(database_session, movie_info)
    database_session.commit()

    res_movie = Movies.get_movie_by_name(database_session, movie_info["name"])

    res_movie_by_id = Movies.get_movie_by_id(database_session, movie.id)

    movie1_by_genre = Movies.get_movies_by_genre_name(
        database_session, movie_info["genre"][0]
    )
    movie2_by_genre = Movies.get_movies_by_genre_name(
        database_session, movie_info["genre"][1]
    )
    movie3_by_genre = Movies.get_movies_by_genre_name(
        database_session, movie_info["genre"][2]
    )

    movie = select(Movies).where(Movies.name == movie_info["name"])
    movie = database_session.exec(movie).first()

    genres = movie.get_genres(database_session)


    assert movie1_by_genre == movie2_by_genre == movie3_by_genre


def test_user_creation(database_session, users_payload):

    for user in users_payload:

        role = user["role"]
        roles1 = Roles.create_new_role(database_session, role)

        if roles1 != None:
            created_role = dict(roles1)

        created_user = dict(Users.create_user(database_session, user))
        created_user_token_data = decode_token(created_user["token"])

        returned_user = Users.get_user_email_password(database_session, user["email"], user["password"])

        returned_user_token_data = decode_token(returned_user)

        database_session.commit()

        assert created_user_token_data["email"] == returned_user_token_data["email"]


def test_Favourites_insertion(database_session, users_payload, movie_payload):

    movie_list_added = []

    for movie_info in movie_payload:
        movie = Movies.add_movie(database_session, movie_info)
        movie_list_added.append(movie)


    for user in users_payload:

        role = user["role"]
        roles1 = Roles.create_new_role(database_session, role)

        if roles1 != None:
            created_role = dict(roles1)

        created_user = dict(Users.create_user(database_session, user))
        created_user_token_data = decode_token(created_user["token"])

        returned_user = Users.get_user_email_password(database_session, user["email"], user["password"])

        returned_user_token_data = decode_token(returned_user)

        user_email = returned_user_token_data["email"]

        user = Users.get_user_email(database_session, user_email)

        
        first_fav = Favourites.add_to_favourites(database_session, user.id, movie_list_added[0].id)
        sec_fav = Favourites.add_to_favourites(database_session, user.id, movie_list_added[1].id)
        third_fav = Favourites.add_to_favourites(database_session, user.id, movie_list_added[2].id)

        removed_fav = Favourites.delete_movie_from_favourites(database_session, user.id, movie_list_added[2].id)
        database_session.commit()

        list_fav_obj = Favourites.get_favourites_user_id(database_session, user.id)
    
        print(list_fav_obj, "*********",removed_fav)
        for ele in list_fav_obj:
            assert ele.movies_id in {movie_list_added[0].id,movie_list_added[1].id}
            assert removed_fav["movies_id"] != ele.movies_id 
    

        database_session.commit()








