FROM python:3.7-alpine

RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev

COPY . .
RUN mkdir photo

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN crontab crontab

CMD ["crond", "-f"]