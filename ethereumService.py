# coding: utf-8

import Library.serviceLibrary as service
import time
import binascii

args = service.set_arguments("ethereum")

url = args.url
region = args.region
aws_secret_access_key = args.accesskey
aws_access_key_id = args.keyid

queue1 = service.getQueue('queue1', url, region, aws_secret_access_key, aws_access_key_id)
queue2 = service.getQueue('queue2', url, region, aws_secret_access_key, aws_access_key_id)
errorQueue = service.getQueue('errorQueue', url, region, aws_secret_access_key, aws_access_key_id)


"""

 geth --rinkeby --datadir /Users/victor/Documents/ubirch-ethereum-service/Rinkeby --fast --rpc --rpcapi db,eth,net,web3,personal --cache=1024  --rpcport 8545 --rpcaddr 0.0.0.0 --rpccorsdomain "*" --bootnodes=enode://a24ac7c5484ef4ed0c5eb2d36620ba4e4aa13b8c84684e1b4aab0cebea2ae45cb4d375b77eab56516d34bfbd3c1a833fc51296ff084b770b94fb9028c4d25ccf@52.169.42.101:30303
 geth --testnet --syncmode "fast" --rpc --rpcapi db,eth,net,web3,personal --cache=1024  --rpcport 8545 --rpcaddr 0.0.0.0 --rpccorsdomain "*"
0x5e1ad4752d5e947f078eacb94c4263293066cec0 / 123
"""

from web3 import Web3, HTTPProvider, IPCProvider
from web3.middleware import geth_poa_middleware

w3 = Web3(HTTPProvider("http://localhost:8545"))
#w3 = Web3(IPCProvider('/Users/victor/Library/Ethereum/rinkeby/geth.ipc'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
print(w3.version.node)

# w3 = Web3(HTTPProvider("https://rinkeby.infura.io/v3/966a3923b3bb4df29cb31db87901700b")) #Infura hosted node : linked to my infura account


#Ether can be mined or demanded through the Faucet service

# # ROPSTEN ADDRESSES
# sender_address = Web3.toChecksumAddress('0x7fd1e740c2280c454d4d9c1585da9ccdd13cbcdc')
# sender_private_key = '45202060464c0f2f789d12da40422d878db3c5c58e69de9c4ea1b441df48d160'
#
# receiver_address = '0x216913375bA97E1E51E0018A9bbF1378350bDB63'


#RINKEBY ADDRESSES :
# sender_address = '0x4d3534E41539E50407795956B14154d63B0420c0'
# sender_private_key = '230e5b00b267299dacb01379e018d80f8c1e7088e3051f0a837aa1b473e2a236'
#
# receiver_address = '0x3C82C1808007fF8aCb254E599752cc456cD756BA'


sender_address = w3.eth.coinbase
password = '123'

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

        #signed_txn = w3.eth.account.signTransaction(txn_dict, sender_private_key) # For remotes nodes like Infura

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


storeStringETH('123456') #For testing

# main(storeStringETH)