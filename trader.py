import sf_client as sf
import json


class Trader(object):
    def __init__(self, account, venue):
        self.gateway = sf.Gateway(account, venue)
        self.orders = {}

    def quote(self, symbol):
        data = self.gateway.retrieve_quote(symbol)

        if data is None:
            return None

        q = json.loads(data)
        return Quote(q.get('symbol'), q.get('bid'), q.get('ask'))

    def buy_a_lot_using_market_price(self, symbol, quantity, target_price):
        remaining = quantity
        already_bought = 0
        buy_chunk = 100

        buy_offer = -1
        while buy_offer == -1:
            q = self.gateway.retrieve_quote(symbol)
            if q.bid is None:
                continue
            if target_price > q.bid:
                buy_offer = q.bid + 1
            else:
                buy_offer = q.bid - 1

        while remaining > 0:
            quantity = buy_chunk if remaining > buy_chunk else remaining
            r = self.gateway.buy_limit(symbol, quantity, buy_offer)
            if r is not None:
                remaining = remaining - quantity
                already_bought = already_bought + quantity
                print "placed order for %d" %already_bought

    def place_order(self, symbol, quantity, bid):
        order_id = self.gateway.buy_limit(symbol, quantity, bid)
        if order_id is not None:
            self.orders[order_id] = PendingOrder(order_id, symbol)

    def check_order(self, symbol, order_id):
        completed = self.gateway.check_if_completed(symbol, order_id)
        print "completed"
        print completed
        if not completed:
            order = self.orders[order_id]
            order.times_checked += 1
            self.orders[order_id] = order


class Quote(object):
    def __init__(self, symbol, bid, ask):
        self.symbol = symbol
        self.bid = bid
        self.ask = ask

    def is_complete(self):
        return self.symbol is not None and self.bid is not None and self.ask is not None


class PendingOrder(object):
    def __init__(self, order_id, symbol):
        self.order_id = order_id
        self.symbol = symbol
        self.times_checked = 0
