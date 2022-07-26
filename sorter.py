import numpy as np
from sklearn.cluster import KMeans
import pandas as pd




def Cal_min_dest(INPUT_POINT,INDEX_POINTS):
    dst_out=100000
    n=0
    for cal_Index in INDEX_POINTS:
        DST=np.linalg.norm(INPUT_POINT-cal_Index)
        if DST<dst_out:
            Idx_out=n
            dst_out=DST
        n+=1
    return dst_out,int(Idx_out)


def cal_alphabeta(history, cycle, spy):

    benchmark = spy.Close.pct_change().dropna()
    LEN_CAL = min(len(history), len(benchmark))
    # print(LEN_CAL)
    benchmark = benchmark[-LEN_CAL:]
    returns = history[-LEN_CAL:]

    bla = np.vstack([benchmark, np.ones(len(returns))]).T

    result = np.linalg.lstsq(bla, returns, rcond=-1)

    beta = result[0][0]
    alpha = result[0][1]

    return alpha, beta


def short_line_parameters(history, spy):

    benchmark = spy.Close.pct_change().dropna()
    LEN_CAL = min(len(history), len(benchmark))
    benchmark = benchmark[-LEN_CAL:]
    returns = history[-LEN_CAL:]  # .Close.pct_change().dropna()

    returns_above_mean = np.mean(returns - benchmark)
    returns_above_var = np.var(returns - benchmark)


    return returns_above_mean, returns_above_var


class KMeansSorter():
    def __init__(self):
        pass

    def sort(self,code_list):
        Data_mat = np.empty(shape=[0, 2])
        Dst_mat = np.empty(shape=[0, 1])
        Sym_mat = np.empty(shape=[0, 1])
        spy = pd.read_csv('./data/StockData/SPY.csv')

        for stock in code_list:
            STOCK_DATA = pd.read_csv("./data/StockData/" + stock + ".csv")['Close']
            #AVR_EARN = (STOCK_DATA['Close'][len(STOCK_DATA) - 1] - STOCK_DATA['Close'][0]) / STOCK_DATA['Close'][0]
            alpha, beta = cal_alphabeta(STOCK_DATA, "month",spy)
            returns_above_mean, returns_above_var = short_line_parameters(STOCK_DATA,spy)
            Data_mat = np.append(Data_mat, [[alpha, beta]], axis=0)
            Dst_mat = np.append(Dst_mat, [0])
            Sym_mat = np.append(Sym_mat, stock)
        print(Data_mat.shape)
        COUNTDEL = 0



        KmeansTypeAmount = 10
        Core_mat = np.empty(shape=[0, 1])
        Core_count = np.zeros(KmeansTypeAmount)

        for DATA in Data_mat:
            if np.isnan(DATA).any():
                # print(DATA,COUNTDEL)
                Data_mat = np.delete(Data_mat, COUNTDEL, axis=0)
                Dst_mat = np.delete(Dst_mat, COUNTDEL, axis=0)
                Sym_mat = np.delete(Sym_mat, COUNTDEL, axis=0)
            else:
                COUNTDEL += 1

        print(Data_mat.shape)

        kmeans = KMeans(n_clusters=KmeansTypeAmount, random_state=0).fit(Data_mat)

        for n in range(COUNTDEL):
            Dst_mat[n], CORE_NEAREST = Cal_min_dest(Data_mat[n], kmeans.cluster_centers_)
            Core_mat = np.append(Core_mat, CORE_NEAREST)
            Core_count[CORE_NEAREST] += 1

        CORE_USE = 0
        MAX_ALPHA = 0
        for n in range(KmeansTypeAmount):
            if (Core_count[n] > COUNTDEL / (2 * KmeansTypeAmount) and MAX_ALPHA < kmeans.cluster_centers_[n][0]):
                CORE_USE = n
                MAX_ALPHA = kmeans.cluster_centers_[n][0]

        print(CORE_USE)
        COUNTDEL = 0
        for DATA in Dst_mat:
            if Core_mat[COUNTDEL] != CORE_USE:
                # print(DATA,COUNTDEL)
                Dst_mat = np.delete(Dst_mat, COUNTDEL, axis=0)
                Sym_mat = np.delete(Sym_mat, COUNTDEL, axis=0)
                Core_mat = np.delete(Core_mat, COUNTDEL, axis=0)
            else:
                COUNTDEL += 1

        DICT_DATA = dict(zip(Sym_mat, Dst_mat))
        return  self.sort_by_value(DICT_DATA)



    def sort_by_value(self,d):
        items = d.items()
        backitems = [[v[1], v[0]] for v in items]
        backitems.sort()
        return [backitems[i][1] for i in range(0, len(backitems))]






if __name__ == '__main__':
    kmeans = KMeansSorter()
    code = pd.read_csv('./data/Runes_clean.csv')['Rune']
    print(kmeans.sort(code))

