#!/usr/bin/env bash
geth --identity "MyTestNetNode" --datadir /Users/victor/Documents/ubirch-ethereum-service/privatetestnet/test-net-blockchain --nodiscover --rpc --networkid 1999 --rpcapi="db,eth,net,web3,personal,web3" console

#geth --identity "MyTestNetNode2" --rpcport 8546 --port 30304 --datadir /Users/victor/Documents/ubirch-ethereum-service/privatetestnet/test-net-blockchain2 --nodiscover --rpc --networkid 1999 --rpcapi="db,eth,net,web3,personal,web3" console
