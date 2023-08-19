import pandas as pd

# Load the data from the provided CSV file
data = pd.read_csv('btcDailyCandleMatch.csv')


# Calculate whether the next day is positive or negative
data['next_day_positive'] = (data['Close'].shift(-1) > data['Open'].shift(-1)).astype(int)

# For each candlestick pattern, compute:
# - total appearances
# - number of positive next days
# - ratio of positive next days to total appearances
pattern_stats = data.groupby('candlestick_pattern').agg(
    total_appearances=('candlestick_pattern', 'size'),
    positive_next_days=('next_day_positive', 'sum')
)

# Compute the ratio
pattern_stats['positive_ratio'] = pattern_stats['positive_next_days'] / pattern_stats['total_appearances']

# Sort the patterns by the computed ratio in descending order
sorted_patterns = pattern_stats.sort_values(by='positive_ratio', ascending=False)

#print(sorted_patterns)

timeframes = [1, 3, 5, 8, 13]

# Calculate whether the day at each timeframe is positive or negative
for days_later in timeframes:
    column_name = f'{days_later}_days_later_positive'
    data[column_name] = (data['Close'].shift(-days_later) > data['Open'].shift(-days_later)).astype(int)

# Aggregating for each timeframe
aggregation = {
    'candlestick_pattern': 'size'
}
for days_later in timeframes:
    aggregation[f'{days_later}_days_later_positive'] = 'sum'

pattern_timeframe_stats = data.groupby('candlestick_pattern').agg(aggregation)

# Compute the ratio for each timeframe
for days_later in timeframes:
    pattern_timeframe_stats[f'{days_later}_days_later_ratio'] = (
        pattern_timeframe_stats[f'{days_later}_days_later_positive'] / 
        pattern_timeframe_stats['candlestick_pattern']
    )

# Keep only the ratio columns for cleaner output
ratio_columns = [f'{days_later}_days_later_ratio' for days_later in timeframes]
pattern_timeframe_stats = pattern_timeframe_stats[ratio_columns]

# Sort by the ratio for the next day (1 day later) for initial display
sorted_pattern_timeframe_stats = pattern_timeframe_stats.sort_values(by='1_days_later_ratio', ascending=False)

sorted_pattern_timeframe_stats['total_appearances'] = pattern_timeframe_stats['1_days_later_ratio'] * data.groupby('candlestick_pattern').size()

# Reorder the columns to display total appearances first
column_order = ['total_appearances'] + ratio_columns
sorted_pattern_timeframe_stats = sorted_pattern_timeframe_stats[column_order]

sorted_pattern_timeframe_stats.to_csv('btcDailyCandleMatchStats.csv')