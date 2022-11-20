FROM python:3.10.8
ENV PYTHONUNBUFFERED 1
WORKDIR /djangoservice
ADD . /djangoservice/
RUN pip install -r requirements.txt