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

from ubirch.anchoring import *
from kafka import *

import logging
from logging.handlers import RotatingFileHandler


""" 
    The code below is used to initialize parameters passed in arguments in the terminal.
    Before starting the service one must choose between --server='SQS' or --server='KAFKA' depending on the message
    queuing service desired.
    Depending on the server chosen, several arguments of configuration of the latest are initialized.

"""

args = set_arguments("ethereum")
server = args.server


"""
    Logger & handlers configuration
"""

log_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'error': logging.ERROR,
}


logger = logging.getLogger('ubirch-ethereum-service')
level = log_levels.get(args.loglevel.lower())
logger.setLevel(level)


# Formatter adding time, name and level of each message when a message is written in the logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Handler redirecting logs in a file in 'append' mode, with 1 backup and 1Mo max size
file_handler = RotatingFileHandler('ethereum_service.log', mode='a', maxBytes=1000000, backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler on the console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


logger.info("You are using ubirch's Ethereum anchoring service")

if server == 'SQS':
    logger.info("SERVICE USING SQS QUEUE MESSAGING")

    url = args.url
    region = args.region
    aws_secret_access_key = args.accesskey
    aws_access_key_id = args.keyid

    input_messages = get_queue(args.input, url, region, aws_secret_access_key, aws_access_key_id)
    output_messages = get_queue(args.output, url, region, aws_secret_access_key, aws_access_key_id)
    error_messages = get_queue(args.errors, url, region, aws_secret_access_key, aws_access_key_id)
    producer = None

elif server == 'KAFKA':
    logger.info("SERVICE USING APACHE KAFKA FOR MESSAGING")

    output_messages = args.output
    error_messages = args.errors

    bootstrap_server = args.bootstrap_server
    producer = KafkaProducer(bootstrap_servers=bootstrap_server)
    input_messages = KafkaConsumer(args.input, bootstrap_servers=bootstrap_server)


node_address = args.node
logger.info("connected to node: %s" % node_address)
w3 = Web3(HTTPProvider(node_address))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)  # Because we are on a Proof of Authority based ETH testnet
logger.info(w3.version.node)


"""
    This is my account, create a new one and change this address to use the service
    It will generate a new address & associated private key in a password encrypted file
"""
sender_address = args.address
logger.info('sender address : %s' % sender_address)
logger.info('sender balance (in Wei): %s' % str(w3.eth.getBalance(sender_address)))

"""
    Account on My Ether Wallet and keystore file stored on my machine
"""
password = args.pwd
keyfile = args.keyfile

with open(keyfile) as kf:
    encrypted_key = kf.read()
    private_key = w3.eth.account.decrypt(encrypted_key, password)


def store_eth(string):
    """
        Stores a string into the Ethereum blockchain
        Returns either False if the string is non hex, either dict with the txid and the string values
        after the tx is mined (with the value 'added' for the key 'status').
        If after 300sec the tx was still not mined,
        returns a dict specifying the string concerned and a 'timeout' value for the key 'status'

        Note that the address must be in checksum format
            To do conversion: Web3.toChecksumAddress(lower case address)
         :param string: message to be sent in the IOTA transaction
    :return: If the input string is hexadecimal : a dictionary containing the string sent in the transaction
    and the transaction hash.
            If not : False
    :rtype: Dictionary if the input string is hexadecimal or boolean if not.

    """

    if is_hex(string):
        logger.debug("'%s' ready to be sent" % string)
        nonce = w3.eth.getTransactionCount(sender_address)
        logger.info("Nonce = %s" % nonce)
        txn_dict = {
            'to': sender_address,
            'from': sender_address,  # From is an optional field
            'value': 0,
            'data': string,
            'gas': 640000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
            'chainId': 4  # 3 is the chainId of the Ropsten testnet, 4 is the one of Rinkeby
        }

        signed_tx = w3.eth.account.signTransaction(txn_dict, private_key)

        txn_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        txn_hash_str = binascii.hexlify(txn_hash).decode('utf-8')

        txn_receipt = None
        count = 0
        while txn_receipt is None and (count < 30): # We wait until our tx is mined
            txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
            logger.debug(txn_receipt)
            count += 1
            time.sleep(10)

        if txn_receipt is None:
            logger.info({'status': 'timeout', 'message': string})
            return {'status': 'timeout', 'message': string}

        logger.debug("'%s' sent" % string)
        logger.info({'status': 'added', 'txid': txn_hash_str, 'message': string})
        return {'status': 'added', 'txid': txn_hash_str, 'message': string}

    else:
        return False


def main(store_function):
    """
        Continuously polls the queue for messages
        Anchors a hash from input_messages
        Sends the TxID + hash (json file) in output_messages and errors are sent in error_messages
        Runs continuously (check if messages are available in input_messages)
    """
    while True:
        poll(input_messages, error_messages, output_messages, store_function, server, producer)


main(store_eth)
