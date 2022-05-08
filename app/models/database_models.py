import os
from typing import Dict, List, Optional
from sqlmodel import Field, SQLModel, select
from sqlalchemy import UniqueConstraint, String
from sqlalchemy import Column
from app.utilities.helper import hash_password, verify_password, create_jwt_token


class Genre(SQLModel, table=True):
    __tablename__ = "genre"
    id: int = Field(primary_key=True)
    name: str = Field(sa_column=Column("name", String(40), unique=True))

    @classmethod
    def add_genre(cls, session, genre_name):

        ''' add genre to genre table if genre not exist in data base'''

        genre_name = genre_name.lower().strip()

        try:
            genre = Genre(name=genre_name)
            session.add(genre)
            session.flush()
            return genre
        except Exception as e:
            return None

    @classmethod
    def get_genre_by_name(cls, session, genre_name):

        '''  return genre obj of given name  '''

        genre_name = genre_name.lower().strip()
        query = select(Genre).where(Genre.name == genre_name)
        result = session.exec(query).first()
        return result

    @classmethod
    def get_genre_by_id(cls, session, genre_id):

        '''return genre obj of given id'''

        query = select(Genre.name).where(Genre.id == genre_id)
        result = session.exec(query).first()
        return result

    @classmethod
    def add_multiple_genre(cls, session, genre_name_set):

        '''for addming list of genre if not exist in genre table'''

        genre_query_list = []
        query = select(Genre.name)
        result = set(session.exec(query).all())

        for ele in genre_name_set:
            genre_name = ele.lower().strip()
            query = select(Genre).where(Genre.name == genre_name)
            genre = session.exec(query).first()

            if genre_name not in result:
                genre = Genre(name=genre_name)
                session.add(genre)
                session.flush()
                genre_query_list.append(genre)
            else:
                genre_query_list.append(genre)

        return genre_query_list

    @classmethod
    def get_multiple_genre(cls, session):
        '''     return list of genre object    '''
        query = select(Genre)
        result = session.exec(query).all()

        return result


class Roles(SQLModel, table=True):
    __tablename__ = "roles"
    id: int = Field(primary_key=True)
    role: str

    @classmethod
    def create_new_role(cls, session, role):

        '''for creating new role if not present in database and return created role obj'''

        role = role.lower().strip()
        query = select(Roles).where(Roles.role == role)
        role1 = session.exec(query).first()

        if role1 == None:
            roles1 = Roles(role=role)
            session.add(roles1)
            session.flush()
            return roles1   
        else:
            return None

    @classmethod
    def get_role_by_id(cls, session, role_id):

        '''return role obj from database by given role id'''

        query = select(Roles).where(Roles.id == role_id)
        role1 = session.exec(query).first()
        return role1
        


class Users(SQLModel, table=True):

    __tablename__ = "users"

    id: int = Field(primary_key=True)
    name: str
    email: str = Field(sa_column=Column("email", String(40), unique=True))
    hashed_password: str
    is_varified: bool = Field(default=False)
    role_id: int = Field(default=None, foreign_key="roles.id")



    @classmethod
    def create_user(cls, session, user_data):

        '''create user in data base and return  HTTPBearer token for authrization'''

        try:
            hashed_password = hash_password(user_data["password"])
            role = user_data["role"].lower().strip()

            query = select(Roles.id).where(Roles.role == role)
            role_id = session.exec(query).first()
            user = Users(name=user_data["name"].lower().strip(),
                    email=user_data["email"].lower().strip(),
                    hashed_password=hashed_password,
                    role_id=role_id,)
            session.add(user)
            session.flush()

            role_obj = Roles.get_role_by_id(session, role_id)
            data = {"email": user_data["email"].lower().strip(), "role": role_obj.role, "is_varified": user.is_varified}
            time = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
            token = create_jwt_token(data, time)
            return {"token":token}

        except Exception as e:
            return None



    @classmethod
    def get_user_email_password(cls, session, email, password):

        '''return  HTTPBearer token for autherization of given user if email and passwords are correct'''

        try:
            email = email.lower().strip()
            query = select(Users).where(Users.email == email)
            user = session.exec(query).first()
            print(user, " //////////////////")
            role_id = user.role_id
            role_obj = Roles.get_role_by_id(session, role_id)
            if verify_password(password, user.hashed_password):
                data = {"email": email, "role": role_obj.role, "is_varified": user.is_varified}
                time = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
                token = create_jwt_token(data, time)
                return token
            else:
                return None
        except Exception as e:
            return None

    @classmethod
    def get_user_email(cls, session, email):

        '''return user obj of given email'''

        email = email.lower().strip()
        query = select(Users).where(Users.email == email)
        user =  session.exec(query).first()
        session.flush()
        return user

        






