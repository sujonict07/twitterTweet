import tweepy
from tweepy import Stream, StreamListener
from twitter_credenticals import (
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
from send_message_to_sqs import manage_sqs

def tweet_connect():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_status(self, status):
        if status.retweeted:
            return
        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        # print("--", text, description, loc)
        print(type(id_str))
        #manage_sqs(text)


        with open('service_status.txt', 'r') as f:
            current_status = f.read()
        if current_status == "stop":
            return False
        return False

    def on_error(self, status):
        print(status)


def start_streaming(keyword):
    l = StdOutListener()
    stream = Stream(tweet_connect(), l)
    stream.filter(track=[keyword])