
from zipline.data import bundles
from zipline.api import order, symbol, record, set_benchmark
import sys

# parameters
selected_stock = 'FB'
n_stocks_to_buy = 10

def initialize(context):
    tickers = ["SPY", "MSFT", "AMZN", "FB", "GOOG", "AAPL", "NFLX"]
    context.assets = [symbol(ticker) for ticker in tickers]
    context.has_ordered = False  

def handle_data(context, data):
    # record price for further inspection
    record(price=data.current(symbol(selected_stock), 'price'))

    # trading logic
    if not context.has_ordered:
        # placing order, negative number for sale/short
        order(symbol(selected_stock), n_stocks_to_buy)
        # setting up a flag for holding a position
        context.has_ordered = True
    else:
        print(context.portfolio.positions[symbol('FB')]['amount'])
        cpp = context.portfolio.positions
        cpp_symbols = list(map(lambda x: symbol(x.symbol), cpp))
        print(cpp_symbols[0])
        print(context.portfolio.positions[cpp_symbols[0]]['amount'])
        sys.exit()