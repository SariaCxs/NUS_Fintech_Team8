import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from pyecharts import options as opts
from pyecharts.charts import Kline
import plotly.offline as py
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def init_data(stockcode,startdate,enddate):
    now = datetime.datetime.now()
    if startdate == "" and enddate == "":
        enddate = str(now.date())
        startdate = str((now - relativedelta(months=2)).date())   
    data = pd.read_csv("./data/StockData/" + stockcode + ".csv")
    data = data[(data.Date <= enddate) & (data.Date >= startdate)]
    return data,startdate,enddate

def kline(stockcode,startdate,enddate):
    data,startdate,enddate = init_data(stockcode,startdate,enddate)
    dates = pd.Series.tolist(data["Date"])
    data = data.iloc[:,1:5]
    data = data[["Open","Close","Low","High"]]
    dflist = []
    for i in range(data.shape[0]):
        row = pd.Series.tolist(data.iloc[i,:])
        dflist.append(row)
    #画图
    c = (
    Kline()
    .add_xaxis(dates)
    .add_yaxis(
        "",
        dflist,
        itemstyle_opts=opts.ItemStyleOpts(
            color="#FF6666",
            color0="#99CC66"
        ),
    )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(is_scale=True,
                                name = "Date"),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            name = "Currency in USD",
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        datazoom_opts=[opts.DataZoomOpts(type_="inside")],
        title_opts=opts.TitleOpts(title="Candlestick Chart of "+ stockcode+ " from " + startdate + " to " + enddate),
    ))
    c.render('./templates/echart.html')

def ochl(stockcode,startdate,enddate,col):
    py.init_notebook_mode(connected=False)
    data = init_data(stockcode,startdate,enddate)[0]
    col = col.split(" ")
    if "Volume" in col and len(col) > 1:
        fig = make_subplots(rows=2, cols=1,shared_xaxes = True,vertical_spacing=0.1,x_title = "Date",y_title = "Currency in USD")
        fig.update_layout(title = "Result of "+stockcode+" from "+startdate+" to "+enddate)
        for each_col in col:
            if each_col != "Volume":
                fig.add_trace(go.Scatter(x=data['Date'], y=data[each_col], mode = 'lines', name= each_col), row=1, col=1)
            else:
                fig.add_trace(go.Scatter(x=data['Date'], y=data['Volume'], name='Volume',marker_color = "red"), row=2, col=1)
    elif "Volume" in col and len(col) == 1:
        layout = go.Layout(yaxis=dict(title='Currency in USD'),xaxis = dict(title = "Date"),title = "Result of "+stockcode+" from "+startdate+" to "+enddate)
        fig = go.Figure(layout = layout)
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Volume'], name='Volume',model = 'lines'))
    else:
        layout = go.Layout(yaxis=dict(title='Currency in USD'),xaxis = dict(title = "Date"),title = "Result of "+stockcode+" from "+startdate+" to "+enddate)
        fig = go.Figure(layout = layout)
        for each_col in col:
            fig.add_trace(go.Scatter(x=data["Date"], y=data[each_col], mode='lines', name=each_col))
    jsfig=fig.to_json()
    return jsfig

def plot_inds(stockcode,startdate,enddate,inds):
    py.init_notebook_mode(connected=False)

    if "RSI" in inds and len(inds.split(" ")) == 1:
        layout = go.Layout(yaxis=dict(title='Currency in USD'),xaxis = dict(title = "Date"),title = "Result of "+stockcode+" from "+startdate+" to "+enddate)
        fig = go.Figure(layout = layout)
        RSI(stockcode,startdate,enddate,inds,fig)
    elif "RSI" not in inds:
        layout = go.Layout(yaxis=dict(title='Currency in USD'),xaxis = dict(title = "Date"),title = "Result of "+stockcode+" from "+startdate+" to "+enddate)
        fig = go.Figure(layout = layout)
        inds = inds.split(" ")
        for ind in inds:
            if "EMA" in ind or "SMA" in ind:
                MA(stockcode,startdate,enddate,ind,fig)
            if ind == 'MACD':
                MACD(stockcode,startdate,enddate,fig)
    else:
        fig = make_subplots(rows=2, cols=1,shared_xaxes = True,vertical_spacing=0.1,x_title = "Date",y_title = "Currency in USD")
        fig.update_layout(title = "Result of "+stockcode+" from "+startdate+" to "+enddate)
        inds = inds.split(" ")
        for ind in inds:
            if "EMA" in ind or "SMA" in ind:
                MA(stockcode,startdate,enddate,ind,fig,True)
            if ind == 'MACD':
                MACD(stockcode,startdate,enddate,fig,True)
            if "RSI" in ind:
                RSI(stockcode,startdate,enddate,ind,fig,True)

    jsfig=fig.to_json()
    return jsfig


