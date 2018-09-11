# coding: utf-8

import Library.serviceLibrary as service
import time
import binascii

from web3 import Web3, HTTPProvider, IPCProvider
from web3.middleware import geth_poa_middleware

args = service.set_arguments("ethereum")


url = args.url
region = args.region
aws_secret_access_key = args.accesskey
aws_access_key_id = args.keyid
password = args.pwd

queue1 = service.getQueue('queue1', url, region, aws_secret_access_key, aws_access_key_id)
queue2 = service.getQueue('queue2', url, region, aws_secret_access_key, aws_access_key_id)
errorQueue = service.getQueue('errorQueue', url, region, aws_secret_access_key, aws_access_key_id)


w3 = Web3(HTTPProvider("http://localhost:8545"))

w3.middleware_stack.inject(geth_poa_middleware, layer=0)
print(w3.version.n




sender_address = "0x305152Bd0631070256e25F33A20fcBd6B1c665cd"

print('sender address :', sender_address)
print('sender balance (in Wei):', w3.eth.getBalance(sender_address))


def main(storefunction):
    """Continuously polls the queue for messages
    Anchors a hash from queue1
    Sends the TxID + hash (json file) in queue2 and errors are sent in errorQueue
    Runs continuously (check if messages are available in queue1)"""
    while True:
        service.poll(queue1, errorQueue, queue2, storefunction)


def storeStringETH(string):
    """ Stores a string into the Ethereum blockchain
        Returns either False if the string is non hex, either dict with the txid and the string values
        after the tx is mined (with the value 'added' for the key 'status').
        If after 300sec the tx was still not mined,
        returns a dict specifying the string concerned and a 'timeout' value for the key 'status' """

    if service.is_hex(string):
        nonce = w3.eth.getTransactionCount(sender_address)
        print("Nonce = ", nonce)
        txn_dict = {                                        # Note that the address must be in checksum format ( Web3.toChecksumAddress(lower case address) to convert
            'to': sender_address,
            'from': sender_address,                         # from is an optional field
            'value': 0,
            'data': string,
            'gas': 640000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
            'chainId': 4       # 3 is the chainId of the Ropsten testnet, 4 is the one of rinkeby
        }

        w3.personal.unlockAccount(sender_address, password)
        txn_hash = w3.eth.sendTransaction(txn_dict)
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

main(storeStringETH)