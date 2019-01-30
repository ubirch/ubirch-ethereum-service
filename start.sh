#!/usr/bin/env bash

python ethereum_service.py -s ${SERVER} -ll ${LOGLEVEL} -n ${ETH_NODE} -a ${ETH_ADDRESS} -kf ${KEYFILE} -pwd ${KEYFILE_PWD} -bs ${KAFKA_BOOTSTRAP_SERVER} -i ${INPUT} -o ${OUTPUT} -e ${ERRORS}
#-u ${SQS_URL} -r ${SQS_REGION} -ak ${SQS_SECRET_ACCESS_KEY} -ki ${SQS_KEY_ID}