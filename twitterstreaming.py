from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
from train import model
from key import *

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True


class listener(StreamListener):

    def on_status(self, status):
        if from_creator(status):
            try:
                # Prints out the tweet
                print(status.text, model.classify(status.text))
                time.sleep(2)
                return True
            except BaseException as e:
                print("Error on_data %s" % str(e))
            return True
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, listener())


