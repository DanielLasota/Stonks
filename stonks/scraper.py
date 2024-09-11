import pandas as pd
import yfinance as yf
import mplfinance as mpf


class Stonks:
    def __init__(self, asset: str):
        self.asset = asset

        self.df = self.download_historical_data(asset)

        if self.df.empty:
            raise ValueError(f"No data fetched for ticker symbol '{self.asset}'. Check the ticker symbol.")

        self.df = self.calculate_indicators(self.df)

    @staticmethod
    def download_historical_data(asset: str) -> pd.DataFrame:
        return yf.download(asset, period='1mo', interval='1h')

    @staticmethod
    def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['SMA'] = df['Close'].rolling(window=20).mean()
        df['STD'] = df['Close'].rolling(window=20).std().round(3)
        df['Upper_Bollinger_Band'] = df['SMA'] + (df['STD'] * 2)
        df['Lower_Bollinger_Band'] = df['SMA'] - (df['STD'] * 2)

        return df

    def plot_fetched_data(self) -> None:
        df = self.df.copy()
        df.index.name = 'Date'

        indicators_width = 0.2

        add_plots = [
            mpf.make_addplot(df['SMA'], color='green', label='SMA', width=indicators_width),
            mpf.make_addplot(df['Upper_Bollinger_Band'], color='red', linestyle='--', label='Upper Bollinger',
                             width=indicators_width),
            mpf.make_addplot(df['Lower_Bollinger_Band'], color='blue', linestyle='--', label='Lower Bollinger',
                             width=indicators_width)
        ]

        mpf.plot(df, type='candle', style='charles', addplot=add_plots, title=f'{self.asset} Px Chart', ylabel='Price',
                 volume=False, figsize=(14, 7), show_nontrading=True)


def run_stocks_analysis(asset: str) -> None:
    stock_analysis = Stonks(asset)
    stock_analysis.plot_fetched_data()
