#!/usr/bin/env bash


TIMESTAMP=`date "+%Y%m%d%H%M"`
TAG="$TIMESTAMP-dev"
SERVICENAME="ubirch-ethereum-service"

docker build -t ubirch/${SERVICENAME} .
docker tag ubirch/${SERVICENAME}:latest ubirch/${SERVICENAME}:$TAG
docker push ubirch/${SERVICENAME}:latest
docker push ubirch/${SERVICENAME}:$TAG

echo "ubirch/${SERVICENAME}:$TAG"