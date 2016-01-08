import requests
import json

security_header = {'X-Starfighter-Authorization':'f7303e2b760c835bcf2dddfd1e7aa426a4ab17fa'}


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
        if r.status_code == 200:
            return json.loads(r.content).get('id')
        else:
            return None

    def retrieve_status(self, symbol, order):
        url = 'https://api.stockfighter.io/ob/api/venues/' + self.venue + '/stocks/' + symbol + '/orders/' + order
        r = requests.get(url, headers = security_header)

class Quote:
    def __init__(self, symbol, bid, ask):
        self.symbol = symbol
        self.bid = bid
        self.ask = ask


#import sf_client as sf
#g = sf.Gateway('BAI24378394', 'OJPEX')
#g.buy_limit('WBM', 1, 98)