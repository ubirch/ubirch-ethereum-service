#!/usr/bin/env bash

cd ../../dependencies/kafka_2.11-2.0.0
./bin/kafka-topics.sh --list --zookeeper localhost:2181