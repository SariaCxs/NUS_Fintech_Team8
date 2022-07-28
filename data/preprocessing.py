import numpy as np
import pandas as pd
from pandas_datareader import data
from scipy.stats import norm


# calculate KDJ indicator

def KDJ(kdjdata):
    N = 9
    M1 = 3
    M2 = 3
    kdj = dict([('golden_cross', 0), ('death_cross', 0),
               ('overbought', 0), ('oversold', 0)])

    # The minimum and maximum of the previous N days are calculated, and the missing values are replaced by the minimum of the previous n days (n<N)
    lowList = kdjdata['Low'].rolling(N).min()
    lowList.fillna(value=kdjdata['Low'].expanding().min(), inplace=True)
    highList = kdjdata['High'].rolling(N).max()
    highList.fillna(value=kdjdata['High'].expanding().max(), inplace=True)

    rsv = (kdjdata['Close'] - lowList) / (highList - lowList) * 100

    kdjdata['kdj_k'] = rsv.ewm(alpha=1 / M1, adjust=False).mean()  # ewm is an exponentially weighted function
    kdjdata['kdj_d'] = kdjdata['kdj_k'].ewm(alpha=1 / M2, adjust=False).mean()
    kdjdata['kdj_j'] = 3.0 * kdjdata['kdj_k'] - 2.0 * kdjdata['kdj_d']

    # Calculate if there is a golden cross in three days
    for i in range(3):
        if kdjdata.kdj_k.values[-i - 2] < kdjdata.kdj_d.values[-i - 2] and kdjdata.kdj_k.values[-i - 1] > kdjdata.kdj_d.values[-i - 1] and \
                kdjdata.kdj_j.values[-i - 3] < kdjdata.kdj_k.values[-i - 3] and kdjdata.kdj_k.values[-i - 1] < kdjdata.kdj_k.values[-i - 1]:
            kdj['golden_cross'] = 1
            break

    # Calculate if there is a death cross in three days
    for i in range(3):
        if kdjdata.kdj_k.values[-i - 2] > kdjdata.kdj_d.values[-i - 2] and kdjdata.kdj_k.values[-i - 1] < kdjdata.kdj_d.values[-i - 1] and \
                kdjdata.kdj_j.values[-i - 3] > kdjdata.kdj_k.values[-i - 3] and kdjdata.kdj_k.values[-i - 1] > kdjdata.kdj_k.values[-i - 1]:
            kdj['death_cross'] = 1
            break

    # Calculate if there is a oversold
    if kdjdata.kdj_k.values[-1] <= 20 and kdjdata.kdj_d.values[-1] <= 20 and kdjdata.kdj_j.values[-1] <= 20:
        kdj['oversold'] = 1

    # Calculate if there is a overbought
    if kdjdata.kdj_k.values[-1] >= 80 and kdjdata.kdj_d.values[-1] >= 80 and kdjdata.kdj_j.values[-1] >= 80:
        kdj['overbought'] = 1

    return kdj


def BIAS(biasdata):
    N1 = 6
    N2 = 12
    N3 = 24
    bias = dict([('golden_cross', 0), ('death_cross', 0)])

    biasdata['BIAS1'] = (biasdata['Close'] - biasdata['Close'].rolling(N1).mean()) / biasdata['Close'].rolling(
        N1).mean() * 100
    biasdata['BIAS2'] = (biasdata['Close'] - biasdata['Close'].rolling(N2).mean()) / biasdata['Close'].rolling(
        N2).mean() * 100
    biasdata['BIAS3'] = (biasdata['Close'] - biasdata['Close'].rolling(N3).mean()) / biasdata['Close'].rolling(
        N3).mean() * 100

    # Calculate if there is a golden cross in three days
    for i in range(3):
        if biasdata.BIAS1.values[-i - 2] < biasdata.BIAS2.values[-i - 2] and biasdata.BIAS1.values[-i - 1] > biasdata.BIAS2.values[-i - 1]:
            bias['golden_cross'] = 1
            break
    for i in range(3):
        if biasdata.BIAS1.values[-i - 2] < biasdata.BIAS3.values[-i - 2] and biasdata.BIAS1.values[-i - 1] > biasdata.BIAS3.values[-i - 1]:
            bias['golden_cross'] = 1
            break

    # Calculate if there is a death cross in three days
    for i in range(3):
        if biasdata.BIAS1.values[-i - 2] > biasdata.BIAS2.values[-i - 2] and biasdata.BIAS1.values[-i - 1] < biasdata.BIAS2.values[-i - 1]:
            bias['death_cross'] = 1
            break
    for i in range(3):
        if biasdata.BIAS1.values[-i - 2] > biasdata.BIAS3.values[-i - 2] and biasdata.BIAS1.values[-i - 1] < biasdata.BIAS3.values[-i - 1]:
            bias['death_cross'] = 1
            break

    return bias


