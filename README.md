# IMDB-TASK

hosted swagger ui link for testing -> https://protected-gorge-43739.herokuapp.com/documentation

verified admin email (or super user) -> ashutoshumiyal21@gmail.com
verified admin password (or super user) --> 9410197255


#common routes (Common Routes Can be used without any token HTTPBearer (http, Bearer)):

method: get --> /search_by_name/{name} ---> return movie from database by given name and no authentication Required for this route.
    
method:  get --> /search_movies_by_genre/{genre} ---> return movies from database by given genre and no authentication Required for this route.
    
method:  get --> /genres --> returns all genres listed in database and no authentication Required for this route.
    
method: get --> /movies --> returns all movies listed in database and no authentication Required for this route.
    
method: post -->/login --> return HTTPBearer token for protected route.
                    example for login requestbody (all fields are required)--->{
                                                     "email": "nitinuniyal21@gmail.com",
                                                      "password": "9410197255"
                                                      }
                                                      
method :post -->/signup --> for creating account and return  HTTPBearer token for protected route.
                   example for signup requestbody (all fields are required)--->{
                                                    "name": "shubnam",
                                                   "email": "shubham21@gmail.com",
                                                    "password": "9410197255",
                                                    "role": "user"
                                                      }
                   
    

#Protected Routes (needs authorizations by setting HTTPBearer (http, Bearer)):

method: post --> /add_movie ----> Route for adding movie to database. ONLY SUPER USER (or verified admin) ARE AUTHORIZE FOR THIS ROUTE. authentication (HTTPBearer (http, Bearer) for authorizations) Required for this route.
example for add_movie requestbody(all fields are required)  ----->{
                                                           "popularity": 64,
                                                           "director": "J. Searle Dawley",
                                                             "genre": [
                                                                         "Fantasy",
                                                                          "Romance"
                                                                       ],
                                                          "imdb_score": 6.4,
                                                          "name": "this is the end"
                                                            }
                                    
    
method: post --> /toggle_favourites/{movie_id} ---> Route for toggling movie ( (if movie already in favourites -->then remove movie from favourite) and (if movie not in favourites -->then add movie to favourite) ). authentication (HTTPBearer (http, Bearer) for authorizations) Required for this route.
     
method: get --> /favourites_list ---> Route returning list of favourites. authentication (HTTPBearer (http, Bearer) for authorizations) Required for this route.
    
    
    
    
#for pytest commands:
1) **docker exec -it mysql_db bash** #this command will open terminal of container ;
2) **mysql -u root -pfynd123;** #this command opens mysql in terminal
3) **GRANT ALL PRIVILEGES ON *.* TO 'fynd_acad'@'%'**; # this commands give all the permissions to user fynd_acad for droping and creating another              dummy database for testing;
 4) **sh tests.sh** # run ths command in local terminal for ri=unning pytest
    
    
    
    
    
 
    
    
    
    
    
    
