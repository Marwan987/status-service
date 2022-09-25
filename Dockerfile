FROM python:3.6-slim-buster

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

RUN mkdir /app && chown python:python /app

WORKDIR /app


COPY  --chown=python:python requirements.txt requirements.txt

RUN pip3 install  -r requirements.txt

USER python

COPY --chown=python:python . .


CMD [ "python3", "status.py"]
