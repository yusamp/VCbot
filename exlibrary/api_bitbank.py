# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import requests
import time
from urllib.parse import urlencode

public_method_list = ('ticker', 'depth', 'transactions', 'candlestick')

trade_method_list = ('/user/assets', '/user/spot/order?',
                     '/user/spot/active_orders?', '/user/spot/order',
                     '/user/spot/cancel_order', '/user/spot/cancel_orders',
                     '/user/spot/orders_info', '/user/spot/trade_history?',
                     '/user/withdrawal_account?', '/user/request_withdrawal')


class Bitbank(object):
    def __init__(self, api_key=None, api_secret=None):
        self.__api_key = str(api_key) if api_key is not None else ''
        self.__api_secret = str(api_secret) if api_secret is not None else ''
        self.__public_url = 'https://public.bitbank.cc'
        self.__public_set = set(public_method_list)
        self.__private_url = 'https://api.bitbank.cc/v1'
        self.__trade_set = set(trade_method_list)
        self.__session = requests.Session()
        self.__nonce = time.time()

    def __api_query(self, method, options=None, req_type=None):
        if not options:
            options = {}

        if method in self.__public_set:
            request_url = self.__public_url + options
            response = self.__session.get(request_url, timeout=5)
            return response.json()

        elif method in self.__trade_set:

            self.__nonce = str(int(time.time() * 1000))

            if req_type == 'GET':
                data = '/v1' + method + urlencode(options)
                query = str(self.__nonce) + data
                h = hmac.new(bytearray(self.__api_secret, 'utf8'),
                             bytearray(query, 'utf8'), hashlib.sha256)
                headers = {'Content-Type': 'application/json',
                           'ACCESS-KEY': self.__api_key,
                           'ACCESS-NONCE': str(self.__nonce),
                           'ACCESS-SIGNATURE': h.hexdigest()
                           }
                trade_url = self.__private_url + method + urlencode(options)
                response = requests.get(trade_url, headers=headers, timeout=60)
                return response.json()

            elif req_type == 'POST':

                data = json.dumps(options)
                query = str(self.__nonce) + data
                h = hmac.new(bytearray(self.__api_secret, 'utf8'),
                             bytearray(query, 'utf8'), hashlib.sha256)
                headers = {'Content-Type': 'application/json',
                           'ACCESS-KEY': self.__api_key,
                           'ACCESS-NONCE': str(self.__nonce),
                           'ACCESS-SIGNATURE': h.hexdigest()
                           }
                trade_url = self.__private_url + method
                response = requests.post(trade_url,
                                         data=data,
                                         headers=headers,
                                         timeout=60)
                return response.json()

    # PublicAPI
    def ticker(self, pair):
        path = '/' + pair + '/ticker'
        return self.__api_query('ticker', path)

    def depth(self, pair):
        path = '/' + pair + '/depth'
        return self.__api_query('depth', path)

    def transactions(self, pair, yyyymmdd=None):
        path = '/' + pair + '/transactions'
        if yyyymmdd:
            path += '/' + yyyymmdd
        return self.__api_query('transactions', path)

    def candlestick(self, pair, candle_type, yyyymmdd):
        path = '/' + pair + '/candlestick/' + candle_type + '/' + yyyymmdd
        return self.__api_query('candlestick', path)

    # TradeAPI
    def asset(self):
        return self.__api_query('/user/assets', {}, 'GET')

    def get_order(self, pair, order_id):
        query = {'pair': pair, 'order_id': order_id}
        return self.__api_query('/user/spot/order?', query, 'GET')

    def active_orders(self, pair, options=None):
        if options is None:
            options = {}
        if 'pair' not in options:
            options['pair'] = pair
        return self.__api_query('/user/spot/active_orders?', options, 'GET')

    def order(self, pair, price, amount, side, order_type):
        query = {'pair': pair, 'price': price,
                 'amount': amount, 'side': side, 'type': order_type}
        return self.__api_query('/user/spot/order', query, 'POST')

    def cancel_order(self, pair, order_id):
        query = {'pair': pair, 'order_id': order_id}
        return self.__api_query('/user/spot/cancel_order', query, 'POST')

    def cancel_orders(self, pair, order_ids):
        query = {'pair': pair, 'order_ids': order_ids}
        return self.__api_query('/user/spot/cancel_orders', query, 'POST')

    def get_orders_info(self, pair, order_ids):
        query = {'pair': pair, 'order_ids': order_ids}
        return self.__api_query('/user/spot/orders_info', query, 'POST')

    def get_trade_history(self, pair, order_count, **options):
        query = {'pair': pair, 'count': order_count}
        if not options == {}:
            query.update(options)
        return self.__api_query('/user/spot/trade_history?', query, 'GET')

    def get_withdraw_account(self, asset):
        query = {'asset': asset}
        return self.__api_query('/user/withdrawal_account?', query, 'GET')

    def request_withdraw(self, asset, uuid, amount, token):
        query = {'asset': asset, 'uuid': uuid,
                 'amount': amount, 'otp_token': token}
        return self.__api_query('/user/request_withdrawal', query, 'POST')

    # real_time
    def pubnub_ticker(self):
        pass

    def pubnub_depth(self):
        pass

    def pubnub_open_trade_history(self):
        pass

    def pubnub_candle_stick(self):
        pass
