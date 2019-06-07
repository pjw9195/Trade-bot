
from key import *
import pyupbit
access_key = ac_key
secret_key = se_key

def upbit():

    upbit = pyupbit.Upbit(access_key, secret_key)
    #내 돈
    print(upbit.get_balances())
    #코인 가격
    price = pyupbit.get_current_price("KRW-BTC")

    #거래
    print("BTC : ",price)
    ret = upbit.buy_limit_order("KRW-BTC", price+4000, 0.003)
