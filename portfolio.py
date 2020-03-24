import pandas as pd

def loadInvestments(filename):
    '''Reads in a file and returns city name, home price, and potential profit
    in three separate lists
    :param csvfile filename: Zillow flat file to read in and store as dataframe
    '''
    zillow_data = pd.read_csv(filename)
    #Remove national aggregate information in first row of dataframe
    zillow_data = zillow_data.iloc[1:]
    #Extract data we need from dataframe and store it in lists
    price_delta = (zillow_data['2020-01']-zillow_data['2019-01']).to_list()
    current_prices = zillow_data['2020-01'].to_list()
    cities = zillow_data['RegionName'].to_list()
    return list(zip(cities, current_prices, price_delta))

def optimizeInvestments(home_data, budget, increment_amount):
    '''Using dynammic programming, returns both the optimal return on investment amount as well as
    the actual investments selected to achieve this optimal.
    :param list home_data: list of tuples containing cities, current home prices, and potential profits
    :param int budget: total budget available to spend across the portfolio
    :param int increments: the smallest increment the dollar amount can have when spending
    '''
    #Unpack list of tuples, store tuple elements in separate lists
    cities = [x[0] for x in home_data]
    home_costs = [x[1] for x in home_data]
    potential_profits = [x[2] for x in home_data]
    spending_increments = []
    #Add increment amount to total budget to ensure 'width' dimension of twoD_table defined below is long enough
    budget = budget+increment_amount
    #Create a list of values that represents the spending increments we have to use
    for i in range(0,budget, increment_amount):
        spending_increments.append(i)
    width_of_twoD_table = len(spending_increments)
    height_of_twoD_table = len(potential_profits)
    #Create and fill 2D table that represents number of investments and amount of money to spend.
    #Table is initially filled with 0s that will be replaced if appropriate
    twoD_table = [[0 for x in range(width_of_twoD_table)] for i in range(height_of_twoD_table)]
    #Iterate over rows of twoD_table
    for items in range(len(potential_profits)):
        #Iterate over columns of twoD_table, which represents money available to spend
        for increment in range(len(spending_increments)):
             #If the home costs more than the allowed budget at that column, take above value
            if home_costs[items]>spending_increments[increment]:
                twoD_table[items][increment] = twoD_table[items-1][increment]
                continue
            #Get column value in the row prior and store in variable to be used if necessary
            prior_value = twoD_table[items-1][increment]
            #To determine best option in the event that the home in question does not cost more than the
            #allowed budget at that column, add potential profit represented by the current home and whichever value
            #from above row that adds the maximum amount to potential profit
            new_best_option = potential_profits[items]+twoD_table[items-1][increment-(home_costs[items]//increment_amount)]
            #If the cost of the current item is greater than allowed budget, then we can't 'afford' the new_best_option
            #so pick the maximum of prior value or the potential profit represented by the current house and replace
            #current row/col value with this value. If we can afford the new_best_option, take larger of new_best_option
            #or prior value and replace current row/col value with this value
            if (spending_increments[-1]-home_costs[items]) > spending_increments[-1]:
                twoD_table[items][increment] = max(prior_value,potential_profits[items])
            else:
                twoD_table[items][increment] = max(prior_value,new_best_option)

    #Iterate over twoD_table and select which investments were used to achieve the optimal
    cities_used = []
    for i in range(len(potential_profits)-1, 0,-1):
        #Walk through table backwards, check if column value is the same as column value of the previous row. If yes, item was
        #not included in optimal, move on to next item. If no, add item to list and subtract its weight from
        #the remaining budget we have.
        if twoD_table[i][(budget//increment_amount)-1] !=twoD_table[i-1][(budget//increment_amount)-1]:
            a = (cities[i],potential_profits[i], home_costs[i])
            #Since we walked through the table backwards, use 'insert' instead of append to add
            #cities used in top down order
            cities_used.insert(0,a)
            budget -= home_costs[i]

    optimal_investment_amount = twoD_table[-1][-1]
    return optimal_investment_amount, cities_used

everything = loadInvestments('Metro.csv')
vv = optimizeInvestments(everything, 1000000, 1000)
print(vv)
