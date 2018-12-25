#!/usr/bin/env bash

cd ../../dependencies/kafka_2.11-2.0.0
./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic $1