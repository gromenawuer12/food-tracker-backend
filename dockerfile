FROM python:3.8-slim-buster
RUN apt-get update 
RUN apt-get -y install zip