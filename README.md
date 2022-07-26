# NUS_Fintech_Team8
## 若要在服务器进行配置，仍需要独立下载以下库：
- tushare
- torch
- flask
- pyecharts
- plotly
## 改动日志
### V1.3
- 在推荐与筛选页面的股票表格中加入了点击股票代码查看近2个月数据的功能
- 加入了一个before_request函数，确保fetch_data()可以执行
- 优化了搜索功能，完善了一点逻辑判断
- 对样式做了一些小的调整

### V1.4
- 调整可视化功能，加入使用pyecharts生成可交互式k线图的功能（因pyechart的渲染机制，目前采用生成文件的形式将图片推送至前端，这导致前端同时只能存储一张图。因此，此功能目前只能保证支持演示、测试时的场景）

### V1.5

- 实现指标筛选功能，预先得到每只股票该指标的数据存储于daily_data.csv 中，初始化的时候加载该表格绝对股票进行筛选。

### V1.6
- 改由plotly代替matplotlib完成K线图以外的可视化
- 加入指标搜索功能，可以查询某股票某时间段内的RSI、EMA、SMA和MACD指标，其中MACD指标的计算目前仍有问题，有待进一步修正

### V1.7

- 整理股票sector，再用户推荐以及指标筛选下增加sector筛选的选项

### V1.8

- 加入Kmeans Sorter， 按照var以及平均收益进行分类，按照到中心点的距离由小到大排序（与大盘的近似度）

### V1.9

- 更改股票分类的参数
- 引入rank_result.html 用于展示排序方法以及排序结果