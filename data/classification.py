import pandas as pd
import numpy as np
from scipy.stats import norm
import datetime
from dateutil.relativedelta import relativedelta


# calculate risk value for stock
def var(data):

    #data = data.DataReader(stock ,start='2016' ,end='2020' ,data_source='yahoo')
    # data = pd.read_csv(f'StockData/{stock}.csv')

    redata = data['Close'].sort_index(ascending=True)
    redata = pd.DataFrame(redata)
    redata['Date'] = redata.index
    redata['Date'] = redata[['Date']].astype(str)
    redata['Rev' ]= redata.Close.diff(1)
    redata['Last_close' ]= redata.Close.shift(1)
    redata['Rev_rate' ]= redata['Rev'] /redata['Last_close']
    redata = redata.dropna()

    sRate = redata["Rev_rate"].sort_values(ascending=True)

    var1 = np.percentile(sRate, 5, interpolation='midpoint' ) *4.69



    u = redata.Rev_rate.values.mean()
    std  = redata.Rev_rate.values.std()
    var2 = (-norm.ppf(0.95 ) * std - u ) *4.69

    return (var1 +var2 ) /2


# sift profitable stocks for users with high risk tolerance
def gainandbeta(data, ben):

    data2 = data
    spy = ben

    benchmark = spy.Close[-64:-5].pct_change().dropna()
    returns = data2.Close[-60:-1].pct_change().dropna()

    bla = np.vstack([benchmark, np.ones(len(returns))]).T
    result = np.linalg.lstsq(bla, returns,rcond=None)
    beta = result[0][0]

    redata2 = data2['Close'].sort_index(ascending=True)
    redata2 = pd.DataFrame(redata2)
    redata2['Date'] = redata2.index
    redata2['Date'] = redata2[['Date']].astype(str)
    redata2['Rev'] = redata2.Close.diff(1)
    redata2['Last_close'] = redata2.Close.shift(1)
    redata2['Rev_rate'] = redata2['Rev'] / redata2['Last_close']
    redata2 = redata2.dropna()

    # print(redata2.head(10))

    sRate2 = redata2["Rev_rate"].sort_values(ascending=True)
    gain1 = np.percentile(sRate2, 95, interpolation='midpoint') * 4.69
    # print(gain1)

    u2 = redata2.Rev_rate.values.mean()
    σ2 = redata2.Rev_rate.values.std()
    gain2 = (norm.ppf(0.95) * σ2 - u2) * 4.69
    # print(gain2)
    return beta, ((gain1 + gain2) / 2)


#screen long term result
def longterm(longdata):
    #longdata = data.DataReader(stock,start='2021',end='2022',data_source='yahoo')
    # longdata = pd.read_csv(f'StockData/{stock}.csv')
    longdata['ma90']=longdata['Close'].rolling(90).mean()
    longdata['ma60']=longdata['Close'].rolling(60).mean()
    if longdata.ma90.values[-1] > longdata.ma60.values[-1] or longdata.ma60.rolling(20).mean().values[-1] > longdata.ma60.values[-1] or \
            longdata.Close.values[-1] < longdata.ma60.values[-1]:
        return False
    else:
        return True

 #screen mid term result
def midterm(middata):
    #middata = data.DataReader(stock,start='2021',end='2022',data_source='yahoo')

    middata['ma60']= middata['Close'].rolling(60).mean()
    middata['ma30'] = middata['Close'].rolling(30).mean()
    if middata.ma60.values[-1]>middata.ma30.values[-1] or middata.ma30.rolling(10).mean().values[-1]>middata.ma30.values[-1] or middata.Close.values[-1] <middata.ma30.values[-1]:
        return False
    else:
        return True



