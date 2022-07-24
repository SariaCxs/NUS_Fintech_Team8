#Gain new data. VPN is needed
import yfinance as yf
import pandas as pd
import datetime
from pandas_datareader import data
from preprocessing import *
DATA = pd.read_csv("Runes_clean.csv")
DataTimeLen=datetime.timedelta(days=365*3)
for stock in DATA['Rune']:
    print("reading:"+stock,end="\r")
    Read= yf.Ticker(stock)
    STOCKDATA=Read.history(start=datetime.date.today()- DataTimeLen,end= datetime.date.today())
    #STOCKDATA = data.DataReader(stock, start=datetime.date.today()- DataTimeLen,end= datetime.date.today(),data_source='yahoo')

    STOCKDATA.to_csv('StockData/'+stock+'.csv')
print("\ndone!")



