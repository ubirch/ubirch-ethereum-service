FROM python:3.6-alpine

LABEL description="ubirch Ethereum anchoring service"

ARG KEYFILE

WORKDIR /ethereum-service/

RUN apk update
RUN apk add build-base libffi-dev openssl-dev

COPY requirements.txt /ethereum-service/
RUN pip install -r requirements.txt

COPY ubirch-ethereum-service/ethereum_service.py /ethereum-service/
COPY start.sh /ethereum-service/
RUN chmod +x ./start.sh

COPY ${KEYFILE} /ethereum-service/keyfile

ENV LOGLEVEL="DEBUG"
ENV KEYFILE=keyfile

CMD ["./start.sh"]