# screen long term result
def shortterm(data, ben):
    shortdata = data
    spy = ben
    
    benchmark = spy.Close.pct_change()[-11:-5]
    returns = shortdata.Close.pct_change()[-7:-1]
    returns_above_mean = np.mean(returns - benchmark)

    if (returns_above_mean < 0):
        return False

    shortdata['ma10'] = shortdata['Close'].rolling(10).mean()
    shortdata['ma5'] = shortdata['Close'].rolling(5).mean()
    shortdata['amplitude'] = (shortdata['High'] - shortdata['Low']) / shortdata['Close'].shift(1)
    shortdata['rev_rate'] = (shortdata.Close.diff(1)) / shortdata['Close'].shift(1)

    count = 0
    count2 = 0

    for amp in shortdata.amplitude[-15:-1]:
        if amp > 0.04:
            count += 1
    for amp in shortdata.rev_rate.values[-15:-1]:
        if amp > 0.05:
            count2 += 1
    if count > 5 or count2 > 3:
        return True
    if shortdata.ma10.values[-1] < shortdata.ma5.values[-1] and shortdata.ma5.rolling(5).mean().values[-1] < shortdata.ma5.rolling(2).mean().values[
        -1]:
        return True
    else:
        return False


# screen based on user preference
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

    ben = pd.read_csv('./StockData/SPY.csv')
    for stock in stocks:
        print(stock)
        data = pd.read_csv(f'./StockData/{stock}.csv')
        myvar = var(data)
        if myvar > -0.125:
            if longterm(data):
                risk0long.append(stock)
                risk1long.append(stock)
                risk2long.append(stock)
            if midterm(data):
                risk0mid.append(stock)
                risk1mid.append(stock)
                risk2mid.append(stock)
            if shortterm(data, ben):
                risk0short.append(stock)
                risk1short.append(stock)
                risk2short.append(stock)
        elif myvar > -0.15:
            if longterm(data):
                risk1long.append(stock)
                risk2long.append(stock)
            if midterm(data):
                risk1mid.append(stock)
                risk2mid.append(stock)
            if shortterm(data, ben):
                risk1short.append(stock)
                risk2short.append(stock)
        elif myvar > -0.2:
            if longterm(data):
                risk2long.append(stock)
            if midterm(data):
                risk2mid.append(stock)
            if shortterm(data, ben):
                risk1short.append(stock)

        beta, mygain = gainandbeta(data, ben)
        if beta < 1.1:
            continue
        if mygain > 0.15:
            if longterm(data):
                risk3long.append(stock)
            if midterm(data):
                risk3mid.append(stock)
            if shortterm(data, ben):
                risk3short.append(stock)

    return [risk0long, risk0mid, risk0short, risk1long, risk1mid, risk1short,
          risk2long, risk2mid, risk2short, risk3long, risk3mid, risk3short]






def short_line_parameters(history):
    end_time = datetime.datetime.now().strftime('%Y-%m-%d')
    start_time = (datetime.datetime.now() + relativedelta(weeks=-1)).strftime('%Y-%m-%d')
    # history = data.DataReader(stock,start=start_time ,end= end_time ,data_source='yahoo')
    spy = pd.read_csv("StockData/SPY.csv")
    benchmark = spy.Close.pct_change().dropna()
    returns = history.Close.pct_change().dropna()

    returns_above_mean = np.mean(returns - benchmark)
    returns_above_var = np.var(returns - benchmark)
    # print(str(stock)+'returns_above_mean:'+str(returns_above_mean))
    # print(str(stock)+'returns_above_var:'+str(returns_above_var))

    return returns_above_mean, returns_above_var

if __name__ == '__main__':
    #classify stocks
    import json

    STOCK_LIST = pd.read_csv('Runes_clean.csv')['Rune']
    json_file_path = 'classification.json'
    json_file = open(json_file_path, mode='w')
    result = coarse_sizing(STOCK_LIST)
    json_content = []
    for i in range(len(result)):
        json_content.append({i: result[i]})

    print(json_content)

    json.dump(json_content, json_file, indent=4)














