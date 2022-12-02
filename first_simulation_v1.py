# This ensures that our graphs will be shown properly in the notebook.
#%matplotlib inline

# Import Zipline functions that we need
from zipline import run_algorithm
from zipline.api import order_target_percent, symbol

# Import date and time zone libraries
from datetime import datetime
import pandas as pd

import pytz

# Import visualization
import matplotlib.pyplot as plt


def initialize(context):
    # Which stock to trade
    context.stock = symbol('MAXHEALTH')

    # Moving average window
    context.index_average_window = 100

def handle_data(context, data):
    # Request history for the stock
    equities_hist = data.history(context.stock, "close",
                                 context.index_average_window, "1d")

    # Check if price is above moving average
    if equities_hist[-1] > equities_hist.mean():
        stock_weight = 1.0
    else:
        stock_weight = 0.0

    # Place order
    order_target_percent(context.stock, stock_weight)

def analyze(context, perf):
    fig = plt.figure(figsize=(12, 8))

    # First chart
    ax = fig.add_subplot(111)
    ax.set_title('Strategy Results')
    ax.semilogy(perf['portfolio_value'], linestyle='-',
                label='Equity Curve', linewidth=3.0)
    ax.legend()
    ax.grid(False)

# Set start and end date
#start_date = datetime(2017, 1, 1, tzinfo=pytz.UTC)
#end_date = datetime(2018, 12, 31, tzinfo=pytz.UTC)

start_date = pd.Timestamp('2020-08-21', tz='utc')
end_date = pd.Timestamp('2022-12-01', tz='utc')

# Fire off the backtest
results = run_algorithm(
    start=start_date,
    end=end_date,
    initialize=initialize,
    analyze=analyze,
    handle_data=handle_data,
    capital_base=10000,
    data_frequency = 'daily', bundle='yahoo_NSE'
)