import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

def GetDemo(stockcode,startdate,enddate,col):
    #测试功能:ZM作为模板，直接读本地文件,输入时间段不管
    now = datetime.datetime.now()
    if startdate == "" and enddate == "":
        enddate = str(now.date())
        startdate = str((now - relativedelta(months=2)).date())
    data = pd.read_csv("./data/StockData/" + stockcode + ".csv")
    data["Date"]= pd.to_datetime(data["Date"])
    data = data[(data.Date <= enddate) & (data.Date >= startdate)].set_index("Date")
        
    col = col.split(" ")
    #选中用户选择的列
    data = data.filter(col)

    return data
    