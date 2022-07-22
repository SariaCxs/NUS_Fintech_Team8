# NUS_Fintech_Team8
## 若要在服务器进行配置，仍需要独立下载以下库：
- tushare
- torch
- matplotlib
- flask

### V1.3
- 在推荐与筛选页面的股票表格中加入了点击股票代码查看近2个月数据的功能
- 加入了一个before_request函数，确保fetch_data()可以执行
- 优化了搜索功能，完善了一点逻辑判断
- 对样式做了一些小的调整