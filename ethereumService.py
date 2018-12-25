# coding: utf-8

# Copyright (c) 2018 ubirch GmbH.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import binascii
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

from lib import *
from kafka import *

args = set_arguments("ethereum")
server = args.server

# To unlock your wallet
password = args.pwd
keyfile = args.keyfile


if server == 'SQS':
    print("SERVICE USING SQS QUEUE MESSAGING")
    url = args.url
    region = args.region
    aws_secret_access_key = args.accesskey
    aws_access_key_id = args.keyid
    queue1 = getQueue('queue1', url, region, aws_secret_access_key, aws_access_key_id)
    queue2 = getQueue('queue2', url, region, aws_secret_access_key, aws_access_key_id)
    errorQueue = getQueue('errorQueue', url, region, aws_secret_access_key, aws_access_key_id)
    producer=None

elif server == 'KAFKA':
    print("SERVICE USING APACHE KAFKA FOR MESSAGING")
    port = args.port
    producer = KafkaProducer(bootstrap_servers=port)
    queue1 = KafkaConsumer('queue1', bootstrap_servers=port)
    queue2=None
    errorQueue=None

w3 = Web3(HTTPProvider("http://localhost:8545"))
w3.middleware_stack.inject(geth_poa_middleware, layer=0) # Because we are on a Proof of Authority based ETH testnet
print(w3.version.node)


# This is my account, create a new one and change this address to use the service
sender_address = "0x31c2CC8b7f15F0A9e7efFdd5Fa02e37E66257744"
print('sender address :', sender_address)
print('sender balance (in Wei):', w3.eth.getBalance(sender_address))

"""Account on My Ether Wallet and keystore file stored on my machine"""
with open(keyfile) as kf:
    encrypted_key = kf.read()
    private_key = w3.eth.account.decrypt(encrypted_key, password)


def storeStringETH(string):
    """ Stores a string into the Ethereum blockchain
        Returns either False if the string is non hex, either dict with the txid and the string values
        after the tx is mined (with the value 'added' for the key 'status').
        If after 300sec the tx was still not mined,
        returns a dict specifying the string concerned and a 'timeout' value for the key 'status' """

    if is_hex(string):
        nonce = w3.eth.getTransactionCount(sender_address)
        print("Nonce = ", nonce)
        txn_dict = {                                        # Note that the address must be in checksum format ( Web3.toChecksumAddress(lower case address) to convert
            'to': sender_address,
            'from': sender_address,                         # From is an optional field
            'value': 0,
            'data': string,
            'gas': 640000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
            'chainId': 4       # 3 is the chainId of the Ropsten testnet, 4 is the one of Rinkeby
        }

        signed_tx = w3.eth.account.signTransaction(txn_dict, private_key)

        txn_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        txn_hash_str = binascii.hexlify(txn_hash).decode('utf-8')

        txn_receipt = None
        count = 0
        while txn_receipt is None and (count < 30): # We wait until our tx is mined
            txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
            print(txn_receipt)
            count += 1
            time.sleep(10)

        if txn_receipt is None:
            print({'status': 'timeout', 'message': string})
            return {'status': 'timeout', 'message': string}

        print({'status': 'added', 'txid': txn_hash_str, 'message': string})
        return {'status': 'added', 'txid': txn_hash_str, 'message': string}

    else:
        return False

def main(storefunction):
    """Continuously polls the queue for messages
    Anchors a hash from queue1
    Sends the TxID + hash (json file) in queue2 and errors are sent in errorQueue
    Runs continuously (check if messages are available in queue1)"""
    while True:
        poll(queue1, errorQueue, queue2, storefunction, server, producer)


main(storeStringETH)