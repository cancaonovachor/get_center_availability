# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7

# chrome-driver用のライブラリ(これを入れないとエラーになる)
RUN apt-get update && apt-get install -y libnss3-dev

# ローカルのファイルをコンテナへ移す
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# pipenv install
RUN pip install pipenv

# Pipfileからインストール. ただしpipenvの仮想環境は作らずにcontainerに直接入れる
RUN pipenv install --system

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app