def MACD(macddata):
    macd = dict([('golden_cross', 0), ('death_cross', 0)])

    # EMA(12) and EMA(26)
    macddata['EMA12'] = macddata['Close'].ewm(
        alpha=2 / 13, adjust=False).mean()
    macddata['EMA26'] = macddata['Close'].ewm(
        alpha=2 / 27, adjust=False).mean()

    # calculate DIFF、DEA、MACD
    macddata['DIFF'] = macddata['EMA12'] - macddata['EMA26']
    macddata['DEA'] = macddata['DIFF'].ewm(alpha=2 / 10, adjust=False).mean()
    macddata['MACD'] = 2 * (macddata['DIFF'] - macddata['DEA'])

    # recognize golden cross in 3 days
    for i in range(3):
        if macddata.DIFF.values[-i - 2] < macddata.DEA.values[-i - 2] and macddata.DIFF.values[-i - 1] > macddata.DEA.values[-i - 1]:
            macd['golden_cross'] = 1
            break

    # recognize death cross in 3days
    for j in range(3):
        if macddata.DIFF.values[-j - 2] > macddata.DEA.values[-j - 2] and macddata.DIFF.values[-j - 1] < macddata.DEA.values[-j - 1]:
            macd['death_cross'] = 1
            break

    return macd


# Calculate DMA
def DMA(dmadata):
    N1 = 10
    N2 = 50
    M = 6
    dma = dict([('golden_cross', 0), ('death_cross', 0)])
    dmadata['MA1'] = dmadata['Close'].rolling(N1).mean()
    dmadata['MA2'] = dmadata['Close'].rolling(N2).mean()
    dmadata['DIF'] = dmadata['MA1'] - dmadata['MA2']
    dmadata['AMA'] = dmadata['DIF'].rolling(M).mean()

    # recognize golden cross in 3days
    for i in range(3):
        if dmadata.DIF.values[-i - 2] < dmadata.AMA.values[-i - 2] and dmadata.DIF.values[-i - 1] > dmadata.AMA.values[-i - 1]:
            dma['golden_cross'] = 1
            break
    # recognize death cross in 3days
    for i in range(3):
        if dmadata.DIF.values[-i - 2] > dmadata.AMA.values[-i - 2] and dmadata.DIF.values[-i - 1] < dmadata.AMA.values[-i - 1]:
            dma['death_cross'] = 1
            break
    return dma


def BOLL(bolldata):
    N = 20
    boll = dict([('high_break', 0), ('mid_break', 0), ('low_break', 0)])

    bolldata['BOLL'] = bolldata['Close'].rolling(N).mean()
    bolldata['UB'] = bolldata['BOLL'] + 2 * bolldata['Close'].rolling(N).std()
    bolldata['LB'] = bolldata['BOLL'] - 2 * bolldata['Close'].rolling(N).std()

    # judge whether cross upper within three days
    for i in range(3):
        if bolldata.Close.values[-i - 2] < bolldata.UB.values[-i - 2] and bolldata.Close.values[-i - 1] > bolldata.UB.values[-i - 1]:
            boll['high_break'] = 1
            break
    # judge whether cross mid within three days
    for i in range(3):
        if bolldata.Close.values[-i - 2] < bolldata.BOLL.values[-i - 2] and bolldata.Close.values[-i - 1] > bolldata.BOLL.values[-i - 1]:
            boll['mid_break'] = 1
            break

    # judge whether cross lower within three days
    for i in range(3):
        if bolldata.Close.values[-i - 2] < bolldata.LB.values[-i - 2] and bolldata.Close.values[-i - 1] > bolldata.LB.values[-i - 1]:
            boll['low_break'] = 1
            break

    return boll


