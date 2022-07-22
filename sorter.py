import tushare as ts
import torch
from model.lstm import LSTM_Regression
import numpy as np

class Sorter():
    def __init__(self):
        self.model = self.load_model()


    def sort(self,data, cols):
        '''
        :param data: dic include stock code and dataframe
        :param cols: column needed to predict the result
        :return: rankresult a sorted list of stock code, predict price and rise percent
        '''
        rank_result = []
        print(data)
        for code in data.keys():

            pred, rise = self.predict(data[code],cols)
            rank_result.append({'code': code, 'pred': pred, 'rise': rise})
        rank_result = sorted(rank_result, key=lambda r: r['rise'], reverse=True)
        return rank_result

    def predict(self,data,cols):
        data = data[cols].values
        data = data.astype('float32')
        max_value = np.max(data)
        min_value = np.min(data)
        min_max_data = (data - min_value) / (max_value - min_value)
        x_data = torch.from_numpy(min_max_data.reshape(-1, 1, 60))
        pred = self.model(x_data).reshape(-1)[0]
        pred = pred * (max_value - min_value) + min_value
        rise = 100 * (pred - data[-1]) / data[-1]

        return np.round(pred.detach().numpy(), 2), np.round(rise.detach().numpy(), 2)


    def load_model(self):
        state_dict = torch.load('./model/lstm.pth')
        model = LSTM_Regression(60, 8, output_size=1, num_layers=2)
        model.load_state_dict(state_dict)
        model = model.eval()
        return model





