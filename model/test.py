import matplotlib.pyplot as plt
import numpy as np
import tushare as ts
import torch
from torch import nn
import datetime
import time
from lstm import LSTM_Regression


DAYS_FOR_TRAIN = 10

def create_dataset(data_close,days_for_train=5):
    x = []
    y = []
    max_value = np.max(data_close)
    min_value = np.min(data_close)
    data = (data_close - min_value) / (max_value - min_value)
    for i in range(len(data) - days_for_train):
        x_data = data[i:(i+days_for_train)]
        x.append(x_data)
        y.append(data[i+days_for_train])
    return np.array(x),np.array(y)



if __name__ == '__main__':
    data_close = ts.get_k_data('000004',start='2019-01-01')['close']
    data_close = data_close.astype('float32').values
    plt.plot(data_close)
    plt.savefig('data.png',format='png',dpi=200)
    plt.close()



    x_dataset, y_dataset = create_dataset(data_close,DAYS_FOR_TRAIN)

    #load model
    state_dict = torch.load('lstm.pth')
    model = LSTM_Regression(DAYS_FOR_TRAIN, 8, output_size=1, num_layers=2)
    model.load_state_dict(state_dict)

    model = model.eval()
    x_dataset = torch.from_numpy(x_dataset.reshape(-1, 1, DAYS_FOR_TRAIN))
    y_dataset = y_dataset.reshape(-1, 1, 1)

    pred = model(x_dataset) .view(-1).detach().numpy()

    pred = np.concatenate((np.zeros(DAYS_FOR_TRAIN), pred))  # 填充0 使长度相同
    assert len(pred) == len(data_close)

    plt.plot(pred, 'r', label='prediction')
    plt.plot(data_close, 'b', label='real')
    #plt.plot((train_size, train_size), (0, 1), 'g--')  # 分割线 左边是训练数据 右边是测试数据的输出
    plt.legend(loc='best')
    plt.savefig('result.png', format='png', dpi=200)
    plt.close()


