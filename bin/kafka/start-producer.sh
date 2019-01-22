#!/usr/bin/env bash

cd ../../dependencies/kafka
./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic $1