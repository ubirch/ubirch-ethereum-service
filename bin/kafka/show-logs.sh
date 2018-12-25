#!/usr/bin/env bash

cd ../../dependencies/kafka_2.11-2.0.0
./bin/kafka-run-class.sh kafka.tools.DumpLogSegments --deep-iteration --print-data-log --files /tmp/kafka-logs/$1-0/00000000000000000000.log

