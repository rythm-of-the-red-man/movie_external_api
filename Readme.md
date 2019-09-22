# Movie API - Recruitment task 

## Getting Started


### Prerequisites

In order to run project locally, you need to have docker, and docker-compose installed.
You can see detailed instructions how to install it here: [Docker](https://docs.docker.com/install/) and here: [Docker Compose](https://docs.docker.com/compose/install/)

### Running project locally

To run the project locally navigate to a project directory, and build docker image: 

```
docker-compose build
```

and after that, start the project by running:

```
docker-compose up
```

The project should be available on 127.0.0.1:8000
## Running the tests

To run automated tests you should have container up and running. First section explains how to achieve it.
After that you can run the tests by executing:
```
docker exec movies_api python3 manage.py test
```

## 3rd party libraries

To develop this app I have used requests, whitenoise and django-rest-framework. I have used requests to build movie-service which handle external API requests. Whitenoise serves static files from django-rest-framework. Django-rest-framework was used to actually build API, including serializers and views. For SQLite/PostgreSQL handling python-dotenv and dj-database-url are in use.

## Database
App uses sql-lite local database, when ran locally. When deployed to heroku, it doesnt get .env file, so heroku mount postgres, as default database.

## Routes

### POST /movies
Takes title of a movie as argument (in JSON file), and saves it to database.
#### Example request body
```
 {'title':'The Shining'}
```
### GET /movies
Returns all movies in database.
### POST /comments
Takes movie id and comment as arguments and add comment to database.
#### Example request body
```
 {'movie':1,'comment':'Cool!'}
```
### GET /comments
Returns all coments from database.
### GET /top
Returns ranking of movies from specified period of time.
#### Example request body
```
/top/?date_start=2011-10-21&date_end=2020-10-21
```