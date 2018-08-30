#!/usr/bin/env bash

geth --identity "MyTestNetNode" --nodiscover --networkid 1999 --datadir /Users/victor/Documents/ubirch-ethereum-service/privatetestnet/test-net-blockchain init /Users/victor/Documents/ubirch-ethereum-service/privatetestnet/genesis.json


geth --identity "MyTestNetNode2" --nodiscover --networkid 1999 --datadir /Users/victor/Documents/ubirch-ethereum-service/privatetestnet/test-net-blockchain2 init /Users/victor/Documents/ubirch-ethereum-service/privatetestnet/genesis.json
