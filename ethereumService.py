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

https://medium.com/mercuryprotocol/how-to-create-your-own-private-ethereum-blockchain-dad6af82fc9f

"""

from web3 import Web3, HTTPProvider


# GETH
# geth --rinkeby --rpc --rpcaddr 0.0.0.0 --rpcport 8545 --rpccorsdomain "*" console
# geth --testnet --fast --rpc --rpcaddr 0.0.0.0 --rpcport 8545 --rpccorsdomain "*" --bootnodes console

w3 = Web3(HTTPProvider("http://localhost:8545"))

# TODO : WALLET MANAGEMENT


#GETH ACCOUNT
#19fa6f349a1f3a9d1165ee0a22157f18b0f7d297 / pwd : test

#sender_address = Web3.toChecksumAddress("19fa6f349a1f3a9d1165ee0a22157f18b0f7d297"
sender_address = w3.eth.accounts[0]
password = 'test'

# Anchors a hash from queue1
# Sends the TxID + hash (json file) in queue2 and errors are sent in errorQueue
# Runs continuously (check if messages are available in queue1)


# myAccount = w3.eth.account.create('put some extra entropy here')
# myAddress = myAccount.address
# myPrivateKey = myAccount.privateKey
# print('my address is     : {}'.format(myAccount.address))
# print('my private key is : {}'.format(myAccount.privateKey.hex()))



def main(storefunction):
    """Continuously polls the queue for messages"""
    while True:
        service.poll(queue1, errorQueue, queue2, storefunction)


def storeStringETH(string):
    """ Stores a string into the Ethereum blockchain
        Returns either False if the string is non hex, either dict with the txid and the string values
        after the tx is mined (with the value 'added' for the key 'status').
        If after 300sec the tx was still not mined,
        returns a dict specifying the string concerned and a 'timeout' value for the key 'status'
        '3' is the chainId of the Ropsten testnet, see https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md
        for the list of chain ID's"""

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
            'chainId': 15
        }

        #signed_txn = w3.eth.account.signTransaction(txn_dict, sender_private_key)

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

print(w3.personal.listAccounts)
print(w3.eth.getBalance(sender_address))
print(w3.eth.getBlock('latest'))#OK
storeStringETH("0x123456")
