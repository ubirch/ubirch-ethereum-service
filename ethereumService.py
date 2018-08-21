# coding: utf-8

import Library.ElasticMQ_Connection as EMQ
import Library.serviceLibrary as service
import time
import binascii



args = service.set_arguments("ethereum")

url = args.url
region = args.region
aws_secret_access_key = args.accesskey
aws_access_key_id = args.keyid

queue1 = EMQ.getQueue('queue1', url, region, aws_secret_access_key, aws_access_key_id)
queue2 = EMQ.getQueue('queue2', url, region, aws_secret_access_key, aws_access_key_id)
errorQueue = EMQ.getQueue('errorQueue', url, region, aws_secret_access_key, aws_access_key_id)


"""
Wallets:
The testnet wallets were created using the client Metamask in the Chrome browser

Node:
Finally, because we’re going to be working with the Ropsten TestNet without hosting our own node, we need a provider that we can connect the Blockchain through.
Infura.io works well for this, so go and create a free account over there.
Note down your provider url for the Ropsten TestNet.

Transaction:
The transaction parameter should be a dictionary with the following fields.
from: bytes or text, hex address or ENS name - (optional, default: web3.eth.defaultAccount) The address the transaction is send from.
to: bytes or text, hex address or ENS name - (optional when creating new contract) The address the transaction is directed to.
gasPrice: integer - (optional, default: To-Be-Determined) Integer of the gasPrice used for each paid gas
value: integer - (optional) Integer of the value send with this transaction
data: bytes or text - The compiled code of a contract OR the hash of the invoked method signature and encoded parameters. For details see Ethereum Contract ABI.
nonce: integer - (optional) Integer of a nonce. This allows to overwrite your own pending transactions that use the same nonce.

If the transaction specifies a data value but does not specify gas then the gas value will be populated using the estimateGas()
function with an additional buffer of 100000 gas up to the gasLimit of the latest block.
In the event that the value returned by estimateGas() method is greater than the gasLimit a ValueError will be raised.

"""

from web3 import Web3, HTTPProvider
import web3

w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/966a3923b3bb4df29cb31db87901700b")) #Infura hosted node : linked to my infura account

# Created via MyEtherWallet.com
# Ether can be mined or demanded through the Ropsten Faucet

# sender_address = "0x8e0efc639A218c502542E0A8f0213feF50a45c06"
# sender_private_key = '6647b8834bc0a9d3e494dc1ecaed8bdde02820e4db45275b26ce0080b2c0f8f9'

receiver_address = '0x216913375bA97E1E51E0018A9bbF1378350bDB63'

sender_address = Web3.toChecksumAddress('0x7fd1e740c2280c454d4d9c1585da9ccdd13cbcdc')
sender_private_key = '45202060464c0f2f789d12da40422d878db3c5c58e69de9c4ea1b441df48d160'


# myAccount = w3.eth.account.create('put some extra entropy here')
# myAddress = myAccount.address
# myPrivateKey = myAccount.privateKey
# print('my address is     : {}'.format(myAccount.address))
# print('my private key is : {}'.format(myAccount.privateKey.hex()))


print(w3.eth.getBalance(sender_address))


def main(storefunction):
    """Continuously polls the queue for messages"""
    while True:
        service.poll(queue1, errorQueue, queue2, storefunction)


# def storeStringETH(string):
#     if service.is_hex(string):
#         nonce = w3.eth.getTransactionCount(sender_address)
#         txn_dict = { # Note that the address must be in checksum format
#             'to': receiver_address,
#             'from': sender_address,
#             'value': 50000000000,
#             'gas': 2000000,
#             'gasPrice': w3.toWei('40', 'gwei'),
#             'nonce': nonce,
#             'chainId': 20
#         }
#         signed_txn = w3.eth.account.signTransaction(txn_dict, sender_private_key)
#         print(signed_txn)
#
#         #w3.eth.sendTransaction(txn_dict) not allowed by infura
#
#         txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
#         print(binascii.hexlify(txn_hash))
#
#         txn_receipt = None
#         count = 0
#         while txn_receipt is None and (count < 30):
#             txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
#
#             print(txn_receipt)
#
#             time.sleep(10)
#
#         if txn_receipt is None:
#             return {'status': 'failed', 'error': 'timeout'}
#
#         return {'status': 'added', 'txn_receipt': txn_receipt, 'txn_hash': binascii.hexlify(txn_hash)}
#
#     else:
#         return False

def storeStringETH(string):
    if service.is_hex(string):
        txn_dict = { # Note that the address must be in checksum format
            'to': receiver_address,
          #  'from': sender_address,
            'value': 1000000000000,
            'gas': 200000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': 0,
            'chainId': 20
        }
        signed_txn = w3.eth.account.signTransaction(txn_dict, sender_private_key)
        print(signed_txn)

        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(binascii.hexlify(txn_hash))

        txn_receipt = None
        count = 0
        while txn_receipt is None and (count < 30):
            txn_receipt = w3.eth.getTransactionReceipt(txn_hash)

            print(txn_receipt)

            time.sleep(10)

        if txn_receipt is None:
            return {'status': 'failed', 'error': 'timeout'}

        return {'status': 'added', 'txn_receipt': txn_receipt, 'txn_hash': binascii.hexlify(txn_hash)}

    else:
        return False


storeStringETH("abc")