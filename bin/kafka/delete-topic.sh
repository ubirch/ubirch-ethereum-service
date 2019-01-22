#!/usr/bin/env bash

cd ../../dependencies/kafka
./bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic $1
