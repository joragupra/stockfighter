import requests
import json

api_key = 'f7303e2b760c835bcf2dddfd1e7aa426a4ab17fa'


class Gateway(object):
    def __init__(self, account, venue):
        self.account = account
        self.venue = venue
        self.security_header = {'X-Starfighter-Authorization':api_key}

    def __get(self, url):
        return requests.get(url, headers=self.security_header)

    def retrieve_quote(self, stock_symbol):
        url = 'https://api.stockfighter.io/ob/api/venues/' + self.venue + '/stocks/' + stock_symbol + '/quote'
        r = self.__get(url)
        if r.status_code == 200:
            return r.content
        return None

    def buy_limit(self, symbol, quantity, price):
        url = 'https://api.stockfighter.io/ob/api/venues/' + self.venue + '/stocks/' + symbol + '/orders'

        data = {'account': self.account, 'venue': self.venue, 'stock': symbol, 'qty': quantity, 'price': price,
                'direction': 'buy', 'orderType': 'limit'}

        r = requests.post(url, headers=self.security_header, data=json.dumps(data))
        if r.status_code == 200:
            return json.loads(r.content).get('id')
        else:
            return None

    def check_if_completed(self, symbol, order):
        url = 'https://api.stockfighter.io/ob/api/venues/' + self.venue + '/stocks/' + symbol + '/orders/' + `order`
        r = self.__get(url)
        if r.status_code == 200:
            return not json.loads(r.content).get('open')

    def retrieve_orderbook(self, symbol):
        offers = []
        req = []
        url = 'https://api.stockfighter.io/ob/api/venues/' + self.venue + '/stocks/' + symbol
        r = self.__get(url)
        if r.status_code == 200:
            bids = json.loads(r.content).get('bids')
            if not bids:
                return None
            for bid in bids:
                offer = Offer(symbol, bid['price'], bid['qty'])
                offers.append(offer)
            asks = json.loads(r.content).get('asks')
            if not asks:
                return None
            for ask in asks:
                request = Request(symbol, ask['price'], ask['qty'])
                req.append(request)
            return OrderBook(symbol, offers, req)
        return None


class Offer:
    def __init__(self, symbol, price, quantity):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity


class Request:
    def __init__(self, symbol, price, quantity):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity


class OrderBook:
    def __init__(self, symbol, offers, requests):
        self.symbol = symbol
        self.offers = offers
        self.requests = requests

    @staticmethod
    def __return__first_if_exists(l):
        if not l:
            return None
        return l[0]

    def best_offer(self):
        return self.__return__first_if_exists(self.offers)

    def best_request(self):
        return self.__return__first_if_exists(self.requests)

