FROM python:3-alpine
LABEL maintainer="zoe@complicity.co.uk"
RUN apk add build-base python3-dev
RUN pip install requests
COPY solarlog.py /app/
WORKDIR /app
CMD python3 ./solarlog.py
