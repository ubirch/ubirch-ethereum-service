# coding: utf-8

import time
import json
import argparse

# Anchors a hash from from queue1
# Sends the TxID + hash (json file) in queue2 and errors are sent in errorQueue

# Runs continuously (check if messages are available in queue1)


def set_arguments(servicetype):
    parser = argparse.ArgumentParser(description="Ubirch" + servicetype + "anchoring service")
    parser.add_argument('-u', '--url',
                        help="endpoint url of the sqs server, input localhost:9324 for local connection (default)",
                        metavar="URL", type=str, default="http://localhost:9324")
    parser.add_argument('-r', '--region', help="region name of sqs server, (default : 'elasticmq' for local)",
                        metavar="REGION", type=str, default="elasticmq")
    parser.add_argument('-ak', '--accesskey', help="AWS secret access key, input 'x'for local connection (default)",
                        metavar="SECRETACCESSKEY", type=str, default="x")
    parser.add_argument('-ki', '--keyid', help="AWS access key id, input 'x' for local connection (default)",
                        metavar="KEYID", type=str, default="x")
    return parser.parse_args()


def send(queue, msg):
    return queue.send_message(
        MessageBody=msg
    )


def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def poll(queue1, errorQueue, queue2, storefunction):
    start = time.time()
    messages = queue1.receive_messages()  # Note: MaxNumberOfMessages default is 1.
    start2 = time.time()
    print("receiving time : " + str(start2 - start))
    for m in messages:
        start3 = time.time()
        process_message(m, errorQueue, queue2, storefunction)
        print("processing time = " + str(time.time() - start3))


def process_message(m, errorQueue, queue2, storefunction):
    a = time.time()
    storing = storefunction(m.body)
    print("storing = " + str(time.time() - a))
    if storing == False:
        json_error = json.dumps({"Not a hash" : m.body})
        b = time.time()
        send(errorQueue, json_error)
        print("sending error = " + str(time.time() - b))

    else:
        transactionHashes = storing
        for txid in transactionHashes:  # In case of the anchoring results in several transactions
            json_data = json.dumps({"tx" : str(txid), "hash" : m.body})
            c = time.time()
            send(queue2, json_data)
            print("sending message= " + str(time.time() - c))

    m.delete()



