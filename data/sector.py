import pandas as pd

sector = ['']
df = pd.read_excel('sectors.xlsx',sheet_name=None)
stock_info = pd.read_csv('daily_data.csv')
stock_code = stock_info['code']
stock_sector = []
for code in stock_code:
    sector = None
    print(code)
    for sec in df.keys():
        sym = df[sec]['Symbol'].values
        if code in sym:
            sector = sec
            break
    stock_sector.append(sector)

stock_info['sector'] = stock_sector
stock_info.to_csv('daily_data.csv',encoding='utf-8',index=False)