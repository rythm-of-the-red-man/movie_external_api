FROM python:3.8-rc-buster
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

COPY recruitment /code/recruitment
COPY movies /code/movies
COPY manage.py /code/manage.py
COPY requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

CMD gunicorn recruitment.wsgi --bind 0.0.0.0:$PORT