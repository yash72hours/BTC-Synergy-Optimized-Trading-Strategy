import pandas as pd
import numpy as np

df = pd.read_csv('trade_logs.csv')
# Assuming df is your DataFrame with columns: entry_datetime, entry_price, exit_datetime, exit_price, pnl%
df['entry_datetime'] = pd.to_datetime(df['entry_datetime'])
df['exit_datetime'] = pd.to_datetime(df['exit_datetime'])

# 1. Win Rate
winning_trades = df[df['pnl%'] > 0]
win_rate = len(winning_trades) / len(df) * 100

# 2. Risk-Reward Ratio
average_win = winning_trades['pnl%'].mean()
losing_trades = df[df['pnl%'] < 0]
average_loss = losing_trades['pnl%'].mean()
if average_loss != 0:
    risk_reward_ratio = -average_win / average_loss
else:
    risk_reward_ratio = np.nan  # Avoid division by zero

# 3. Average Profit %
average_profit = df['pnl%'].mean()

# 4. Average Hold Duration (in days)
df['hold_duration'] = (df['exit_datetime'] - df['entry_datetime']).dt.total_seconds() / (60 * 60 * 24)  # Convert to days
average_hold_duration = df['hold_duration'].mean()

# 5. Static Return (sum of all percentage returns)
static_return = df['pnl%'].sum()

# 6. Compound Return
compound_return = np.prod((1 + df['pnl%'] / 100)) - 1

# Output all the statistics
stats = {
    'Win Rate (%)': win_rate,
    'Risk-Reward Ratio': risk_reward_ratio,
    'Average Profit (%)': average_profit,
    'Average Hold Duration (days)': average_hold_duration,
    'Static Return (%)': static_return,
    'Compound Return (%)': compound_return * 100
}

# Print the results
for stat, value in stats.items():
    print(f"{stat}: {value:.2f}")
