import json
import boto3
from botocore.exceptions import ClientError


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
    table = dynamodb.Table('CodingTips')

    table.put_item(
        Item=item_obj
    )


def retrieve_sqs_messages(sqs_queue_url, num_msgs=1, wait_time=0, visibility_time=5, region_name='us-east-2'):
    if num_msgs < 1:
        num_msgs = 1
    elif num_msgs > 10:
        num_msgs = 10

    sqs_client = boto3.client('sqs', region_name=region_name)
    try:
        msgs = sqs_client.receive_message(QueueUrl=sqs_queue_url,
                                          MaxNumberOfMessages=num_msgs,
                                          WaitTimeSeconds=wait_time,
                                          VisibilityTimeout=visibility_time)
    except ClientError as e:
        print(e)
        return None

    return msgs['Messages']


def delete_sqs_message(sqs_queue_url, msg_receipt_handle, region_name='us-east-2'):
    sqs_client = boto3.client('sqs', region_name=region_name)
    sqs_client.delete_message(QueueUrl=sqs_queue_url,
                              ReceiptHandle=msg_receipt_handle)


def lambda_handler(event, context):
    obj = dict()
    sqs_queue_url = 'https://sqs.us-east-2.amazonaws.com/982798321347/tweetsQueue'

    for i in range(1, 6):
        msg_body = f'SQS message #{i}'
        msg = send_sqs_message(sqs_queue_url, msg_body)
        obj[i] = msg_body

    data = retrieve_sqs_messages(sqs_queue_url, num_msgs=3)
    if data is not None:
        for msg in data:
            item_obj = {"tweetID": "",
                        "tweetBody": msg.get('Body')
                        }
            data = put_items_to_db()
            delete_sqs_message(sqs_queue_url, msg['ReceiptHandle'])

    return {
        'statusCode': 200,
        'body': json.dumps("Successfully data managed")
    }
