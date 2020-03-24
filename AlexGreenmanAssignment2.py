from operator import itemgetter
import pandas as pd
pd.options.mode.chained_assignment = None

def MSSDAC(A, low, high):
    '''Using divide and conquer, finds the contiguous subarray whose
    sum is largest.
    :param list A: The list you are searching for maximum contiguous subarray
    :param int low: Beginning of list you are searching
    :param int high: End of list you are searching'''
    #base case - when list is one element, return element if positive,
    #otherwise, return zeroes
    if low == high-1:
        if A[low]>0:
            return low,high-1, A[low]
        else:
            return 0,0,0
    else:
        #calculate list mid point to be used to in recursive calls
        mid = (low + high)//2
        #recursively call function until base case is reached, returns tuple of values
        left_list_low_index, left_list_high_index, left_list_max = MSSDAC(A, low, mid)
        right_list_low_index, right_list_high_index, right_list_max = MSSDAC(A, mid, high)
        #in each recursive call, reset left_sum and left_sum_temp since you are
        #dealing with a 'new' array and subarrays
        left_sum = float('-inf')
        left_sum_temp = 0
        bridge_list_low_index = mid
        #iterate over left side of list, working backwords from the mid point
        for i in range(mid - 1, low - 1, -1):
            #add up values being iterated over to themselves
            left_sum_temp += A[i]
            #if values added are greater than -inf, set left_sum = to left_sum_temp and
            #update the index position in order to know where the left list has ended
            if left_sum_temp > left_sum:
                left_sum = left_sum_temp
                bridge_list_low_index = i
        #in each recursive call, reset right_sum and right_sum_temp since you are
        #dealing with a 'new' array and subarrays
        right_sum = float('-inf')
        right_sum_temp = 0
        bridge_list_high_index = mid
        #iterate over right side of list, working forwards from the mid point
        for i in range(mid, high):
            #add up values being iterated over to themselves
            right_sum_temp += A[i]
            if right_sum_temp > right_sum:
                #if values added are greater than -inf, set right_sum = right_sum_temp and
                #update the index position in order to know where the right list has ended
                right_sum = right_sum_temp
                bridge_list_high_index = i+1
        #add together sums of left list and right list, to be compared against
        #maximum sum of left and right lists individually
        bridge_list_max = left_sum+right_sum
        #The maximum subarray profit is either the maximum subarray profit
        #of one of the halves or the maximum subarray bridging the midpoint
        #of the two halves
        if left_list_max > right_list_max and left_list_max > bridge_list_max:
            return left_list_low_index, left_list_high_index, left_list_max
        elif right_list_max > left_list_max and right_list_max > bridge_list_max:
            return right_list_low_index, right_list_high_index, right_list_max
        else:
            return bridge_list_low_index, bridge_list_high_index, bridge_list_max

def read_files(securities_file, prices_file):
    '''Reads in csv files containing historical stock data, merges them into a
    single dataframe on the common symbol column, and then trims the dataframe
    to contain only the requisite columns.
    :param csvfile securities_file: file to read in and store as dataframe
    :param csvfile prices_file: file to read in and store as dataframe'''
    securities = pd.read_csv(securities_file)
    securities.rename(columns={'Ticker symbol': 'symbol'}, inplace = True)
    psa = pd.read_csv(prices_file)
    #merge the two dataframes on the common column
    psa_securities = pd.merge(securities, psa, on = 'symbol')
    #trim the merged dataframe so it has relevant information only
    psa_securities = psa_securities[['symbol','Security','date', 'open','close','low','high','volume']]
    return psa_securities

def find_ticker_max_profit(ticker_df, ticker = None, all_tickers = False):
    '''Depending on parameter input, returns maximum profit for a single stock,
    or maximum profit for all stocks contained in ticker_df.
    :param dataframe ticker_df: dataframe containing stock prices and associated data
    :param str ticker: particular stock you are interested in getting max profit for
    :param bool all_tickers: boolean to toggle based on whether you want max profit
    for a single stock or all stocks'''
    list_of_tuples = []
    #create list of stock tickers to be iterated over
    list_of_symbols = list(set(ticker_df['symbol'].to_list()))
    #if all stocks are to be checked for max profit
    if all_tickers and ticker is None:
        for symbol in list_of_symbols:
            #create dataframe object for each stock
            symbol_df = ticker_df.loc[ticker_df['symbol'] == symbol]
            #calculate difference in day over day closing price for stock
            symbol_df['price_delta'] = symbol_df.close.diff()
            #reset data frame index so index can be used to find buy and sell dates
            symbol_df.reset_index(inplace=True)
            #get full company name for relevant stock
            security = symbol_df['Security'][0]
            #store difference in day over day closing price for stock as a list
            diff_in_closing_prices = symbol_df['price_delta'].to_list()
            #pass list of price differences to MSSDAC function
            start, end, maximum = MSSDAC(diff_in_closing_prices, 0, len(diff_in_closing_prices))
            #use indices returned by MSSDAC function to find buy and sell date
            #for that particular stock's maximum profit. Subtract one so that date bought
            #is one day prior to stock's optimal run (since we are dealing with differences
            #in closing prices) and day sold is the day the optimal run ends
            start_date = symbol_df['date'][start-1]
            end_date = symbol_df['date'][end-1]
            #append tuple containing each stock's information to list
            list_of_tuples.append((symbol,security,start_date,end_date,maximum))
        #use built in itemgetter to find tuple that contains maximum stock profit
        #from list of tuples and return it
        winner = max(list_of_tuples,key=itemgetter(4))
        return f'Best stock to buy: {winner[1]} on {winner[2]} and sell on {winner[3]} with profit {winner[4]}'
    else:
        #create dataframe object for requested stock
        symbol_df = ticker_df.loc[ticker_df['symbol'] == ticker]
        #calculate difference in day over day closing price for stock
        symbol_df['price_delta'] = symbol_df.close.diff()
        #reset data frame index so index can be used to find buy and sell dates
        symbol_df.reset_index(inplace=True)
        #get full company name for relevant stock
        security = symbol_df['Security'][0]
        #store difference in day over day closing price for stock as a list
        diff_in_closing_prices = symbol_df['price_delta'].to_list()
        #pass list of price differences to MSSDAC function
        start, end, maximum = MSSDAC(diff_in_closing_prices, 0, len(diff_in_closing_prices))
        #use indices returned by MSSDAC function to find buy and sell date
        #for that particular stock's maximum profit. Subtract one so that date bought
        #is one day prior to stock's optimal run (since we are dealing with differences
        #in closing prices) and day sold is the day the optimal run ends
        start_date = symbol_df['date'][start-1]
        end_date = symbol_df['date'][end-1]

        return f'Best time to buy and sell {security} (ticker = {ticker}) stock: buy on {start_date} and sell on {end_date} with profit {maximum}'

ticker_df = read_files('securities.csv', 'prices-split-adjusted.csv')
AAPL_max_profit = find_ticker_max_profit(ticker_df, ticker = 'AAPL', all_tickers = False)
all_stocks_max_profit = find_ticker_max_profit(ticker_df, ticker = None, all_tickers = True)

print(AAPL_max_profit)
print(all_stocks_max_profit)
