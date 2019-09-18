import boto3
from botocore.exceptions import ClientError


def send_sqs_message(sqs_queue_url, msg_body, region_name='us-east-2'):
    print("send sms to sqs")
    sqs_client = boto3.client('sqs', region_name=region_name)
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=msg_body)
    except ClientError as e:
        return None
    return msg


def manage_sqs(msg_body):
    print("manage_sqs body function")
    sqs_queue_url = 'https://sqs.us-east-2.amazonaws.com/982798321347/tweetsQueue'
    msg = send_sqs_message(sqs_queue_url, msg_body)
    if msg is not None:
        print(f'Sent SQS message ID: {msg["MessageId"]}')