from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from trade import *
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
                if model.classify(status.text) > 0.7:
                    buy()
                    print(status.text)
                    def swi(swi):
                        swi =0
                        return swi

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


