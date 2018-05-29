FROM  ubuntu:16.04

WORKDIR /ASUKA

EXPOSE 28080

COPY . /ASUKA

COPY requirements.txt /
RUN pip install  --no-cache-dir  -r /requirements.txt

CMD ["/ASUKA/run.sh"]