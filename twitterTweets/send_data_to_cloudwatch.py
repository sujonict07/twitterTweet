import boto3
import random


def send_data_to_cloud_watch(country, text, id_str):
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-2')
    print("send_data_to_cloud_watch-  {} -  {} - {}".format(country, text, id_str))
    if country is None:
        country = "None"
    if text is None:
        text = "None"
    if id_str is None:
        id_str = "None"
    try:
        response = cloudwatch.put_metric_data(
            MetricData=[
                {
                    'MetricName': 'TweetWatch',
                    'Dimensions': [
                        {
                            'Name': 'TEXT',
                            'Value': str(text)
                        },
                        {
                            'Name': 'tweetID',
                            'Value': str(id_str)
                        },
                        {
                            'Name': 'TweetLocation',
                            'Value': str(country)
                        },
                        {
                            'Name': 'APP_VERSION',
                            'Value': '1.0'
                        },
                    ],
                    'Unit': 'None',
                    'Value': random.randint(1, 500)
                },
            ],
            Namespace='Tweet/Watch'
        )
    except Exception:
        return "Something want wrong"
    return response


def get_matrix():
    # Create CloudWatch client
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-2')

    # List metrics through the pagination interface
    paginator = cloudwatch.get_paginator('list_metrics')
    for response in paginator.paginate(Dimensions=[{'Name': 'APP_VERSION'}],
                                       MetricName='TweetWatch',
                                       Namespace='Tweet/Watch'):
        print(response['Metrics'])


def cloud_watch(country_location, text, tweetID):
    print(send_data_to_cloud_watch(country_location, text, tweetID))
    get_matrix()


# if __name__ == "__main__":
#     country = "Dhaka"
#     text = "hello world"
#     str = "123123"
#     cloud_watch(country, text, str)
