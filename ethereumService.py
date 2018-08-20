# coding: utf-8

import json
import sys
import random

import time
import Library.ElasticMQ_Connection as EMQ
import Library.serviceLibrary as service


args = service.set_arguments("ethereum")

url = args.url
region = args.region
aws_secret_access_key = args.accesskey
aws_access_key_id = args.keyid

queue1 = EMQ.getQueue('queue1', url, region, aws_secret_access_key, aws_access_key_id)
queue2 = EMQ.getQueue('queue2', url, region, aws_secret_access_key, aws_access_key_id)
errorQueue = EMQ.getQueue('errorQueue', url, region, aws_secret_access_key, aws_access_key_id)

from web3 import Web3, HTTPProvider
import web3


"""

TESTNET WALLET CREATED WITH METAMASK CLIENT

Finally, because we’re going to be working with the Ropsten TestNet without hosting our own node, we need a provider that we can connect the Blockchain through.
Infura.io works well for this, so go and create a free account over there.
Note down your provider url for the Ropsten TestNet.

"""

sender_address = "0x14a85df9b0d2cc905ed2491545dbc23b39c4708f"

receiver_address = "0x7fd1e740c2280c454d4d9c1585da9ccdd13cbcdc"

w3 = Web3(HTTPProvider(["ropsten.infura.io/v3/966a3923b3bb4df29cb31db87901700b"]))


def main(queue_name, storefunction):
    """Continuously polls the queue for messages"""
    while True:
        service.poll(queue1, errorQueue, queue2, storefunction)


"""
The transaction parameter should be a dictionary with the following fields.

from: bytes or text, hex address or ENS name - (optional, default: web3.eth.defaultAccount) The address the transaction is send from.
to: bytes or text, hex address or ENS name - (optional when creating new contract) The address the transaction is directed to.
gas: integer - (optional, default: 90000) Integer of the gas provided for the transaction execution. It will return unused gas.
gasPrice: integer - (optional, default: To-Be-Determined) Integer of the gasPrice used for each paid gas
value: integer - (optional) Integer of the value send with this transaction
data: bytes or text - The compiled code of a contract OR the hash of the invoked method signature and encoded parameters. For details see Ethereum Contract ABI.
nonce: integer - (optional) Integer of a nonce. This allows to overwrite your own pending transactions that use the same nonce.


If the transaction specifies a data value but does not specify gas then the gas value will be populated using the estimateGas()
function with an additional buffer of 100000 gas up to the gasLimit of the latest block.
In the event that the value returned by estimateGas() method is greater than the gasLimit a ValueError will be raised.

"""


def storeStringETH(string):
    transaction = {'to': receiver_address, 'from': sender_address, 'value': 0, 'data': string}
    txhash = web3.eth.sendTransaction(transaction)
    return txhash


main(queue1, storeStringETH)
