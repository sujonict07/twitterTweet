import tweepy
from tweepy import Stream, StreamListener
from twitter_credenticals import (
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
from send_message_to_sqs import manage_sqs
from send_data_to_cloudwatch import cloud_watch


def tweet_connect():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_status(self, status):
        print("I am coming from ---on_status---")
        if status.retweeted:
            return
        loc = status.user.location
        text = status.text
        id_str = status.id_str
        msg = "ID:{}:body:{}".format(id_str, text)
        manage_sqs(msg)
        cloud_watch(loc, text, id_str)

        with open('service_status.txt', 'r') as f:
            current_status = f.read()
        if current_status == "stop":
            return False
        return False

    def on_error(self, status):
        print(status)


def start_streaming(keyword):
    print("I am coming from ---start_streaming--- {}".format(keyword))
    stream_instance = StdOutListener()
    stream = Stream(tweet_connect(), stream_instance)
    stream.filter(track=[keyword])
