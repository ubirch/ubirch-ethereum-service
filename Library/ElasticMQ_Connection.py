# TO START THE SERVER
#  See custom.conf for more details
# execute : java -Dconfig.file=custom.conf -jar elasticmq-server-0.14.2.jar

import boto3

def connect(url, region, aws_secret_access_key, aws_access_key_id):
    client = boto3.resource('sqs',
                          endpoint_url=url,  #
                          region_name=region,  #
                          aws_secret_access_key=aws_secret_access_key,  # parameters passed as arguments
                          aws_access_key_id=aws_access_key_id,  #
                          use_ssl=False)
    return client


def getQueue(queue_name, url, region, aws_secret_access_key, aws_access_key_id):
    client = connect(url, region, aws_secret_access_key, aws_access_key_id)
    queue = client.get_queue_by_name(QueueName=queue_name)
    print("The url of " + queue_name + " is : " + queue.url)
    return queue
