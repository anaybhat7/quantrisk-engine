import pandas as pd
import numpy as np
from typing import Optional

class DataPreprocessor:
    """
    Cleans and transforms raw price data into risk-ready returns.
    """

    @staticmethod
    def clean_data(df: pd.DataFrame, method: str = 'dropna') -> pd.DataFrame:
        """
        Handles missing values. 
        ORIE 5270 Tip: Document why you chose 'dropna' vs 'fill' in your README.
        """
        if method == 'dropna':
            return df.dropna()
        elif method == 'ffill':
            return df.fillna(method='ffill').dropna()
        else:
            raise ValueError("Method must be 'dropna' or 'ffill'")

    @staticmethod
    def calculate_log_returns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts adjusted prices to log returns.
        """
        # Log returns are preferred for risk engines due to normality assumptions
        returns = np.log(df / df.shift(1))
        return returns.dropna()

    def get_risk_ready_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        A pipeline method to clean and transform in one go.
        """
        cleaned = self.clean_data(df, method='ffill')
        returns = self.calculate_log_returns(cleaned)
        return returns