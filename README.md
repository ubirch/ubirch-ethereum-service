# ubirch-ethereum-service
ubirch Ethereum based anchoring service. The ethereum library requires Python >= 3.5.

An Ethereum based anchoring service. Master sends the messages one by one while fix_storing sends them in a bundle.
After a few tests I remarked that sending them one by one seems more time efficient.

## Documentation and requirements
This projects uses python 3.7 and the libraries needed are the following :
web3py, json, sys, random, boto3 and argparse. Working with a venv is recommended.
Moreover, Elasticmq and Geth need to be properly installed.

-Elasticmq documentation : https://github.com/adamw/elasticmq

-Geth, the go implementation of the Ethereum protocol : https://github.com/ethereum/go-ethereum

-Web3py, a python library for interacting with Ethereum. Its API is derived from the Web3.js Javascript API : https://web3py.readthedocs.io/en/stable/
    
## How to use this service :

1. Install Geth (see : https://github.com/ethereum/go-ethereum/wiki/Building-Ethereum)

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

where x.x.x is the number of the version of elasticMQ

4. Once the server is running, start sender.py which will send via an infinite loop messages to the first queue (queue1). Those messages will mainly be hex strings (hashes) but there will be also be non hex-strings which will be processed as errors by the service.

5. Before running the service, you need to be connected to the Ethereum network.

  a. If you are on branch master :
  The service is connected via web3py to its own node on the Ropsten public testnet.



  b. If you are on branch privatetestnet :
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

and type personal.newAccount() in the console. This will give you an ETH address and ask you for a passphrase which you must not forget.

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

Now initialize a second node by changing only these two flags : --identity "MyTestNetNode2" and --datadir YOUR_DATADIR2, but keep the same genesis file (important).
Once the second node is initialized, connect to it (add the flags --rpcport 8546 --port 30304) and create an account by typing personal.newAccount() on the geth console. This address will serve of base address for the mining process.

Now, your two nodes should be running on the same network. Next, find the enode url of one of your nodes.
Enode url is like a unique id for nodes to communicate with each other

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

And type miner.stop() to stop the mining process.

6. Run the service ethereumService.py (you can run this script several times to increase the message procession speed). This script will either send errors to the errorQueue or store a Json file {status: status, hash : hash, txid : txid } in the Ethereum Blockchain and will also send this JSON to queue2.

7. Run the two scripts receiver.py and receiver_errors.py which will read the messages sent into the two queues.
