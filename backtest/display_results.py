import pickle
import pandas as pd
import zipline
import matplotlib.pyplot as plot
import numpy as np

f = open("result.pkl", "rb")
df = pickle.load(f)
total_value = df['ending_cash'] + df['ending_value']
plot.plot(total_value)
plot.show()

beta = df['beta'].tail(1).reset_index(drop=True).at[0]
alpha = df['alpha'].tail(1).reset_index(drop=True).at[0]
print(f'Beta calculated by zipline is {beta}')
print(f'Alpha calculated by zipline is {alpha}')