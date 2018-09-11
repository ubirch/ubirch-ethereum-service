# ubirch-ethereum-service

This ubirch service continously polls a queue (Queue1) and anchors its messages on the Ethereum blockchain.
Errors such as timeouts and non hex messages are sent into an errorQueue while the successful anchoring of an hexadecimal message results in the sending of a JSON file : {'status': 'added', 'txid': txid, 'message': message} in another queue (Queue2).

# Documentation and requirements
This projects uses python 3.7 and the libraries needed are the following :
web3py, json, sys, random, boto3 and argparse. <br>
Moreover, Elasticmq and Geth need to be properly installed.

-Elasticmq documentation : https://github.com/adamw/elasticmq

-Geth, the go implementation of the Ethereum protocol : https://github.com/ethereum/go-ethereum

-Web3py, a python library for interacting with Ethereum. Its API is derived from the Web3.js Javascript API : https://web3py.readthedocs.io/en/stable/
    
# How to use this service :

1. Install Geth, see : https://github.com/ethereum/go-ethereum/wiki/Building-Ethereum

2. Download ElasticMQ and create a custom.conf file so it looks like this :


        include classpath("application.conf")

        // What is the outside visible address of this ElasticMQ node
        // Used to create the queue URL (may be different from bind address!)
        node-address {
            protocol = http
            host = localhost
            port = 9324
            context-path = ""
        }

        rest-sqs {
            enabled = true
            bind-port = 9324
            bind-hostname = "0.0.0.0"
            // Possible values: relaxed, strict
            sqs-limits = strict
        }

        // Should the node-address be generated from the bind port/hostname
        // Set this to true e.g. when assigning port automatically by using port 0.
        generate-node-address = false


        queues {


          queue1 {
            defaultVisibilityTimeout = 10 seconds
            receiveMessageWait = 0 seconds
            deadLettersQueue {
                name = "queue1-dead-letters"
                maxReceiveCount = 10 // from 1 to 1000
            }
          }

            queue2 {
            defaultVisibilityTimeout = 10 seconds
            receiveMessageWait = 0 seconds
            deadLettersQueue {
                name = "queue2-dead-letters"
                maxReceiveCount = 10 // from 1 to 1000
            }
          }

            errorQueue {
            defaultVisibilityTimeout = 10 seconds
            receiveMessageWait = 0 seconds
            deadLettersQueue {
                name = "errorQueue-dead-letters"
                maxReceiveCount = 10 // from 1 to 1000
            }
          }

        }

3. Run it with :


        java -Dconfig.file=custom.conf -jar elasticmq-server-x.x.x.jar

where x.x.x is the number of the version of elasticMQ.

4. Once the server is running, start sender.py which will send via an infinite loop messages to the first queue (queue1). Those messages will mainly be hex strings (hashes) but there will be also be non hex-strings which will be processed as errors by the service.

5. Before running the service, you need to be connected to the Ethereum network.

<b>  a. If you are on branch master : </b> <br>

The service is connected via web3py to its own node on the Rinkeby public testnet, which is PoA (Proof of Authority) based.

UPDATE : Ubirch has now its own Rinkeby testnet node running on the strato server. If you wish to use this node, before running the service please run :
        
        ssh -L 8545:localhost:8545 user@hostname

<b> If you want to set up your own node : </b> <br>
Please visit : https://www.rinkeby.io/#geth and download rinkeby.json <br>


To initialize, execute:

    geth --datadir=YOUR_DATA_DIR init PATH_TO_rinkeby.json

Then, execute:

    geth --rinkeby --datadir YOUR_DATA_DIR --fast --rpc --rpcapi db,eth,net,web3,personal --cache=1024  --rpcport 8545 --rpcaddr 0.0.0.0 --rpccorsdomain "*" --bootnodes=enode://a24ac7c5484ef4ed0c5eb2d36620ba4e4aa13b8c84684e1b4aab0cebea2ae45cb4d375b77eab56516d34bfbd3c1a833fc51296ff084b770b94fb9028c4d25ccf@52.169.42.101:30303

