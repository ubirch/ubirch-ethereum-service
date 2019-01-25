#!/usr/bin/env bash

python iota_service.py -s ${SERVER} -ll ${LOGLEVEL} -n ${ETH_NODE} -a ${ETH_ADDRESS} -kf ${KEYFILE_PATH} -pwd ${KEYFILE_PWD} -p ${KAFKA_PORT} -u ${SQS_URL} -r ${SQS_REGION} -ak ${SQS_SECRET_ACCESS_KEY} -ki ${SQS_KEY_ID}
