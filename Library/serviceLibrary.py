# coding: utf-8

import time
import json
import argparse

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


# storefunction should always return either False is the string is non-hex or {'txid': hash, 'hash': string}
def process_message(m, errorQueue, queue2, storefunction):
    t0 = time.time()
    storingResult = storefunction(m.body) #Anchoring of the message body
    print("anchoring time = " + str(time.time() - t0))
    if storingResult == False:
        json_error = json.dumps({"Not a hash": m.body})
        send(errorQueue, json_error)

    else:
        json_data = json.dumps(storingResult)
        send(queue2, json_data)

    m.delete()


def poll(queue1, errorQueue, queue2, storefunction):
    messages = queue1.receive_messages()  # Note: MaxNumberOfMessages default is 1.
    for m in messages:
        t0 = time.time()
        process_message(m, errorQueue, queue2, storefunction)
        print(" total processing time = " + str(time.time() - t0))


