FROM python:3.6

LABEL description="ubirch Ethereum anchoring service"


ARG LOGLEVEL='DEBUG'

ARG ETH_NODE="http://localhost:8545"
ARG ETH_ADDRESS='0x31c2CC8b7f15F0A9e7efFdd5Fa02e37E66257744'

ARG KAFKA_PORT=['localhost:9092']

ARG SQS_URL="http://localhost:9324"
ARG SQS_REGION="elasticmq"
ARG SQS_SECRET_ACCESS_KEY="x"
ARG SQS_KEY_ID="x"

# Choice between SQS or KAFKA and choice of LOGLEVEL
ENV SERVER=${SERVER}
ENV LOGLEVEL=${LOGLEVEL}

# Ethereum configuration
ENV ETH_NODE=${ETH_NODE}
ENV ETH_ADDRESS=${ETH_ADDRESS}
ENV KEYFILE_PATH=${KEYFILE_PATH}
ENV KEYFILE_PWD=${KEYFILE_PWD}

ENV KAFKA_PORT=${KAFKA_PORT}

# Parametrizes the SQS server
ENV SQS_URL=${SQS_URL}
ENV SQS_REGION=${SQS_REGION}
ENV SQS_SECRET_ACCESS_KEY=${SQS_SECRET_ACCESS_KEY}
ENV SQS_KEY_ID=${SQS_KEY_ID}

WORKDIR /ethereum-service/

COPY requirements.txt /ethereum-service/
RUN pip install -r requirements.txt

COPY ubirch-ethereum-service/UTC--testing /ethereum-service

COPY ubirch-ethereum-service/ethereum_service.py /ethereum-service/

COPY start.sh /ethereum-service/
RUN chmod +x ./start.sh

CMD ["./start.sh"]