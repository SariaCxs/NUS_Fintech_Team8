## User Guideline
---
[Stock Funnel](http://101.34.65.50:5007/) is a simple, free and no login stock picking assistant based on `Python` , `Flask`  and `Bootstrap` . It uses some simple financial indicators to determine your type of investment and can find the best stock for you from thousands of stocks by K-means algorithm. 
You can also use simple filtering indicators to get the best stocks for you. And the the visualization results of stocks' historical information and the changes of their related indicators also can be easily access in Stock Funnel.
In this article, we will briefly introduce you to the modules of Stock Funnel.

### Module Catalog
---
- Survey
- Recommendation
- Stock Search
- Indicator Search
### Survey

---

We assume you are beginners and don’t know what kind of stock to choose from thousands of them.  

To help you quickly find stocks that are suitable for you, we design this part as a customized stock funnel.

In this part, you can have a quick and simple test of your investment type by filling the survey form. The form includes three questions, what is your goal for investment, what is the biggest loss you can afford and your cycle for holding a stock. 

After you submit, the website will show you what your investment type is( `cautious`, `steady`, `active`, `aggressive` ) and list stocks that meet your type. Basic information like high, low, open and close is shown. For each stock, you can click on the code name to view details of the history data. Further, you can select the sector checkbox to choose the sector you are interested in.



### Recommendation
---
We assume you have experience in stock market. Sometimes you have want to select stocks that have special signal for trading but it may be hard to find them just by viewing the figure of history data.

To help you quickly get stocks that have particular signal you expect, we design this part for you.

In this part, you can first select the indicators and then choose one of the condition for the indicator.  We provide you with six different indicators( `MACD`, `KDJ`, `BIAS`, `BOLL`, `DMA`, `RSI` ) and conditions like `gold cross`, `death cross`, `overbought` and `oversold`. After clicking on the submit button,stocks that meet your condition is listed in the table below. 

But just filtering them out is not enough, you may want to know their performance, thus we design an **Machine Learning based ranker** to rank stocks you select from good to  poor.  The higher it rank is, the higher possibility that it can have excess earnings.  After you click on the rank button, you can see a brief introduction of our ranking strategy and the ranking result of those stocks together with their close price, change and total yield. 



### Stock Search

---
By entering the following information, you can easily get a visualization of the historical information changes for the stock you are interested in. This historical information includes `Open`, `High`, `Low`, `Close`, `Adj Close` and `Volume`.
##### 1. Symbol

You need to enter the Symbol of the stock in this field to help the system retrieve the corresponding data in the database, such as `AAPL` or `TSLA`. Note: If you enter a null value or a non-existent Symbol here, the system will return a 404 page or nothing at all.

##### 2. Date Range

Includes both Start Date and End Date information, in the format as `YYYY-MM-DD`.

Note: Entering the wrong date format will cause the system to return an error. However, you can enter nothing in these two fields and the system will assume that the time range you want to query is the last two months.

##### 3. Data

Here, you must specify the information you want to search for. As described at the beginning of this section, there are six types of information available to you. You can search for one or more messages at the same time. If you want to search for more than one message at the same time, please separate the names of these messages with a space.

Also, please note that everything in the system is **case-sensitive**, which means that entering data in the wrong case will give different or incorrect results.

The search module also provides the you with the ability to generate a candlestick chart, which only requires you to fill in the other information correctly and fill in `CandleStick` in the this row.

**Good**

> Open High Low

> Open

> Low Volume

**Bad**

> Open-HighLow

> open

> Open  High



### Indicator Search
---

The use and functional structure of this module is very similar to the previous one. The difference is that here you can query changes in more complex indicators like Stock Moving Average (both `EMA` and `SMA`), `RSI` and `MACD`.

If you are confused about these indicators, please refer to this tutorial: https://www.investopedia.com/technical-analysis-4689657

Similar to the "Stock Search" module, you should fill in the Symbol, Start Date and End Date information in the same format here, and if you fill in some information incorrectly, the result will be similar to the previous module (for example, if you don't fill in the date range, the system will default to the last two months of data you want to query).

The only difference is that you must fill in this field with the indicator you want to query, including `RSI`, `EMA`, `SMA` and `MACD`. note: when you query RSI and any of the moving averages, you must specify a specific corresponding date and append the date to the indicator name with a "-".

Similarly, you can query one or more indicators at the same time, just separate the indicators with a space when querying multiple indicators.

##### Format Example for "Indicators"

**Good**

> EMA-7 SMA-5 MACD

> MACD

> EMA-7

**Bad**

> EMA-7SMA-5

> EMA SMA

> MACD-7



