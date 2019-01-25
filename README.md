# ubirch-ethereum-service
This is a command line interface python service developed to anchor data on the Ethereum BLockchain.<br>

Default address used in the service:
**0x31c2CC8b7f15F0A9e7efFdd5Fa02e37E66257744**<br>
Click [here](https://rinkeby.etherscan.io/address/0x31c2CC8b7f15F0A9e7efFdd5Fa02e37E66257744) to see all transactions made with this address.<br>

Help concerning the CLI can be found running:
```bash
python ethereum_service.py --help
```

## Configuration

This projects uses python 3.6. <br>
Please run in your virtual environment:
   ```bash
        pip install -r requirements.txt
   ```

## How to use this service


Before running the service, you need to be connected to an Ethereum node. Please, [Install Geth](https://github.com/ethereum/go-ethereum/wiki/Building-Ethereum) <br>

<b>If you are on branch master : </b> <br>

The service is connected via web3py to the Rinkeby public testnet, which is PoA (Proof of Authority) based. <br>

Ubirch has its own Rinkeby testnet node running in stratoserver. If you wish to use this node, before running the service please use the following ssh tunnel :
        
        8545:localhost:8545
        
The keyfile of your account must be stored on the same machine that you run the service with.
You can create an account on the ETH Rinkeby testnet on https://www.myetherwallet.com/, and request fake ETH on https://faucet.rinkeby.io/.


1. Please install [Elasticmq](https://github.com/adamw/elasticmq) and/or [Kafka](https://kafka.apache.org/).
Please respect the following folder structure: <br>

        dependencies/
        ├── elasticMQServer
        │   ├── custom.conf
        │   └── elasticmq-server.jar
        └── kafka
            ├── bin
            │   ├── ...
            ├── config
            │   ├── ...
            ├── libs
            │   ├──...
            ├── LICENSE
            ├── NOTICE
            └── site-docs
                └── ...

And custom.conf should look like this:

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
        
            error_queue {
            defaultVisibilityTimeout = 10 seconds
            receiveMessageWait = 0 seconds
            deadLettersQueue {
                name = "error_queue-dead-letters"
                maxReceiveCount = 10 // from 1 to 1000
            }
          }
        
        }
        


2. Useful scripts are in *bin/* <br>
    a) In *bin/elasticMQ/*, to run the ElasticMQ server: <br>
      ```bash
      ./start-elasticMQ.sh
      ```
       
    b) In *bin/kafka/*, to run the Kafka server and create the topics, execute successively: <br>
     ```bash

        ./start_zookeeper.sh
        ./start-kafka.sh
        ./create-all-topics.sh
     
    ```      

        
3. Then, in a terminal, run successicely in *ubirch-ethereum-service/*, the scripts *sender.py* then *receiver.py*
and *receiver_errors.py*, with the flag **--server='SQS'** or **--server='KAFKA'**<br><br>

4. Finally, start the service.<br>

    ```bash
    python ethereum_service.py --server='SQS' -kf PATH_TO_KEYFILE -pwd KEYFILE_PASSWORD
    ```
    Or:

   ```bash
    python ethereum_service.py --server='KAFKA' -kf PATH_TO_KEYFILE -pwd KEYFILE_PASSWORD
   ```
    Where:
    - --server='SQS' to use elasticMQ's SQS queuing service
    - --server='KAFKA' to use Apache's Kafka messaging service.
    - -kf PATH_TO_KEYFILE specifies the location of your keyfile
    - -pwd KEYFILE_PASSWORD specifies the password to your keyfile
      

## Logs


Once the service is running, logs are recorded in *ethereum_service.log*

# License 

This project is publicized under the [Apache License 2.0](LICENSE).