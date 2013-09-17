# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

print "Pandas Version", pd.__version__

def simulate(startDate, endDate, symbols, allocations):
    '''Function for calculating sharpe ratio and other factors'''
    
    volatility = 0.0
    avgDailyReturn = 0.0
    sharpeRatio = 0.0
    cumulativeReturn = 0.0

    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(startDate, endDate, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    # we will fetch data from finance.yahoo.com
    c_dataobj = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Copying close price into separate dataframe to find rets
    df_rets = d_data['close'].copy()

    # Filling the data.
    df_rets = df_rets.fillna(method='ffill')
    df_rets = df_rets.fillna(method='bfill')
    df_rets = df_rets.fillna(1.0)

    # Numpy matrix of filled data values
    na_rets = df_rets.values
    
    print na_rets


    return (volatility, avgDailyReturn, sharpeRatio, cumulativeReturn)


def main():
    ''' Main Function'''

    # List of symbols
    ls_symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]

    # Start and End date of the charts
    dt_start = dt.datetime(2011, 12, 1)
    dt_end = dt.datetime(2011, 12, 8)

    (lf_volatility, lf_avgDailyReturn, lf_sharpeRatio, lf_cumulativeReturn) = simulate(dt_start, dt_end, ls_symbols, [0.1, 0.2, 0.4, 0.3])
    
if __name__ == '__main__':
    main()

# Start Date: January 1, 2011
# End Date: December 31, 2011
# Symbols: ['AAPL', 'GLD', 'GOOG', 'XOM']
# Optimal Allocations: [0.4, 0.4, 0.0, 0.2]
# Sharpe Ratio: 1.02828403099
# Volatility (stdev of daily returns):  0.0101467067654
# Average Daily Return:  0.000657261102001
# Cumulative Return:  1.16487261965
