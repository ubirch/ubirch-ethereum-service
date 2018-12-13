#!/usr/bin/env bash

cd ../../kafka_2.11-2.0.0
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic $1 --from-beginning