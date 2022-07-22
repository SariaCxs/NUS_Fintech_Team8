import torch
from torch import nn

class LSTM_Regression(nn.Module):
    def __init__(self,input_size,hidden_size,output_size=1,num_layers=2):
        super(LSTM_Regression, self).__init__()
        self.lstm = nn.LSTM(input_size,hidden_size,num_layers)
        self.fc = nn.Linear(hidden_size,output_size)

    def forward(self,x):
        out,_ = self.lstm(x)
        s,b,h = out.shape
        out = out.view(s*b,h)
        out = self.fc(out)
        out = out.view(s,b,-1)
        return out

