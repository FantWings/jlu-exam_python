FROM python:3.9-rc-buster

WORKDIR /opt/url
COPY . .

RUN pip install --no-cache-dir -r ./requirements.txt && \
    chown 1000:1000 -R /opt/url

EXPOSE 9090

ENV SQL_USER=username
ENV SQL_PASS=password
ENV SQL_HOST=hostname
ENV SQL_PORT=3306
ENV SQL_BASE=basename
ENV EXEC_TOKEN=token

ENTRYPOINT [ "uwsgi", "-w", "wsgi:app", "--uid", "1000", "--http", ":9090","--master", "--workers", "3"]