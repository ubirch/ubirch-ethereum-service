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
Wallets:
The testnet wallets were created using the client Metamask in the Chrome browser

Node: Finally, because we’re going to be working with the Ropsten TestNet without hosting our own node, 
we need a provider that we can connect the Blockchain through. Infura.io works well for this, so go and create a free 
account over there. Note down your provider url for the Ropsten TestNet. 

Transaction: The transaction parameter should be a dictionary with the following fields. from: bytes or text, 
hex address or ENS name - (optional, default: web3.eth.defaultAccount) The address the transaction is send from. to: 
bytes or text, hex address or ENS name - (optional when creating new contract) The address the transaction is 
directed to. gasPrice: integer - (optional, default: To-Be-Determined) Integer of the gasPrice used for each paid gas 
value: integer - (optional) Integer of the value send with this transaction data: bytes or text - The compiled code 
of a contract OR the hash of the invoked method signature and encoded parameters. For details see Ethereum Contract 
ABI. nonce: integer - (optional) Integer of a nonce. This allows to overwrite your own pending transactions that use 
the same nonce. 

If the transaction specifies a data value but does not specify gas then the gas value will be populated using the 
estimateGas() function with an additional buffer of 100000 gas up to the gasLimit of the latest block. In the event 
that the value returned by estimateGas() method is greater than the gasLimit a ValueError will be raised. 

"""

from web3 import Web3, HTTPProvider


w3 = Web3(HTTPProvider("http://localhost:8545"))
# w3 = Web3(HTTPProvider("https://rinkeby.infura.io/v3/966a3923b3bb4df29cb31db87901700b")) #Infura hosted node : linked to my infura account


# GETH
#geth --rpc --rpcapi="db,eth,net,web3,personal,web3" --testnet --fast --bootnodes "enode://6332792c4a00e3e4ee0926ed89e0d27ef985424d97b6a45bf0f23e51f0dcb5e66b875777506458aea7af6f9e4ffb69f43f3778ee73c81ed9d34c51c4b16b0b0f@52.232.243.152:30303,enode://94c15d1b9e2fe7ce56e458b9a3b672ef11894ddedd0c6f247e0f1d3487f52b66208fb4aeb8179fce6e3a749ea93ed147c37976d67af557508d199d9594c35f09@192.81.208.223:30303"

# geth --rinkeby --fast --rpc --rpcaddr 0.0.0.0 --rpcport 8545 --rpcapi="db,eth,net,web3,personal,web3" console
# geth --testnet --fast --rpc --rpcport 8545 --rpccorsdomain "*" --bootnodes console

#w3 = Web3(HTTPProvider("http://localhost:8545"))

# TODO : WALLET MANAGEMENT

# Created via MyEtherWallet.com or MetaMask / Ether can be mined or demanded through the Ropsten Faucet

# # ROPSTEN ADDRESSES
sender_address = Web3.toChecksumAddress('0x7fd1e740c2280c454d4d9c1585da9ccdd13cbcdc')
sender_private_key = '45202060464c0f2f789d12da40422d878db3c5c58e69de9c4ea1b441df48d160'

receiver_address = '0x216913375bA97E1E51E0018A9bbF1378350bDB63'


# RINKEBY ADDRESSES :
# sender_address = '0x4d3534E41539E50407795956B14154d63B0420c0'
# sender_private_key = '230e5b00b267299dacb01379e018d80f8c1e7088e3051f0a837aa1b473e2a236'
#
# receiver_address = '0x3C82C1808007fF8aCb254E599752cc456cD756BA'


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
            'chainId': 3        # 3 is the chainId of the Ropsten testnet
        }

        #signed_txn = w3.eth.account.signTransaction(txn_dict, sender_private_key)

        #w3.personal.unlockAccount(sender_address, '123')
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

print(w3.eth.net.getId())
print(w3.eth.getBalance(sender_address))
# print(w3.eth.gasPrice)
# print(w3.eth.getBlock('latest')['number'])

storeStringETH('123456')