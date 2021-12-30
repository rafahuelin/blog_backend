FROM python:3.9.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client

RUN mkdir -p /var/src/assets
WORKDIR /var/src

# install dependencies
COPY requirements.txt /var/src
RUN pip install -r requirements.txt

# copy project code
COPY . /var/src/

# run Django management commands at start
RUN python manage.py collectstatic --no-input

# expose the port 80
EXPOSE 80

CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:80", "--chdir", "/var/src/config/", "--reload"]