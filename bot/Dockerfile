FROM python:3.9-alpine

ARG TG_BOT_TOKEN
ARG YA_OAUTH_TOKEN
ARG FOLDER_ID

ENV TG_BOT_TOKEN=$TG_BOT_TOKEN
ENV YA_OAUTH_TOKEN=$YA_OAUTH_TOKEN
ENV FOLDER_ID=$FOLDER_ID

WORKDIR /bot

ADD . .

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install -r requirements.txt
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
