import sf_client as sf


class Trader(object):
    def __init__(self, account, venue):
        self.gateway = sf.Gateway(account, venue)

    def buy_a_lot_using_market_price(self, symbol, quantity, target_price):
        remaining = quantity
        already_bought = 0
        buy_chunk = 100

        while remaining > 0:
            q = self.gateway.retrieve_quote(symbol)
            if q.bid is None:
                continue
            if target_price > q.bid:
                buy_offer = q.bid + 1
            else:
                buy_offer = q.bid -1
            quantity = buy_chunk if remaining > buy_chunk else remaining
            r = self.gateway.buy_limit(symbol, quantity, buy_offer)
            if r == 200:
                remaining = remaining - quantity
                already_bought = already_bought + quantity
                print "already bought %d" %already_bought


# import trader as t
# trader = t.Trader('BPB12585004', 'QMBEX')
# trader.buy_a_lot_using_market_price('MCC', 100000)