import pandas as pd
class Filter():
    def __init__(self):
        '''
        filter stock by indicators and industries
        '''
        self.industries = ['Financial Services','Energy Healthcare','Technology','Utilities','Industrials','Basic Materials',
            'Communication Services','Consumer Cyclical','Consumer Defensive']
        self.indicator_pool = {'kdj':['kdj_golden_cross', 'kdj_death_cross', 'kdj_oversold', 'kdj_overbought'], 'bias':['bias_golden_cross', 'bias_death_cross'],
        'macd':['macd_golden_cross', 'macd_death_cross'],'dma':[ 'dma_golden_cross', 'dma_death_cross'],
        'boll':['boll_high_break', 'boll_mid_break', 'boll_low_break'],
        'rsi':['rsi_golden_cross', 'rsi_death_cross', 'rsi_oversold', 'rsi_overbought']}
        self.data = pd.read_csv('./data/daily_data.csv')
        self.stock_info = pd.read_csv('./data/Runes_clean.csv')

    def filt(self,indicators,sector=None):
        '''
        Args:
        data (dic): {stock_code:data_frame}
        indicators (dic): {indicator:requirement} {'':}

        Returns:
        stocks: the code of stock
        '''
        out_indicators = []
        if sector is not None:
            result = self.data[self.data['sector'] == sector]
            out_indicators.append({'name':'sector','value':sector})
        else:
            result = self.data.copy()
        if len(indicators)>0:
            for ind in indicators:
                col = indicators[ind]
                col_name = self.indicator_pool[ind][int(col)]
                result = result[result[col_name] == 1]
                out_indicators.append({'name':ind,'value':col_name})
        code = result['code'].values

        return code,out_indicators



