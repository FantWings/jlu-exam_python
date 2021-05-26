
# build stage
FROM python:3.9-rc-buster as builder

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt && \
    pip install --no-cache-dir pyinstaller

# build exec files
WORKDIR /opt/src
COPY . .
RUN pyinstaller -D wsgi.py


# run stage
FROM python:3.9.5-slim-buster

WORKDIR /opt/jlu_helper
COPY --from=builder /opt/src/dist/wsgi .

ENV SQL_USER=username
ENV SQL_PASS=password
ENV SQL_HOST=hostname
ENV SQL_PORT=3306
ENV SQL_BASE=basename
ENV FLASK_ENV=production

EXPOSE 9090

ENTRYPOINT [ "./wsgi"]