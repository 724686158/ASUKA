FROM  ubuntu:16.04

WORKDIR /asuka

EXPOSE 8000

COPY requirements.txt /
RUN pip install  --no-cache-dir  -r /requirements.txt
