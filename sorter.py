import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
from data.classification import var


class KMeansSorter():
    def __init__(self):
        pass

    def sort(self,code_list):
        Data_mat = np.empty(shape=[0, 2])
        Dst_mat = np.empty(shape=[0, 1])

        for stock in code_list:
            STOCK_DATA = pd.read_csv("./data/StockData/" + stock + ".csv")
            AVR_EARN = (STOCK_DATA['Close'][len(STOCK_DATA) - 1] - STOCK_DATA['Close'][0]) / STOCK_DATA['Close'][0]
            Data_mat = np.append(Data_mat, [[var(STOCK_DATA), AVR_EARN]], axis=0)
            Dst_mat = np.append(Dst_mat, [0])


        kmeans = KMeans(n_clusters=4, random_state=0).fit(Data_mat)

        #y_predict = kmeans.predict(Data_mat)

        for n in range(Dst_mat.shape[0]):
            Dst_mat[n] = Cal_min_dest(Data_mat[n], kmeans.cluster_centers_)
        DICT_DATA = dict(zip(code_list, Dst_mat))
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

