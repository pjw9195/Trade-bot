from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import re
from key import *
import pyupbit
import websocket
import time
import json
try:
    import thread
except ImportError:
    import _thread as thread
import time
access_key = ac_key
secret_key = se_key
upbit = pyupbit.Upbit(access_key, secret_key)
import nltk
from nltk.corpus import stopwords
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
                parse = re.sub('https?://\S+','',status.text)
                parse = re.sub('#\S+','',parse)
                if model.classify(status.text) > 0.7:
                    print(status.text, model.classify(parse))
                    buy()

                print(status.text, model.classify(parse))
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


def mybalnace():
    # 내 돈
    print(upbit.get_balances())
    # print((upbit.get_balances())[0][0]['currency'] +' : ' + (upbit.get_balances())[0][0]['balance'] )
def find():

    def on_message(ws, message):

        get_message = json.loads(message.decode('utf-8'))
        print(get_message)
        global msg_ask
        msg_ask = get_message['orderbook_units'][5]['ask_price']
        global msg_bid
        msg_bid = get_message['orderbook_units'][3]['bid_price']
        global msg_cur
        msg_cur = get_message['orderbook_units'][0]['bid_price']
        # 한번만받고 종료.
        ws.close()


    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("close")


    def on_open(ws):
        def run(*args):
            ws.send('[{"ticket":"test"},{"type":"orderbook","codes":["KRW-BTC"]}]')

            time.sleep(0.1)

        thread.start_new_thread(run, ())

    ws = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
                                  on_message = on_message,
                                  on_error = on_error,
                                  on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()

def buy():
    find()
    getbalance = upbit.get_balances()
    KRW = getbalance[0][0]['balance']
    num = (float(KRW)*0.9/float(msg_ask))
    ret = upbit.buy_limit_order("KRW-BTC", msg_ask, num );
    print(ret)
    cur = msg_cur
    while True:
        if cur*0.95 > msg_cur:
            sell()
            break
        elif cur*1.05 <msg_cur:
            sell()
            break
        time.sleep(2)


def sell():
    find()
    ret = upbit.sell_limit_order("KRW-BTC", msg_bid, (upbit.get_balances())[0][0]['balance']);
    print(ret)