# ubirch-ethereum-service
An Ethereum based anchoring service.
This service uses Apache Kafka for messaging.

# Configuration
This projects uses Python 3. <br>
Please, run in your virtual environment:

        pip3 install -r requirements.txt

1. Set up the [Kafka]((https://kafka.apache.org/)) server. Useful bash scripts are in bin/ ( ./start-zookeeper.sh, ./start-kafka.sh and./create-all-topics.sh).<br> Three topics should be created : queue1, queue2 and errorQueue. <br>


2. [Install Geth](https://github.com/ethereum/go-ethereum/wiki/Building-Ethereum)

3. Once the server is running, start sender.py which will send via an infinite loop messages to the first queue (queue1). Those messages will mainly be hex strings (hashes) but there will be also be non hex-strings which will be processed as errors by the service.

4. Before running the service, you need to be connected to an Ethereum node.

<b>  a. If you are on branch master : </b> <br>

The service is connected via web3py to the Rinkeby public testnet, which is PoA (Proof of Authority) based. <br>

Ubirch has now its own Rinkeby testnet node running in stratoserver. If you wish to use this node, before running the service please use the following ssh tunnel :
        
        8545:localhost:8545
        
The keyfile of your account must be stored on the same machine that you run the service with.
You can create an account on the ETH Rinkeby testnet on https://www.myetherwallet.com/, and request fake ETH on https://faucet.rinkeby.io/.

<b> If you want to set up your own node : </b> <br>
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
Once the node is up and running and you have access ( = keyfile on your machine and known password) to an address with Rinkeby ETH on it, you can start the service.

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


    python ethereumService.py --keyfile=PATHTOKEYFILE --pwd=PASSWORD
    

If you need some additional documentation, please run :

    python ethereumService.py -h

7. Run the two scripts receiver.py and receiver_errors.py which will read the messages sent into the two queues.
