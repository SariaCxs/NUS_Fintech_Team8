
class Filter():
    def __init__(self):
        self.indicator_pool = {'WR':['','',''],'MA':['','','']}

    def filt(self,data,indicators):
        '''
        Args:
        data (dic): {stock_code:data_frame}
        indicators (dic): {indicator:requirement} {'':}

        Returns:
        stocks: the code of stock
        '''
        result = data.copy()
        for ind in indicators:
            col = indicators[ind]
            result = result[self.indicator_pool[col] == 1]
        return result['code']



