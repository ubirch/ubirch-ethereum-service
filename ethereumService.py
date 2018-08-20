# coding: utf-8

import json
import sys
import random
import argparse
import time  # for testing

sys.path.insert(0, 'Library')
import ElasticMQ_Connection as EMQ

parser = argparse.ArgumentParser(description='Ubirch iota anchoring service')

parser.add_argument('-u', '--url',
                    help="endpoint url of the sqs server, input localhost:9324 for local connection (default)",
                    metavar="URL", type=str, default="http://localhost:9324")
parser.add_argument('-r', '--region', help="region name of sqs server, (default : 'elasticmq' for local)",
                    metavar="REGION", type=str, default="elasticmq")
parser.add_argument('-ak', '--accesskey', help="AWS secret access key, input 'x'for local connection (default)",
                    metavar="SECRETACCESSKEY", type=str, default="x")
parser.add_argument('-ki', '--keyid', help="AWS access key id, input 'x' for local connection (default)",
                    metavar="KEYID", type=str, default="x")

args = parser.parse_args()

url = args.url
region = args.region
aws_secret_access_key = args.accesskey
aws_access_key_id = args.keyid

queue1 = EMQ.getQueue('queue1', url, region, aws_secret_access_key, aws_access_key_id)
queue2 = EMQ.getQueue('queue2', url, region, aws_secret_access_key, aws_access_key_id)
errorQueue = EMQ.getQueue('errorQueue', url, region, aws_secret_access_key, aws_access_key_id)

