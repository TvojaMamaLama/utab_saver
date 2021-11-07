FROM python:3.8-slim

ENV BOT_TOKEN ${BOT_TOKEN}

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev

ADD requirements.txt /

RUN pip install -r requirements.txt

WORKDIR /srv

ADD src /srv

CMD python app.py