class MovieGenre(SQLModel, table=True):

    __tablename__ = "moviegenre"
    id: int = Field(primary_key=True)
    movies_id: int = Field(default=None, foreign_key="movies.id")
    genre_id: int = Field(default=None, foreign_key="genre.id")

    @classmethod
    def get_genres_by_movie_id(cls, session, movie_id):

        '''return moviegenre obj for given movie id'''

        query = select(MovieGenre).where(MovieGenre.movies_id == movie_id)
        result = session.exec(query).all()
        return result


class Favourites(SQLModel, table=True):

    __tablename__ = "favourites"
    id: int = Field(primary_key=True)
    movies_id: int = Field(default=None, foreign_key="movies.id")
    user_id: int = Field(default=None, foreign_key="users.id")

    @classmethod 
    def add_to_favourites(cls, session, user_id, movie_id):

        '''create favourites entries in the data base by given user id and movie id 
        return favourites obj '''

        query = select(Favourites).where(Favourites.movies_id == movie_id,Favourites.user_id == user_id )
        fav  = session.exec(query).first()
        try:
            if fav != None:
                return {"message": "already exists in Favourites"}
            favourite = Favourites(movies_id =movie_id, user_id = user_id)
            session.add(favourite)
            session.flush()
            return favourite
        except Exception as e:
            return None

    @classmethod 
    def get_favourites_user_id(cls, session, user_id):

        '''return list of favourites by given user_id'''

        query = select(Favourites).where(Favourites.user_id == user_id)
        user_fav  = session.exec(query).all()
        return user_fav

    @classmethod 
    def delete_movie_from_favourites(cls, session, user_id, movie_id):
        
        '''delete  movie from favourites for given user by given movie id and user_id'''

        query = select(Favourites).where(Favourites.movies_id == movie_id,Favourites.user_id == user_id )
        fav  = session.exec(query).first()

        try:
            if fav == None:
                return {"message": "movie not in  Favourites"}
            Deleted_fav = dict(fav)
            session.delete(fav)
            session.flush()
            return Deleted_fav

        except Exception as e:
            return e




class Movies(SQLModel, table=True):

    __tablename__ = "movies"

    id: int = Field(primary_key=True)
    name: str = Field(sa_column=Column("name", String(40), unique=True, index=True))
    imdb_score: float
    popularity: float
    director: str

    @classmethod
    def add_movie(cls, session, movie_info: Dict):

        '''add movie to movie table and return movie obj'''

        try:
            genre_list = movie_info["genre"]
            genre_obj_list = Genre.add_multiple_genre(session, genre_list)
            movie = Movies(
                name=movie_info["name"].lower().strip(),
                imdb_score=movie_info["imdb_score"],
                popularity=movie_info["popularity"],
                director=movie_info["director"].lower().strip(),
            )

            session.add(movie)
            session.flush()

            movie.add_genres(session, genre_obj_list)

            return movie
        except Exception as e:
            return None

    def get_genres(self, session):

        '''return genre of movie by given movie id'''

        return MovieGenre.get_genres_by_movie_id(session, self.id)

    @classmethod
    def get_movie_by_name(cls, session, movie_name):

        '''return list of movies matching given movie name'''

        try:
            movie_name = movie_name.lower().strip()
            query = select(Movies).where(Movies.name.like(movie_name + "%"))
            result = session.exec(query).all()

            movie_info = []

            for movie in result:
                genres = MovieGenre.get_genres_by_movie_id(session, movie.id)
                genre_list = []
                for genre in genres:
                    print(genre.id)
                    genre_name = Genre.get_genre_by_id(session, genre.genre_id)
                    genre_list.append(genre_name)
                movie_dct = dict(movie)
                movie_dct["genre"] = genre_list
                movie_info.append(movie_dct)

            return movie_info
        except Exception as e:
            return None

    @classmethod
    def get_movie_by_id(cls, session, movie_id):

        '''return movie obj by given movie id'''

        query = select(Movies).where(Movies.id == movie_id)
        result = session.exec(query).first()
        return result

    def add_genres(self, session, genre_list: List[Genre]):

        '''add genres to MovieGenre table associated with given movie'''

        movie_genres = [
            MovieGenre(movies_id=self.id, genre_id=genre.id) for genre in genre_list
        ]
        session.add_all(movie_genres)
        session.flush()

        return movie_genres

    @classmethod
    def get_movies_by_genre_name(cls, session, genre_name):

        '''return list of movies having genre equal to given genre name'''

        try:
            genre_name = genre_name.lower().strip()
            genre_obj = Genre.get_genre_by_name(session, genre_name)
            # return genre_obj
            query = select(MovieGenre).where(MovieGenre.genre_id == genre_obj.id)
            result = session.exec(query).all()
            res = []

            for obj in result:
                movie = Movies.get_movie_by_id(session, obj.movies_id)
                res.append(movie)

            return res
        except Exception as e:
            return None

    @classmethod
    def get_all_movies(cls, session):

        ''' return list of all movies present in the data base '''

        try:
            query = select(Movies)
            result = session.exec(query).all()
            movies = []
            for movie in result:
                movies.append(Movies.get_movie_by_name(session, movie.name))

            return movies

        except Exception as e:
            return None
