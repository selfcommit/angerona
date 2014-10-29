FROM dockerfile/python
MAINTAINER Peter Grace, pete.grace@gmail.com

RUN apt-get update
RUN apt-get install -y supervisor unixodbc-dev tdsodbc freetds-dev freetds-bin freetds-common unixodbc 

ADD docker/odbcinst.ini /etc/odbcinst.ini
ADD docker/odbc.ini /etc/odbc.ini

ADD . /opt/angerona

WORKDIR /opt/angerona
RUN ["python", "setup.py", "install"]

ADD docker/supervisor-system.conf /etc/supervisor/conf.d/system.conf
ADD docker/supervisor-gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

CMD ["/usr/bin/supervisord"]
EXPOSE 16543
