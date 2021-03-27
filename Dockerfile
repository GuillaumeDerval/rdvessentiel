FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN apk add postgresql-libs postgresql-dev
RUN apk add build-base
RUN pip install -r /var/www/requirements.txt

COPY . /app
