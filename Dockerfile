FROM python:3.9.9

ENV PYTHONUNBUFFERED 1

ADD . /var/src

RUN ls -lha /var/src

RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client

RUN mkdir -p /var/src/assets
WORKDIR /var/src

# install dependencies
COPY ./requirements.txt /var/src
RUN pip install -r requirements.txt

# copy project code
COPY . /var/src

# run Django management commands at start
RUN python manage.py collectstatic --no-input

# expose the port 8000
EXPOSE 80

CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000", "--chdir", "/var/src/config/", "--reload"]