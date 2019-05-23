#!/usr/bin/env sh

python ethereum_service.py -s ${SERVER} -ll ${LOGLEVEL} -nt "${NETWORKTYPE}" -ni "${NETWORKINFO}" -n ${ETH_NODE} -a ${ETH_ADDRESS} -kf ${KEYFILE} -pwd ${KEYFILE_PWD} -g ${GAS} -gp ${GASPRICE} -cid ${CHAINID} -bs ${KAFKA_BOOTSTRAP_SERVER} -i ${INPUT} -o ${OUTPUT} -e ${ERRORS}
#-u "${SQS_URL}" -r "${SQS_REGION}" -ak "${SQS_SECRET_ACCESS_KEY}" -ki "${SQS_KEY_ID}"
