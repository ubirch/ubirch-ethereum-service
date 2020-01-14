#!/usr/bin/env sh

cd ubirch-ethereum-service

export SERVER=KAFKA

export LOGLEVEL=DEBUG
export NETWORKTYPE=TESTNET
export NETWORKINFO=TESTNET
export ETH_NODE=https://rinkeby.infura.io/v3/a0a7cbebdc4249c4b12fd8b76c608d25
export ETH_ADDRESS=0xC17E0AeB794Ccf893D77222fbeAe37a4dDf64d7F
export KEYFILE="/Volumes/Keybase/team/ubirch_coins/etererum/keystore/testnet-dev/UTC--2019-01-29T08-45-35.482266000Z--c17e0aeb794ccf893d77222fbeae37a4ddf64d7f"
export KEYFILE_PWD="9AJ]=2fz=6O5!!vb*:OSTSIn/epC(i"
export GAS=70000
export GASPRICE=30
export CHAINID=4
export KAFKA_BOOTSTRAP_SERVER=localhost:9092
export INPUT=eth_input
export OUTPUT=eth_output
export ERRORS=eth_error

python ethereum_service.py -s ${SERVER} -ll ${LOGLEVEL} -nt "${NETWORKTYPE}" -ni "${NETWORKINFO}" -n ${ETH_NODE} -a ${ETH_ADDRESS} -kf ${KEYFILE} -pwd ${KEYFILE_PWD} -g ${GAS} -gp ${GASPRICE} -cid ${CHAINID} -bs ${KAFKA_BOOTSTRAP_SERVER} -i ${INPUT} -o ${OUTPUT} -e ${ERRORS}
#-u "${SQS_URL}" -r "${SQS_REGION}" -ak "${SQS_SECRET_ACCESS_KEY}" -ki "${SQS_KEY_ID}"
