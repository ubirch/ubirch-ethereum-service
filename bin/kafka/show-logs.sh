#!/usr/bin/env bash

cd ../../dependencies/kafka
./bin/kafka-run-class.sh kafka.tools.DumpLogSegments --deep-iteration --print-data-log --files /tmp/kafka-logs/$1-0/00000000000000000000.log

