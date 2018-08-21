# coding: utf-8

#Retrieves Json (message sent + txid) & error messages after anchoring into the IOTA Blockchain

import Library.ElasticMQ_Connection as EMQ
import Library.serviceLibrary as service

args = service.set_arguments("ethereum")
url = args.url
region = args.region
aws_secret_access_key = args.accesskey
aws_access_key_id = args.keyid

errorQueue = EMQ.getQueue('errorQueue', url, region, aws_secret_access_key, aws_access_key_id)

while True:
    errors = errorQueue.receive_messages()
    for e in errors:
        print(e.body)
        e.delete()

