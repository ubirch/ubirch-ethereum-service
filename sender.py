# coding: utf-8
import Library.ElasticMQ_Connection as EMQ
import Library.serviceLibrary as service
import time
import hashlib

# Sends messages (HASH (hex) into queue1
# Dev purposes


args = service.set_arguments("ethereum")
url = args.url
region = args.region
aws_secret_access_key = args.accesskey
aws_access_key_id = args.keyid

queue1 = EMQ.getQueue('queue1', url, region, aws_secret_access_key, aws_access_key_id)

i = 0.5
j = 0.5
while True:
    t = str(time.time()).encode('utf-8')
    message = hashlib.sha256(t).hexdigest()
    if '0' in message[0:8]:                 # Error propagation in queue1
        service.send(queue1, "error %s" %i)
        print("error %s sent" %i)
        i += 1

    else:                                   # Sends in queue1 the sha256 hash of the time()
        service.send(queue1, message)
        print("message %s sent" % j)
        j += 1
