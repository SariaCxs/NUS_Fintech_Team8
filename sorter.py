import tushare as ts
import torch
from model.lstm import LSTM_Regression
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
from data.classification import var

class LSTMSorter():
    def __init__(self):
        self.model = self.load_model()


    def sort(self,data, cols):
        '''
        :param data: dic include stock code and dataframe
        :param cols: column needed to predict the result
        :return: rankresult a sorted list of stock code, predict price and rise percent
        '''
        rank_result = []
        for code in data.keys():

            pred, rise = self.predict(data[code],cols)
            rank_result.append({'code': code, 'pred': pred, 'rise': rise})
        rank_result = sorted(rank_result, key=lambda r: r['rise'], reverse=True)
        return rank_result

    def predict(self,data,cols):
        data = data[cols].values
        data = data.astype('float32')
        # 归一化
        max_value = np.max(data)
        min_value = np.min(data)
        
        min_max_data = (data - min_value) / (max_value - min_value)

        x_data = torch.from_numpy(min_max_data.reshape(-1, 1, 60))
        pred = self.model(x_data).reshape(-1)[0]
        #反归一化并输出预测值
        pred = pred * (max_value - min_value) + min_value
        rise = 100 * (pred - data[-1]) / data[-1]

        return np.round(pred.detach().numpy(), 2), np.round(rise.detach().numpy(), 2)


    def load_model(self):
        state_dict = torch.load('./model/lstm.pth')
        model = LSTM_Regression(60, 8, output_size=1, num_layers=2)
        model.load_state_dict(state_dict)
        model = model.eval()
        return model

def Cal_min_dest(INPUT_POINT, INDEX_POINTS):
    dst_out = 100
    for cal_Index in INDEX_POINTS:
        dst_out = min(np.linalg.norm(INPUT_POINT - cal_Index), dst_out)
    return dst_out

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

