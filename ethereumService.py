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

# TODO : WALLET MANAGEMENT

# Created via MyEtherWallet.com or MetaMask / Ether can be mined or demanded through the Ropsten Faucet

sender_address = Web3.toChecksumAddress('0x7fd1e740c2280c454d4d9c1585da9ccdd13cbcdc')
sender_private_key = '45202060464c0f2f789d12da40422d878db3c5c58e69de9c4ea1b441df48d160'

receiver_address = '0x216913375bA97E1E51E0018A9bbF1378350bDB63'

print('sender address :', sender_address)
print('receiver address', receiver_address)
print('sender balance (in Wei):', w3.eth.getBalance(sender_address))

# Anchors a hash from queue1
# Sends the TxID + hash (json file) in queue2 and errors are sent in errorQueue
# Runs continuously (check if messages are available in queue1)


def main(storefunction):
    """Continuously polls the queue for messages"""
    while True:
        service.poll(queue1, errorQueue, queue2, storefunction)


def storeStringETH(string):
    if service.is_hex(string):
        nonce = w3.eth.getTransactionCount(sender_address)
        print("Nonce = ", nonce)
        txn_dict = {                                        # Note that the address must be in checksum format ( Web3.toChecksumAddress(lower case address) to convert
            'to': receiver_address,
            'from': sender_address,                         # from is an optional field
            'value': 600000000000,
            'data': string,
            'gas': 2000000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
            'chainId': 3        # 3 is the chainId of the Ropsten testnet
        }

        signed_txn = w3.eth.account.signTransaction(txn_dict, sender_private_key)

        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn_hash_str = binascii.hexlify(txn_hash).decode('utf-8')

        print({'status': 'added', 'txid': txn_hash_str, 'message': string})

        txn_receipt = None
        count = 0
        while txn_receipt is None and (count < 30):
            txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
            print(txn_receipt)
            count +=1
            time.sleep(10)

        if txn_receipt is None:
            print({'status': 'timeout', 'message': string})
            return {'status': 'timeout', 'message': string}

        return {'status': 'added', 'txid': txn_hash_str, 'message': string}

    else:
        return False


main(storeStringETH)