# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 15:33:10 2021

@author: regru
"""




import os
import numpy as np
import pandas as pd
import re
import requests
import time
os.chdir('C:/Users/rrussell1/Desktop/Docs/Widgets_Exercise-master/Python_Trading')
pd.options.display.max_columns = None
#BKXNTWKML10AHHQK
key = 'BKXNTWKML10AHHQK'

# Get listing of all symbols
amex = pd.read_csv('AMEX.csv')
nyse = pd.read_csv('NYSE.csv')
nasdaq = pd.read_csv('NASDAQ.csv')
all_sym = pd.concat([amex[['Symbol','Name']],nyse[['Symbol','Name']],nasdaq[['Symbol','Name']]])
# DF to store all stocks downloaded per day
all_df = pd.read_csv('Historical_Data.csv') #pd.DataFrame(columns=['Date','Open', 'High', 'Low', 'Close', 'Volume','Symbol'])
# Loop at 5 requests per minute for a max of 500 per day
API_URL = "https://www.alphavantage.co/query"
daily_limit = """{'Information': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}"""

###########
# Can only download 5 symbols per minute and max of 500 per day
i = 0
response_json = []
errors = []
while response_json != daily_limit:
    # Symbols that we already have data for
    completed_syms0 = pd.read_csv('Historical_Data.csv') #pd.DataFrame(columns=['Date','Open','High','Low','Close','Volume','Symbol']) 
    completed_syms = completed_syms0['Symbol'].unique()
    # Symbols that we don't have data for
    unique_syms = sorted(list(set(all_sym['Symbol']) - set(completed_syms))) 
    #symbol = 'MSFT'
    for sym in unique_syms[0:5]:
        # Inputs
        data = { "function": "TIME_SERIES_DAILY", 
        "symbol": sym.split('^')[0].split('/')[0],
        "outputsize" : "full",
        "datatype": "json", 
        "apikey": key } 
        # Data request
        response = requests.get(API_URL, data) 
        response_json = response.json()
        try:
            response_json['Time Series (Daily)']
        except Exception as err:
            errors.append([sym,err])
            break
        # Dataframe
        data = pd.DataFrame.from_dict(response_json['Time Series (Daily)'], orient= 'index').sort_index(axis=1)
        data = data.reset_index().rename(columns={'index':'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'})
        data['Symbol'] = sym
        # Combine all data
        all_df = all_df.append(data,ignore_index=True,sort=False)
        # Pause loop for 1 minute
    time.sleep(60)
    # Write to .csv
    i += 1
    all_df.to_csv('Historical_Data.csv',index=False)






###############################################################################################################
###############################################################################################################
###############################################################################################################
####################################################### Testing ###############################################
###############################################################################################################
###############################################################################################################
completed_syms0 = pd.read_csv('Historical_Data.csv') #pd.DataFrame(columns=['Date','Open','High','Low','Close','Volume','Symbol']) 
completed_syms = completed_syms0['Symbol'].unique()
# Symbols that we don't have data for
unique_syms = sorted(list(set(all_sym['Symbol']) - set(completed_syms))) 
#symbol = 'MSFT'
for sym in unique_syms[0:2]:
    # Inputs
    data = { "function": "TIME_SERIES_DAILY", 
    "symbol": sym.split('^')[0],
    "outputsize" : "full",
    "datatype": "json", 
    "apikey": key } 
    # Data request
    response = requests.get(API_URL, data) 
    response_json = response.json()
    # Dataframe
    data = pd.DataFrame.from_dict(response_json['Time Series (Daily)'], orient= 'index').sort_index(axis=1)
    data = data.reset_index().rename(columns={'index':'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'})
    data['Symbol'] = sym
    # Combine all data
    all_df = all_df.append(data,ignore_index=True,sort=False)
    # Pause loop for 1 minute
    # time.sleep(60)
# Write to .csv
# i += 1
all_df.to_csv('Historical_Data.csv',index=False)




re.sub('[^A-Za-z0-9]+', '', sym)
'IBM'.split('^')[0]

# How many symbols do I have
all_df['Symbol'].unique()

#time.sleep(number of seconds)

"""{'Information': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}"""



























