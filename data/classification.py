import pandas as pd
import numpy as np
from scipy.stats import norm

# 计算个股月风险价值:历史模拟法和方差-协方差法的平均值
def var(data):

    #data = data.DataReader(stock ,start='2016' ,end='2020' ,data_source='yahoo')
    # data = pd.read_csv(f'StockData/{stock}.csv')

    redata = data['Close'].sort_index(ascending=True)
    redata = pd.DataFrame(redata)
    redata['Date'] = redata.index
    redata['Date'] = redata[['Date']].astype(str)
    redata['Rev' ]= redata.Close.diff(1)
    redata['Last_close' ]= redata.Close.shift(1)
    redata['Rev_rate' ]= redata['Rev' ] /redata['Last_close']
    redata = redata.dropna()

    sRate = redata["Rev_rate"].sort_values(ascending=True)
    var1 = np.percentile(sRate, 5, method='midpoint' ) *4.69

    u = redata.Rev_rate.mean()
    std  = redata.Rev_rate.std()
    var2 = (-norm.ppf(0.95 ) * std - u ) *4.69

    return (var1 +var2 ) /2


# 为风险承受力高的用户筛选极端收益可能更高的股票
def gain(data2):
    # 计算极端收益
    #data2 = data.DataReader(stock, start='2016', end='2020', data_source='yahoo')
    # data2 = pd.read_csv(f'StockData/{stock}.csv')
    redata2 = data2['Close'].sort_index(ascending=True)
    redata2 = pd.DataFrame(redata2)
    redata2['Date'] = redata2.index
    redata2['Date'] = redata2[['Date']].astype(str)
    redata2['Rev'] = redata2.Close.diff(1)
    redata2['Last_close'] = redata2.Close.shift(1)
    redata2['Rev_rate'] = redata2['Rev'] / redata2['Last_close']
    redata2 = redata2.dropna()

    sRate2 = redata2["Rev_rate"].sort_values(ascending=True)
    gain1 = np.percentile(sRate2, 95, method='midpoint') * 4.69
    print(gain1)

    u2 = redata2.Rev_rate.mean()
    std2 = redata2.Rev_rate.std()
    gain2 = (norm.ppf(0.95) * std2 - u2) * 4.69

    return (gain1 + gain2) / 2


#筛选长线股票
def longterm(longdata):
    #longdata = data.DataReader(stock,start='2021',end='2022',data_source='yahoo')
    # longdata = pd.read_csv(f'StockData/{stock}.csv')
    longdata['ma120']=longdata['Adj Close'].rolling(120).mean()
    longdata['ma60']=longdata['Adj Close'].rolling(60).mean()
    if  longdata.ma120[-1]>longdata.ma60[-1] or longdata.ma60.rolling(5).mean()[-1]>longdata.ma60.rolling(2).mean()[-1]:
        print(0)
        return False
    else:
        print(1)
        return True

 #筛选中线股票
def midterm(middata):
    #middata = data.DataReader(stock,start='2021',end='2022',data_source='yahoo')

    middata['ma30']= middata['Adj Close'].rolling(30).mean()
    middata['ma20'] = middata['Adj Close'].rolling(20).mean()
    if middata.ma30[-1]>middata.ma20[-1] or middata.ma20.rolling(5).mean()[-1]>middata.ma20.rolling(2).mean()[-1]:
        print(0)
        return False
    else:
        print(1)
        return True


  #筛选短线股票
def shortterm(shortdata):
    from pandas_datareader import data
    #shortdata = data.DataReader(stock,start='2021',end='2022',data_source='yahoo')
    # shortdata = pd.read_csv(f'StockData/{stock}.csv')
    shortdata['ma10'] =  shortdata['Adj Close'].rolling(10).mean()
    shortdata['ma5'] =   shortdata['Adj Close'].rolling(5).mean()
    shortdata['amplitude'] = (shortdata['High'] - shortdata['Low'])/shortdata['Close'].shift(1)
    shortdata['rev_rate'] = (shortdata.Close.diff(1))/shortdata['Close'].shift(1)
    count =0
    count2 = 0
    for amp in shortdata.amplitude[-15:-1]:
        if amp >0.04:
            count+=1
    print(count)
    for amp in shortdata.rev_rate[-15:-1]:
        if amp >0.05:
            count2+=1
    print(count2)
    if count > 5 or count2 > 3:
        print(11)
        return True
    if  shortdata.ma10[-1]< shortdata.ma5[-1] or  shortdata.ma5.rolling(5).mean()[-1]< shortdata.ma5.rolling(2).mean()[-1]:
        print(12)
        return True
    else:
        print(0)
        return False


# 根据投资偏好筛选
def coarse_sizing(stocks):
    risk0long = []
    risk0mid = []
    risk0short = []
    risk1long = []
    risk1mid = []
    risk1short = []
    risk2long = []
    risk2mid = []
    risk2short = []
    risk3long = []
    risk3mid = []
    risk3short = []


    for code in stocks:
        try:
            stock = pd.read_csv(f'StockData/{code}.csv')
            myvar = var(stock)
            if myvar > -0.1:
                if longterm(stock):
                    risk0long.append(stock)
                    risk1long.append(stock)
                    risk2long.append(stock)
                if midterm(stock):
                    risk0mid.append(stock)
                    risk1mid.append(stock)
                    risk2mid.append(stock)
                if shortterm(stock):
                    risk0short.append(stock)
                    risk1short.append(stock)
                    risk2short.append(stock)
            elif myvar > -0.15:
                if longterm(stock):
                    risk1long.append(stock)
                    risk2long.append(stock)
                if midterm(stock):
                    risk1mid.append(stock)
                    risk2mid.append(stock)
                if shortterm(stock):
                    risk1short.append(stock)
                    risk2short.append(stock)
            elif myvar > -0.2:
                if longterm(stock):
                    risk2long.append(stock)
                if midterm(stock):
                    risk2mid.append(stock)
                if shortterm(stock):
                    risk1short.append(stock)

            mygain = gain(stock)
            if mygain > 0.1:
                if longterm(stock):
                    risk3long.append(stock)
                if midterm(stock):
                    risk3mid.append(stock)
                if shortterm(stock):
                    risk3short.append(stock)
        except :
            pass

    return [risk0long, risk0mid, risk0short, risk1long, risk1mid, risk1short,
          risk2long, risk2mid, risk2short, risk3long, risk3mid, risk3short]


#对股票进行分类
import json
STOCK_LIST = pd.read_csv('Runes_clean.csv')['Rune']
json_file_path = 'classification.json'
json_file = open(json_file_path, mode='w')
result = coarse_sizing(STOCK_LIST)
json_content = []
for i in range(len(result)):
    json_content.append({i:result[i]})

print(json)

json.dump(json_content, json_file, indent=4)
# json.dump(save_json_content, json_file, ensure_ascii=False, indent=4) # 保存中文
