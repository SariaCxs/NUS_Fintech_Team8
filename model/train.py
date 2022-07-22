import matplotlib.pyplot as plt
import numpy as np
import tushare as ts
import torch
from torch import nn
import datetime
import time
from lstm import LSTM_Regression


DAYS_FOR_TRAIN = 60

def create_dataset(data,days_for_train=5):
    x = []
    y = []
    for i in range(len(data) - days_for_train):
        x_data = data[i:(i+days_for_train)]
        x.append(x_data)
        y.append(data[i+days_for_train])
    return np.array(x),np.array(y)

if __name__ == '__main__':
    data_close = ts.get_k_data('000001',start='2017-01-01')['close']
    data_close = data_close.astype('float32').values
    plt.plot(data_close)
    plt.savefig('data.png',format='png',dpi=200)
    plt.close()

    max_value = np.max(data_close)
    min_value = np.min(data_close)
    data_close = (data_close - min_value) / (max_value - min_value)

    x_dataset, y_dataset = create_dataset(data_close,DAYS_FOR_TRAIN)

    train_size = int(len(x_dataset) * 0.7)
    train_x = x_dataset[:train_size]
    train_y = y_dataset[:train_size]


    train_x = train_x.reshape(-1, 1, DAYS_FOR_TRAIN)
    train_y = train_y.reshape(-1, 1, 1)

    train_x = torch.from_numpy(train_x)
    train_y = torch.from_numpy(train_y)

    model = LSTM_Regression(DAYS_FOR_TRAIN, 8, output_size=1, num_layers=2)

    train_loss = []
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-2, betas=(0.9, 0.999),eps=1e-08, weight_decay=0)

    t0  = time.time()
    for i in range(200):
        out = model(train_x)
        loss = loss_function(out,train_y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        train_loss.append(loss.item())

        with open('log.txt', 'a+') as f:
            f.write('{} - {}\n'.format(i + 1, loss.item()))
        if (i + 1) % 1 == 0:
            print('Epoch: {}, Loss:{:.5f}'.format(i + 1, loss.item()))


# 画loss曲线
    plt.figure()
    plt.plot(train_loss, 'b', label='loss')
    plt.title("Train_Loss_Curve")
    plt.ylabel('train_loss')
    plt.xlabel('epoch_num')
    plt.savefig('loss.png', format='png', dpi=200)
    plt.close()


    # torch.save(model.state_dict(), 'model_params.pkl')  # 可以保存模型的参数供未来使用
    t1=time.time()
    T=t1-t0
    print('The training time took %.2f'%(T/60)+' mins.')

    tt0=time.asctime(time.localtime(t0))
    tt1=time.asctime(time.localtime(t1))
    print('The starting time was ',tt0)
    print('The finishing time was ',tt1)

    #save model
    torch.save(model.state_dict(), 'lstm.pth')

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
    plt.plot((train_size, train_size), (0, 1), 'g--')  # 分割线 左边是训练数据 右边是测试数据的输出
    plt.legend(loc='best')
    plt.savefig('result.png', format='png', dpi=200)
    plt.close()