def MA(stockcode,startdate,enddate,ind,fig,flag = False):
    kind,days = ind.split("-")
    if startdate == "" and enddate == "":
        data = init_data(stockcode,startdate,enddate)[0]
    else:
        startdate = datetime.datetime.strptime(startdate,'%Y-%m-%d')
        if kind == "EMA":
            startdate = startdate - pd.tseries.offsets.BDay(1)
            startdate = str(startdate).split(" ")[0]
            data = init_data(stockcode,startdate,enddate)[0]
            data[kind] = data['Close'].ewm(int(days)).mean().shift()
        elif kind == 'SMA':
            startdate = startdate - pd.tseries.offsets.BDay(int(days))
            startdate = str(startdate).split(" ")[0]
            data = init_data(stockcode,startdate,enddate)[0]
            data[kind] = data['Close'].rolling(int(days)).mean().shift()
    data.dropna(inplace = True)
    if flag == True:
        fig.add_trace(go.Scatter(x=data["Date"], y=data[kind], mode='lines', name=kind + "-" + days),row=1,col=1)
    else:
        fig.add_trace(go.Scatter(x=data["Date"], y=data[kind], mode='lines', name=kind + "-" + days))

def RSI_converter(df,days):
    diff = df['Close'].diff()[1:]
    Up = diff.copy()
    Down = diff.copy()
    Up[Up < 0] = 0
    Down[Down > 0] = 0
    Uprolling = Up.rolling(days).mean()
    Downrolling = Down.abs().rolling(days).mean()
    rs = Uprolling / Downrolling
    rsi = 100 - (100 / (1 + rs))
    return rsi

def RSI(stockcode,startdate,enddate,ind,fig,flag = False):
    days = ind.split("-")[1]
    if startdate == "" and enddate == "":
        data = init_data(stockcode,startdate,enddate)[0]
    else:
        startdate = datetime.datetime.strptime(startdate,'%Y-%m-%d')
        startdate = startdate - pd.tseries.offsets.BDay(int(days))
        startdate = str(startdate).split(" ")[0]
        data = init_data(stockcode,startdate,enddate)[0]
    data["rsi"] = RSI_converter(data,int(days))
    data.dropna(inplace = True)
    if flag == True:
        fig.add_trace(go.Scatter(x=data["Date"], y=data["rsi"], mode='lines', name="RSI" + "-" + days),row=2,col=1)
    else:
        fig.add_trace(go.Scatter(x=data["Date"], y=data["rsi"], mode='lines', name="RSI" + "-" + days))

def MACD(stockcode,startdate,enddate,fig,flag = False):
    data = init_data(stockcode,startdate,enddate)[0]
    E12 = pd.Series(data['Close'].ewm(span=12, min_periods=12).mean())
    E26 = pd.Series(data['Close'].ewm(span=26, min_periods=26).mean())
    MACD = pd.Series(E12 - E26)
    if flag == True:
        fig.add_trace(go.Scatter(x=data["Date"], y=MACD, mode='lines', name='MACD'),row=1,col=1)
    else:
        fig.add_trace(go.Scatter(x=data["Date"], y=MACD, mode='lines', name='MACD'))
