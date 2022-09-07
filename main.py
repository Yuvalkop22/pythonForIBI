import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()
#ask the user what stock they want to look up
stock = input("Enter a stock ticker symbol: ")
print(stock)

startYear = 2019
startMonth = 1
startDay = 1

#datetime object
start = dt.datetime(startYear,startMonth,startDay)
now = dt.datetime.now()

df = pdr.get_data_yahoo(stock,start,now)


#print(df)
#
# ma = 50 #ממוצע נע
#
# smaString = "Sma_" + str(ma)
#
# df[smaString] = df.iloc[:,4].rolling(window=ma).mean()
#
# #print(df)
#
# df = df.iloc[ma:]
#
# #print(df)

emasUsed = [3,5,8,10,12,15,30,35,40,45,50,60]
for x in emasUsed:
    ema = x
    df["Ema_" + str(ema)] = round(df.iloc[:,4].ewm(span = ema, adjust=False).mean(),2)
print(df.tail()) #last few values from the data-frame

pos = 0
num = 0
percentChange = []

for i in df.index:
    cmin = min(df["Ema_3"][i],df["Ema_5"][i],df["Ema_8"][i],df["Ema_10"][i],df["Ema_12"][i],df["Ema_15"][i])
    cmax = max(df["Ema_30"][i],df["Ema_35"][i],df["Ema_40"][i],df["Ema_45"][i],df["Ema_50"][i],df["Ema_60"][i])

    close = df["Adj Close"][i]
    if (cmin > cmax):
        print("Red White Blue")
        if (pos == 0):
            buyPrice = close
            pos = 1
            print("Buying now at " + str(buyPrice))
    elif(cmin < cmax):
        print("Blue White Red")
        if (pos == 1):
            pos = 0
            sellPrice = close
            print("Selling now at " + str(sellPrice))
            pc = (sellPrice/buyPrice - 1) * 100
            percentChange.append(pc)

        if (num == df["Adj Close"].count()-1 and pos == 1):
            pos = 0
            sellPrice = close
            print("Selling now at " + str(sellPrice))
            pc = (sellPrice / buyPrice - 1) * 100
            percentChange.append(pc)
        num += 1
print(percentChange)

gains = 0



# for i in df.index:
#     #print(df.iloc[:,4][i])
#     if (df["Adj Close"][i] > df[smaString][i]):
#         print("The Close is higher")
#     else:
#         print("The Close is lower")