import pickle
import pandas as pd
import zipline
import matplotlib.pyplot as plot
import numpy as np

f = open("result.pkl", "rb")
df = pickle.load(f)
#total_value = df['ending_cash'] + df['ending_value']
#plot.plot(total_value)

plot.plot(df['benchmark_period_return'])
plot.plot(df['algorithm_period_return'])
plot.show()

plot.plot(df['benchmark_volatility'])
plot.plot(df['algo_volatility'])
plot.show()

algo_return = df['algorithm_period_return'].tail(1).reset_index(drop=True).at[0]
benchmark_return = df['benchmark_period_return'].tail(1).reset_index(drop=True).at[0]

beta = df['beta'].tail(1).reset_index(drop=True).at[0]
alpha = df['alpha'].tail(1).reset_index(drop=True).at[0]
print(f'The algorithm return over this period is  {algo_return}')
print(f'The benchmark return over this period is  {benchmark_return}')
print(f'Beta calculated by zipline is {beta}')
print(f'Alpha calculated by zipline is {alpha}')