# ubirch-ethereum-service
This is a command line interface python service developed to anchor data on the Ethereum Blockchain.<br>

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

<b>a. If you are on branch master: </b> <br>

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
   
<b> b. If you want to set up your own node : </b> <br>
Please visit : https://www.rinkeby.io/#geth and download rinkeby.json <br>


To initialize, execute:

    geth --datadir=YOUR_DATA_DIR init PATH_TO_rinkeby.json

Then, execute:

    geth --rinkeby --datadir YOUR_DATA_DIR --fast --rpc --rpcapi db,eth,net,web3,personal --cache=1024  --rpcport 8545 --rpcaddr 0.0.0.0 --rpccorsdomain "*" --bootnodes=enode://a24ac7c5484ef4ed0c5eb2d36620ba4e4aa13b8c84684e1b4aab0cebea2ae45cb4d375b77eab56516d34bfbd3c1a833fc51296ff084b770b94fb9028c4d25ccf@52.169.42.101:30303

To use the geth console, open another terminal and execute :

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
Once the node is up and running and you have access ( = keyfile on your machine and known password)
to an address with Rinkeby ETH on it, you can start the service.

## Logs


Once the service is running, logs are recorded in *ethereum_service.log*

# License 

This project is publicized under the [Apache License 2.0](LICENSE).