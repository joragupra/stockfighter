import requests
import json

security_header = {'X-Starfighter-Authorization':'cbcd4ff88d9d6973a0dec57aba357bcefdf71ef8'}


class Gateway(object):
    def __init__(self, account, venue):
        self.account = account
        self.venue = venue

    def retrieve_quote(self, stock_symbol):
        url = 'https://api.stockfighter.io/ob/api/venues/' + self.venue + '/stocks/' + stock_symbol + '/quote'
        r = requests.get(url, headers = security_header)
        if r.status_code == 200:
            response = r.content
            symbol = json.loads(response).get('symbol')
            bid = json.loads(response).get('bid')
            ask = json.loads(response).get('ask')
            return Quote(symbol, bid, ask)
        return ''

    def buy_limit(self, symbol, quantity, price):
        url = 'https://api.stockfighter.io/ob/api/venues/' + self.venue + '/stocks/' + symbol + '/orders'

        data = {}
        data['account'] = self.account
        data['venue'] = self.venue
        data['stock'] = symbol
        data['qty'] = quantity
        data['price'] = price
        data['direction'] = 'buy'
        data['orderType'] = 'limit'

        r = requests.post(url, headers = security_header, data = json.dumps(data))

        return r.status_code

class Quote:
    def __init__(self, symbol, bid, ask):
        self.symbol = symbol
        self.bid = bid
        self.ask = ask