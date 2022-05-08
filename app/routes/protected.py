from app.utilities.helper import decode_token
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import List
from pydantic import BaseModel
from app.utilities.dependencies import get_session
from app.models.database_models import Favourites, MovieGenre, Movies, Users, Genre
from app.utilities.decorators import auth_required, auth_required_nonverified_user
from app.utilities.helper import decode_token

router = APIRouter()
security = HTTPBearer()


class MovieInfo(BaseModel):
    name: str
    imdb_score: float
    popularity: float
    director: str
    genre: List[str]


    class Config:
        schema_extra = {
            "example": {
                        "popularity": 64.0,
                        "director": "J. Searle Dawley",
                        "genre": [
                                    "Fantasy",
                                    "Romance"
                                ],
                        "imdb_score": 6.4,
                        "name": "Snow White"
  }
        }


@router.post("/add_movie", 
            tags=["Protected Routes"],
            description= "**Route for adding movie to database. ONLY SUPER USER (or verified admin) ARE AUTHORIZE FOR THIS ROUTE. /authentication (HTTPBearer  (http, Bearer) for authorizations) Required for this route.**")
@auth_required("admin")
def add_movie(request: Request, movie_info: MovieInfo,credentials: HTTPAuthorizationCredentials = Security(security), session: dict = Depends(get_session)):

    movie = Movies.add_movie(session, dict(movie_info))

    if movie == None:
        return {"message": " error movie already exist or pay load error"}
    
    res = dict(movie)
    session.commit()

    return {"movie": res, "message": "added"}




@router.post("/toggle_favourites/{movie_id}", 
            tags=["Protected Routes"],
            description= '''**Route for toggling movie ( (if movie already in favourites -->then remove movie from favourite) and (if movie not in favourites -->then add movie to favourite) ). authentication (HTTPBearer  (http, Bearer) for authorizations) Required for this route.**''')
@auth_required_nonverified_user({"user", "admin"})
def toggle_favourites(request: Request, movie_id:int,credentials: HTTPAuthorizationCredentials = Security(security), session: dict = Depends(get_session)):

    movie = Movies.get_movie_by_id(session, movie_id)

    if movie == None:
        return {"message":"invalid movie id"}

    data = request.session.get("decode_existing_token")
    email = data.get("email")
    user = Users.get_user_email(session, email)
    fav_list = Favourites.get_favourites_user_id(session, user.id)
    set_of_movie_id = {ele.movies_id for ele in fav_list}

    if movie_id in set_of_movie_id:
        deleted_movie = Favourites.delete_movie_from_favourites(session, user.id,movie_id)
        session.commit()
        return {"deleted movie":deleted_movie,"message":"movie sucessfully deleted from favourites"}
    else:
        movie_added_to_fav = dict(Favourites.add_to_favourites(session, user.id, movie_id))
        session.commit()
        return {"added movie":movie_added_to_fav,"message":"movie sucessfully added to favourites"}




@router.get("/favourites_list",
         tags=["Protected Routes"],
         description= '''**Route returning list of favourites. authentication (HTTPBearer  (http, Bearer) for authorizations) Required for this route.**''')
@auth_required_nonverified_user({"user", "admin"})
def favourites_list(request: Request,credentials:  HTTPAuthorizationCredentials = Security(security), session: dict = Depends(get_session)):
   
    data = request.session.get("decode_existing_token")
    email = data.get("email")
    user = Users.get_user_email(session, email)
    fav_list = Favourites.get_favourites_user_id(session, user.id)
    fav_movie_list = []

    for ele in fav_list:
        movie = Movies.get_movie_by_id(session, ele.movies_id)
        genre_list = MovieGenre.get_genres_by_movie_id(session, ele.movies_id)
        genre_list = [Genre.get_genre_by_id(session, genre.genre_id) for genre in genre_list]
        fav_movie_list.append({"movie":movie, "genre":genre_list})
    
    return fav_movie_list


