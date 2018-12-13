#!/usr/bin/env bash

cd ../../kafka_2.11-2.0.0
./bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic $1
