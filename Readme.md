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

and after that start the project by running:

```
docker-compose up
```

The project should be available on 127.0.0.1:8000
## Running the tests

To run automated tests you should have container up and running. First section explains how to achieve it.
After that you can run tests by executing:
```
docker exec movies_api python3 manage.py test
```

## 3rd party libraries

To develop this app I have used requests, whitenoise and django-rest-framework. I've used requests to build movie-service which handle external API requests. Whitenoise serves static files from django-rest-framework. Django-rest-framework was used to actually build API, including serializers and views.

## Database
Because it is just recruitment app I did not see a point to use anything more than SQL-Lite. However I'm fully aware that if it would be regular app, something more efficient, like PostgreSQL should be set up.