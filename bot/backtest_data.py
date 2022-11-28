class BacktestData:
    def __init__(self, ticker, timeframe, date, open, high, low, close, volume):
        self.ticker = ticker
        self.timeframe = timeframe
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        
    def __init__(self, df):
        pass
        
    def __iter__(self):
        return iter([self.ticker, self.timeframe, self.date, self.open, self.high, self.low, self.close, self.volume])