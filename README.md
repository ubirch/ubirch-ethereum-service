# ubirch-ethereum-service
ubirch Ethereum based anchoring service. The ethereum library requires Python >= 3.5.

An Ethereum based anchoring service. Master sends the messages one by one while fix_storing sends them in a bundle.
After a few tests I remarked that sending them one by one seems more time efficient.

## Documentation and requirements
This projects uses python 3.7 and the libraries needed are the following :
ethereum, json, sys, random, boto3 and argparse. Working with a venv is recommended.
Moreover, Elasticmq and Geth need to be properly installed.

-Elasticmq documentation : https://github.com/adamw/elasticmq

-Geth, the go implementation of the Ethereum protocol : https://github.com/ethereum/go-ethereum

## How to use this service :

1. Set up the elasticmq server : see https://github.com/adamw/elasticmq

2. Create a custom.conf so it looks like this :


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
  1. If you are on branch master :
  The service is connected via web3py to its own node on the Ropsten public testnet.



  2. If you are on branch privatetestnet :
  The service is connected via web3py a private testnet. Two nodes needs to be setup to mine the transactions.




5. Run the service ethereumService.py (you can run this script several times to increase the message procession speed). This script will either send errors to the errorQueue or store a Json file {status: status, hash : hash, txid : txid } in the Ethereum Blockchain and will also send this JSON to queue2.

6. Run the two scripts receiver.py and receiver_errors.py which will read the messages sent into the two queues.