To check the syncing, open another terminal and execute :

    geth --datadir YOUR_DATA_DIR attach

To check the syncing, execute in the Geth terminal:

    eth.syncing //output : false when fully synchronised
   
To create a new account :

    >personal.newAccount("notmyrealpassword")
    "0xb2e9fe08ca9a0323103883fe12c9609ed380f475"
    > eth.coinbase
    "0xb2e9fe08ca9a0323103883fe12c9609ed380f475"
    > eth.getBalance(eth.coinbase)
    0

To request ETH : https://faucet.rinkeby.io/ <br>
Once the node is up and running and you have an address with Rinkeby ETH on it, you can start the service.


<b>  b.  If you are on branch privatetestnet : </b> <br> 

The service is connected via web3py a private testnet. Two nodes needs to be setup to mine the transactions.

To set up the first node, please run :

        geth --identity "MyTestNetNode" --nodiscover --networkid 1999 --datadir YOUR_DATADIR init PATH_TO_GENESIS/genesis.json

where genesis.json looks like this:

        {
            "nonce": "0x0000000000001337",
            "timestamp": "0x0",
            "config": {
                "chainId": 15,
                "homesteadBlock": 0,
                "eip155Block": 0,
                "eip158Block": 0
            },
            "difficulty": "0x400",
            "gasLimit": "0x2100000"
          }
        }


Then run:

        geth --identity "MyTestNetNode" --datadir YOUR_DATADIR --nodiscover --rpc --networkid 1999 --rpcapi="db,eth,net,web3,personal,web3" console

and type in the console : 

        personal.newAccount()
        
This will give you an ETH address and ask you for a passphrase which you must not forget as it gives you access to your private key, and thus, to your money. <br>

Finally run:

        geth removedb --datadir YOURDATADIR

and:

        geth --identity "MyTestNetNode" --nodiscover --networkid 1999 --datadir YOUR_DATADIR init PATH_TO_GENESIS/genesis.json

with genesis.json looking like this:

        {
        "nonce": "0x0000000000001337",
        "timestamp": "0x0",
        "config": {
            "chainId": 15,
            "homesteadBlock": 0,
            "eip155Block": 0,
            "eip158Block": 0
        },
        "difficulty": "0x400",
        "gasLimit": "0x2100000",
        "alloc": {
            "Address1 just created": { "balance" : "0x1337000000000000000000"},
          }
}
    
<b> Now initialize a second node </b> by changing only these two flags : <b> --identity "MyTestNetNode2" </b> and <b> --datadir YOUR_DATADIR2 </b>, but you have keep the same genesis file. <br>
Once the second node is initialized, connect to it : <b> add the flags --rpcport 8546 --port 30304 </b> and create an account by typing on the geth console :

        personal.newAccount()
 
This address will serve of base address for the mining process. <br>
Now, your two nodes should be running on the same network. Next, find the enode url of one of your nodes.
Enode url is like a unique id for nodes to communicate with each other.

In the first terminal, (now it should be in the geth console)

        admin.nodeInfo.enode

The output should be like : 

        enode://b7cfadc86549c931be4e0ffca03299053b31dd40503313e05cbdc855399fca225623dd7e2e262a1f45e01137345641c4d90b88080cd678a03867f53bca890315@[::]:30302

Where [::] is equivalent to 127.0.0.1 (localhost) and 30302 is the port your node is running on.


Before connecting, there should be no peer right now

        web3.net.peerCount //output 0
    
In the second terminal,

        admin.addPeer(“enode_url_u_just_get_from_the_first_terminal”)
    
And then check if the node is successfully added

        web3.net.peerCount //output 1

Now that the nodes are connected to each other, in both terminals : 

        miner.start() //output true

And, to stop the mining process :

        miner.stop()

6. Run the service ethereumService.py (you can run this script several times to increase the message procession speed). <br> 
This script will either send errors to the errorQueue or store a Json file {status: status, hash : hash, txid : txid } in the Ethereum Blockchain and will also send this JSON to queue2.

7. Run the two scripts receiver.py and receiver_errors.py which will read the messages sent into the two queues.
