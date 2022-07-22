import pandas as pd
import yfinance as yf

def GetDemo(stockcode,startdate,enddate,col):
    #测试功能:ZM作为模板，直接读本地文件,输入时间段不管
    if stockcode == "ZM" :
        data = pd.read_csv("ZM.csv")
        data["Date"]= pd.to_datetime(data["Date"])
        data = data[(data.Date <= enddate) & (data.Date >= startdate)].set_index("Date")
    else:
        data = yf.download(stockcode,startdate,enddate,progress = True)
        
    col = col.split(" ")
    #选中用户选择的列
    data = data.filter(col)

    return data
    