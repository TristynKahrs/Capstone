from config import Configuration as cf
import pandas as pd

# class IStrategy(ABC):
class IStrategy:
    def __init__(self, config: cf):
        self.config = config
        super().__init__(config)
        raise NotImplementedError("Should implement __init__()!")
    
    
    def populate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        return data
    
    def populate_entry_trend(self, data: pd.DataFrame) -> pd.DataFrame:
        return data
    
    def populate_exit_trend(self, data: pd.DataFrame) -> pd.DataFrame:
        return data
    
    # @abstractmethod
    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Should implement execute()!")
    
    def backtest(self):
        raise NotImplementedError("Should implement backtest()!")
    
    def exit(self):
        raise NotImplementedError("Should implement exit()!")