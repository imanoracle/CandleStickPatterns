import pandas as pd
import talib

# Load the data from the file
df = pd.read_csv('btcDaily.csv')

# Extract OHLC
op = df['Open']
hi = df['High']
lo = df['Low']
cl = df['Close']

# Get candlestick patterns
candle_names = talib.get_function_groups()['Pattern Recognition']

# Create columns for each pattern
for candle in candle_names:
    df[candle] = getattr(talib, candle)(op, hi, lo, cl)

print(df.head())
df.to_csv('btcDailyCandlePatterns.csv', index=False)