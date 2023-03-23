FROM python:2.7-slim

ARG BASIC_AUTH_USERNAME_ARG
ARG BASIC_AUTH_PASSWORD_ARG

ENV BASIC_AUTH_USERNAME=$BASIC_AUTH_USERNAME_ARG
ENV BASIC_AUTH_PASSWORD=$BASIC_AUTH_PASSWORD_ARG

COPY ./requirements.txt /usr/requirements.txt

WORKDIR /usr

COPY ./src /usr/src
COPY ./models /usr/models

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "src/app/main.py" ]