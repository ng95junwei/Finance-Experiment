
from zipline.data import bundles
from zipline.api import order, symbol, record, set_benchmark

# parameters
selected_stock = 'ABN'
n_stocks_to_buy = 10

def initialize(context):
    context.asset = symbol('ABN')
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