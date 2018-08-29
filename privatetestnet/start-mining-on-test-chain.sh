#!/usr/bin/env bash
geth --identity "MyTestNetNode" --datadir /Users/victor/Documents/ubirch-ethereum-service/privatetestnet/test-net-blockchain --nodiscover --rpc --rpcapi="db,eth,net,web3,personal,web3" --networkid 1999 --mine --minerthreads=1 --etherbase=0xc9bFfB5b6325C402B058Dd026e0985B338c92ac3

#geth --identity "MyTestNetNode2" --rpcport 8546 --port 30304 --datadir /Users/victor/Documents/ubirch-ethereum-service/privatetestnet/test-net-blockchain2 --nodiscover --rpc --rpcapi="db,eth,net,web3,personal,web3" --networkid 1999 --mine --minerthreads=1 --etherbase=0x5c4e80ccd1d96665a6b894cc2a6ead5286956d9a

