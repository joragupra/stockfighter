import websocket
import json

class StockMonitor(object):
    def __init__(self, trading_account, venue, stock_symbol, ask_prices=[]):
        self.ask_prices = ask_prices
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp('wss://api.stockfighter.io/ob/api/ws/' + trading_account + '/venues/' + venue + '/tickertape',
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
        ws.run_forever()

    def on_message(self, ws, message):
        print message
        quote = json.loads(message).get('quote')
        if quote and quote['ask']:
            self.ask_prices.append(quote['ask'])
            print 'new ask price %d' %quote['ask']

    def on_error(self, ws, error):
        print error

    def on_close(self, ws):
        print "### closed ###"