def RSI(rsidata):
    N1 = 6
    N2 = 12
    N3 = 24

    rsi = dict([('golden_cross', 0), ('death_cross', 0),
               ('overbought', 0), ('oversold', 0)])

    rsidata['Change'] = rsidata['Close'] - rsidata['Close'].shift(1)  # 计算涨跌幅
    rsidata.loc[(rsidata['Close'].shift(1) == 0),
                'Change'] = 0  # if it is the first day, change = 0
    rsidata['x'] = rsidata['Change'].apply(lambda x: max(x, 0))  # 涨跌幅<0换为0
    rsidata['RSI1'] = rsidata['x'].ewm(alpha=1 / N1, adjust=0).mean() / (
        np.abs(rsidata['Change']).ewm(alpha=1 / N1, adjust=0).mean()) * 100
    rsidata['RSI2'] = rsidata['x'].ewm(alpha=1 / N2, adjust=0).mean() / (
        np.abs(rsidata['Change']).ewm(alpha=1 / N2, adjust=0).mean()) * 100
    rsidata['RSI3'] = rsidata['x'].ewm(alpha=1 / N3, adjust=0).mean() / (
        np.abs(rsidata['Change']).ewm(alpha=1 / N3, adjust=0).mean()) * 100

    # recognize golden cross
    golden1 = 0
    golden2 = 0
    for i in range(3):
        if rsidata.RSI1.values[-i - 2] < rsidata.RSI2.values[-i - 2] and rsidata.RSI1.values[-i - 1] > rsidata.RSI2.values[-i - 1]:
            golden1 = 1
            break
    for i in range(3):
        if rsidata.RSI1.values[-i - 2] < rsidata.RSI3.values[-i - 2] and rsidata.RSI1.values[-i - 1] > rsidata.RSI3.values[-i - 1]:
            golden2 = 1
            break
    if golden1 & golden2:
        rsi['golden_cross'] = 1

    # recognize death cross
    death1 = 0
    death2 = 0
    for i in range(3):
        if rsidata.RSI1.values[-i - 2] > rsidata.RSI2.values[-i - 2] and rsidata.RSI1.values[-i - 1] < rsidata.RSI2.values[-i - 1]:
            death1 = 1
            break
    for i in range(3):
        if rsidata.RSI1.values[-i - 2] > rsidata.RSI3.values[-i - 2] and rsidata.RSI1.values[-i - 1] < rsidata.RSI3.values[-i - 1]:
            death2 = 1
            break
    if death1 & death2:
        rsi['death_cross'] = 1

    # judge whether oversold
    if rsidata.RSI1.values[-1] <= 20 and rsidata.RSI2.values[-1] <= 20 and rsidata.RSI3.values[-1] <= 20:
        rsi['oversold'] = 1

    # judge whether overbought
    if rsidata.RSI1.values[-1] >= 80 and rsidata.RSI2.values[-1] >= 80 and rsidata.RSI3.values[-1] >= 80:
        rsi['overbought'] = 1

    return rsi


# Update daily_data
STOCK_LIST = pd.read_csv('Runes_clean.csv')['Rune']
cols = ['code', 'kdj_golden_cross', 'kdj_death_cross', 'kdj_oversold', 'kdj_overbought', 'bias_golden_cross', 'bias_death_cross',
        'macd_golden_cross', 'macd_death_cross', 'dma_golden_cross', 'dma_death_cross',
        'boll_high_break', 'boll_mid_break', 'boll_low_break',
        'rsi_golden_cross', 'rsi_death_cross', 'rsi_oversold', 'rsi_overbought']
daily_data = pd.DataFrame(columns=cols)
ind = ['kdj', 'bias', 'macd', 'dma', 'boll', 'rsi']
ind_func = [KDJ, BIAS, MACD, DMA, BOLL, RSI]
for stock in STOCK_LIST:
    try:
        print(stock)
        # read data
        result = []
        data = pd.read_csv(f'./StockData/{stock}.csv')
        if len(data) < 365:
            continue
        for func in ind_func:
            result.append(func(data))
        row = {}
        row['code'] = stock
        for i in range(len(ind)):
            for key in result[i].keys():
                ind_name = f'{ind[i]}_{key}'
                row[ind_name] = result[i][key]
        daily_data = daily_data.append(row, ignore_index=True)
    except FileNotFoundError:
        pass
daily_data.to_csv('./daily_data.csv')
