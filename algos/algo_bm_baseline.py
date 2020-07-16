
from zipline.data import bundles
from zipline.api import order, symbol, record, set_benchmark
import pypfopt
from pypfopt import black_litterman, risk_models
from pypfopt import BlackLittermanModel, plotting
from pypfopt import EfficientFrontier, objective_functions
from pypfopt import DiscreteAllocation
import sys

# parameters
selected_stock = 'FB'
n_stocks_to_buy = 10

def initialize(context):
    context.tickers = ["MSFT", "AMZN", "FB", "GOOG", "AAPL", "NFLX", "BTC-USD"]
    context.assets = [symbol(ticker) for ticker in context.tickers]
    context.balance_days = 0  
    context.bar_count = 365


def handle_data(context, data):
    if context.balance_days == 0:
        # Rebalancing

        # Risk Aversion
        market_prices = data.history(symbol("SPY"), 'open', bar_count=context.bar_count, frequency="1d")
        delta = black_litterman.market_implied_risk_aversion(market_prices)

        # Covariance
        prices = data.history(context.assets, 'open', bar_count=context.bar_count, frequency="1d")
        rename = {}
        for original, new in zip(prices.columns, context.tickers):
            rename[original] = new
        prices = prices.rename(columns=rename).dropna()
        covariance_matrix = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
        
        # Allocations Need to figure this out!
        allocations = {
                        'MSFT': 1624372805632,
                        'AMZN': 1556016529408,
                        'FB': 694724526080,
                        'GOOG': 1038930018304,
                        'AAPL': 1665986330624,
                        'NFLX': 222342905856,
                        'BTC-USD': 170074475723}
        
        # Market prior
        market_prior = black_litterman.market_implied_prior_returns(allocations, delta, covariance_matrix, risk_free_rate=0.0)

        # Black litterman model with empty views
        viewdict = {}
        confidences = []
        bl = BlackLittermanModel(covariance_matrix, pi=market_prior, absolute_views=viewdict, omega="idzorek", view_confidences=confidences)
        ret_bl = bl.bl_returns()
        
        # Determine allocation
        ef = EfficientFrontier(ret_bl, covariance_matrix)
        ef.add_objective(objective_functions.L2_reg)
        ef.max_sharpe()
        weights = ef.clean_weights()
        
        da = DiscreteAllocation(weights, prices.iloc[-1], total_portfolio_value=context.portfolio.portfolio_value)
        alloc, leftover = da.lp_portfolio()

        # Make order
        cpp = context.portfolio.positions
        cpp_symbols = map(lambda x: x.symbol, cpp) 
        for symbolz in cpp_symbols:
            alloc[symbolz] -= cpp[symbol(symbolz)]['amount']
        for symbolz, amount in alloc.items():
            order(symbol(symbolz), amount)

        context.balance_days = 20 # Balance once every 20 days

        # Printing zone
        # print(covariance_matrix)
        #print(alloc)
        # print(weights)


    else:
        context.balance_days -= 1

    context.bar_count += 1 # Increase window size by 1
    


  