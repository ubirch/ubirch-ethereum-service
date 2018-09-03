# coding: utf-8

import Library.serviceLibrary as service

#Retrieves Json (message sent & txid) document

args = service.set_arguments("ethereum")
url = args.url
region = args.region
aws_secret_access_key = args.accesskey
aws_access_key_id = args.keyid

queue2 = service.getQueue('queue2', url, region, aws_secret_access_key, aws_access_key_id)

while True:
    response = queue2.receive_messages()
    for r in response:
        print(r.body)
        r.delete()



