# Twiter Tweet Analytics

## Introduction
"Build a system that lets you browse and query Twitter tweets.

The incoming tweets from Twitter real time API must be consumed pushed to SQS. SQS Queue must be consumed and tweets must be put into DynamoDB.
The interface to the system must be a RESTful API that contains both private and public end-points.
The origin country of every tweet must be published to CloudWatch.

## Technologies 
- Python 3.6
- AWS Lamda  
- AWS API GATEWAY
- CloudWatch
- AWS SQS
- DyanamoDB


## Installation
1. Clone the git repository
2. Go to the repository and upload zip file to the lamda function


You can Deploy in local server:
```bash
git clone https://github.com/sujonict07/twitterTweet.git
cd twitterTweet/
# if pipenv is not installed
#    pip install pipenv
pipenv --three
pipenv install
pipenv shell
```

## Runing Procedure
- API Gateway configuration
- SQS Configuration
- Configuration of lamda function


## Testing
```Comming Soon```
