from email import message
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, validator
from app.utilities.decorators import auth_required
from app.utilities.helper import hash_password


from app.utilities.dependencies import get_session

from app.models.database_models import Movies, Genre, Roles, Users

router = APIRouter()

security = HTTPBearer()



class AuthModel(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "ashutoshuniyal21@gmail.com",
                "password": "9410197255",
            }
        }




class UserModel(BaseModel):

    name:str
    email: str
    password:str
    role:str # in [admin, user]

    @validator('role')
    def c_match(cls, v):
        if not v.lower().strip() in ['admin', 'user']:
            raise ValueError('role must be in [admin, user]')
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "Ashutosh",
                "email": "ashutoshuniyal21@gmail.com",
                "password": "9410197255",
                "role": "possible values for role [admin ,user]",
            }
        }


@router.get("/search_by_name/{name}",
             tags=["Common Routes"],
             description="**return movie from database by given name and no authentication Required for this route**")
def search_by_name(name: str, session: dict = Depends(get_session)):
    movie = Movies.get_movie_by_name(session, name)

    if movie == None:
        message = "not found"
    else:
        message = "successfully found"

    return movie


@router.get("/search_movies_by_genre/{genre}",
             tags=["Common Routes"],
              description="**return movies from database by given genre and no authentication Required for this route**")
def search_movies_by_genre(genre: str, session: dict = Depends(get_session)):
    movies = Movies.get_movies_by_genre_name(session, genre)
    if movies == None:
        return {"movies": [], "message": "sucessfully"}
    return {"movies": movies, "message": "sucessfully"}


@router.get("/genres",
        tags=["Common Routes"],
        description="**returns all genres listed in database and no authentication Required for this route**")
def get_all_genres(session: dict = Depends(get_session)):
    genres = Genre.get_multiple_genre(session)
    res = [genre.name for genre in genres]
    return {"genres": res, "message": "sucessfully"}


@router.get("/movies", 
            tags=["Common Routes"],
            description="**returns all movies listed in database and no authentication Required for this route**")
def get_all_movies(session: dict = Depends(get_session)):
    movies = Movies.get_all_movies(session)
    return movies




@router.post('/login', 
            tags=["Common Routes"],
            description="**Route Loggin In**")
def login(auth:AuthModel, session: dict = Depends(get_session)):
   
    token = Users.get_user_email_password(session, auth.email, auth.password)
    if token == None:
        return {"message": "password or email error"}

    return {"token":token, "message":"succesfully loged in"}


@router.post('/signup',
        tags=["Common Routes"],
        description="**Route for creating account**")
def create_account(user_info:UserModel, session: dict = Depends(get_session)):
    print("***************start************")
    user_info = dict(user_info)
    token = Users.create_user(session, user_info)
    print(f"***************{token}*****************")
    if token == None:
        return {"message":"email already resister"}
    session.commit()
    return {"token":token, "message":"user successfully created"}
