import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from pyecharts import options as opts
from pyecharts.charts import Kline
import plotly
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

# def GetDemo(stockcode,startdate,enddate,col):
#     data,startdate,enddate = init_data(stockcode,startdate,enddate)
#     data["Date"]= pd.to_datetime(data["Date"])
#     data = data[(data.Date <= enddate) & (data.Date >= startdate)].set_index("Date")
        
#     col = col.split(" ")
#     #选中用户选择的列
#     data = data.filter(col)

#     return data

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
                fig.add_trace(go.Scatter(x=data['Date'], y=data['Volume'], name='Volume'), row=2, col=1)
    else:
        layout = go.Layout(yaxis=dict(title='Currency in USD'),xaxis = dict(title = "Date"),title = "Result of "+stockcode+" from "+startdate+" to "+enddate)
        fig = go.Figure(layout = layout)
        for each_col in col:
            fig.add_trace(go.Scatter(x=data["Date"], y=data[each_col], mode='lines', name=each_col))
    jsfig=fig.to_json()
    return jsfig
    
