# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 15:33:10 2021

@author: regru
"""




import os
import numpy as np
import pandas as pd
import requests
os.chdir('C:/Users/regru/Desktop/AutoTrader_AlphaAdvantage')
pd.options.display.max_columns = None
#BKXNTWKML10AHHQK
key = 'BKXNTWKML10AHHQK'

# Get listing of all symbols
amex = pd.read_csv('AMEX.csv')
nyse = pd.read_csv('NYSE.csv')
nasdaq = pd.read_csv('NASDAQ.csv')
all_sym = pd.concat([amex[['Symbol','Name']],nyse[['Symbol','Name']],nasdaq[['Symbol','Name']]])

###########
# Can only download 5 symbols per minute and max of 500 per day
for i in range(500):
    # Symbols that we already have data for
    completed_syms0 = pd.read_csv('Historical_Data.csv')
    completed_syms = completed_syms0['Symbol'].unique()
    # Symbols that we don't have data for
    unique_syms = set(all_sym['Symbol']) - set(completed_syms)  
    # DF to store all stocks downloaded per day
    all_df = pd.DataFrame(columns=['Date','Open', 'High', 'Low', 'Close', 'Volume','Symbol'])
    # Loop at 5 requests per minute for a max of 500 per day
    API_URL = "https://www.alphavantage.co/query" 
    #symbol = 'MSFT'
    for sym in unique_syms[0:5]:
        # Inputs
        data = { "function": "TIME_SERIES_DAILY", 
        "symbol": sym,
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
    # Write to .csv
    all_df.to_csv('Historical_Data.csv',index=False)



































