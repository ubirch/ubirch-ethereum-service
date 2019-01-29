FROM python:3.6

LABEL description="ubirch Ethereum anchoring service"

ARG KEYFILE

WORKDIR /ethereum-service/

COPY requirements.txt /ethereum-service/
RUN pip install -r requirements.txt

COPY ubirch-ethereum-service/ethereum_service.py /ethereum-service/
COPY start.sh /ethereum-service/
RUN chmod +x ./start.sh

COPY ${KEYFILE} /ethereum-service/keyfile

ENV LOGLEVEL="DEBUG"
ENV KEYFILE=keyfile

CMD ["./start.sh"]