# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 20:23:25 2018
This is for python 3
@author: Maverick
"""

import pandas as pd
import cryptocompare_maverick as MLLC

Mapi = MLLC.CryptocompareMaverick()


# get meta data
message, coinlist = Mapi.getMetadataListCoins()     #separate the response and data
coins = pd.DataFrame.from_dict(coinlist, orient='index')

# get historical data
symbol='ETH'
message, data = Mapi.getHistoDayFull(symbol, to_symbol = 'USD')
price_df = pd.DataFrame(data)



