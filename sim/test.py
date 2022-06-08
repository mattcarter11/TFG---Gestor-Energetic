import pandas as pd
from time import time_ns

repeat = 5

df = pd.read_csv('./db/2022-04-22..2022-05-27 Jordi.csv', parse_dates=['timestamp'])
t0 = time_ns()
for _ in range(repeat):
    print(df.isna().any())
print((time_ns() - t0)/repeat)

t0 = time_ns()
for _ in range(repeat):
    print(df.isna().values.any())
print((time_ns() - t0)/repeat)