FROM  django:latest

WORKDIR /ASUKA

EXPOSE 28080

COPY . /ASUKA

COPY requirements.txt /
RUN pip install  --no-cache-dir  -r /requirements.txt

RUN chmod a+x /ASUKA/run.sh

CMD ["/ASUKA/run.sh"]