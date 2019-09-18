import json
import boto3
from botocore.exceptions import ClientError
from tweetsController import start_streaming
from utils import random_string

def send_sqs_message(sqs_queue_url, msg_body):
    sqs_client = boto3.client('sqs', region_name='us-east-2')
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=msg_body)
    except ClientError as e:
        return None
    return msg


def put_items_to_db(item_obj={}):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Tweets')

    table.put_item(
        Item=item_obj
    )


def retrieve_sqs_messages(sqs_queue_url, num_msgs=1, wait_time=0, visibility_time=5, region_name='us-east-2'):
    # Validate number of messages to retrieve
    if num_msgs < 1:
        num_msgs = 1
    elif num_msgs > 10:
        num_msgs = 10

    # Retrieve messages from an SQS queue
    sqs_client = boto3.client('sqs', region_name=region_name)
    try:
        msgs = sqs_client.receive_message(QueueUrl=sqs_queue_url,
                                          MaxNumberOfMessages=num_msgs,
                                          WaitTimeSeconds=wait_time,
                                          VisibilityTimeout=visibility_time)
    except ClientError as e:
        print(e)
        return None

    # Return the list of retrieved messages
    return msgs['Messages']


def delete_sqs_message(sqs_queue_url, msg_receipt_handle, region_name='us-east-2'):
    sqs_client = boto3.client('sqs', region_name=region_name)
    sqs_client.delete_message(QueueUrl=sqs_queue_url,
                              ReceiptHandle=msg_receipt_handle)


def others():
    #obj = dict()
    sqs_queue_url = 'https://sqs.us-east-2.amazonaws.com/982798321347/tweetsQueue'

    # for i in range(1, 6):
    #     msg_body = f'SQS message #{i}'
    #     msg = send_sqs_message(sqs_queue_url, msg_body)
    #     obj[i] = msg_body

    data = retrieve_sqs_messages(sqs_queue_url, num_msgs=3)
    if data is not None:
        for msg in data:
            item_obj = {"tweetID": random_string(),
                        "tweetBody": msg.get('Body')
                        }
            data = put_items_to_db(item_obj)
            delete_sqs_message(sqs_queue_url, msg['ReceiptHandle'])

    # data = put_items_to_db()


def lambda_handler(event, context):
    query_string = event["keyword"]
    #start_streaming(query_string)
    others()

    return {
        'statusCode': 200,
        'body': json.dumps(query_string)
    }


if __name__ == "__main__":
    event = dict()
    event["keyword"] = "cricket"
    context = ""
    lambda_handler(event,context)