# ubirch-ethereum-service
ubirch Ethereum based anchoring service

An Ethereum based anchoring service. Master sends the messages one by one while fix_storing sends them in a bundle.
After a few tests I remarked that sending them one by one seems more time efficient.

## Documentation and requirements
This projects uses python 2.7 and the libraries needed are the following :
ethereum, json, sys, random and argparse. Working with a venv is recommended.

You can find documentation about elasticmq here : https://github.com/adamw/elasticmq 

You can find documentation about pyethereum here : https://github.com/ethereum/pyethereum


## How to use this service :

1. Set up the elasticmq server : https://github.com/adamw/elasticmq 

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

5. Run the service ethereumService.py (you can run this script several times to increase the message procession speed). This script will either send errors to the errorQueue or store a Json file {hash : hash ; txid : txid } in the Ethereum Blockchain and also send it to queue2.

6. Run the two scripts receiver.py and receiver_errors.py which will read messages sent into the two queues.
