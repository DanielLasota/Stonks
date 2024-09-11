import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, RadioButtons


class Stonks:
    def __init__(self, asset: str):
        self.ax = None
        self.asset = asset
        self.current_plot_type = 'candle'
        self.current_period = '1mo'
        self.current_interval = '15m'
        self.indicators_width = 0.35
        self.df = self.download_historical_data(asset, self.current_period, self.current_interval)

        if self.df.empty:
            raise ValueError(f"No data fetched for ticker symbol '{self.asset}'. Check the ticker symbol.")

        self.df = self.calculate_indicators(self.df)

    @staticmethod
    def download_historical_data(asset: str, period: str, interval: str) -> pd.DataFrame:
        return yf.download(asset, period=period, interval=interval)

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

        add_plots = [
            mpf.make_addplot(df['SMA'], color='green', label='SMA', width=self.indicators_width),
            mpf.make_addplot(df['Upper_Bollinger_Band'], color='red', linestyle='--', label='Upper Bollinger',
                             width=self.indicators_width),
            mpf.make_addplot(df['Lower_Bollinger_Band'], color='blue', linestyle='--', label='Lower Bollinger',
                             width=self.indicators_width)
        ]

        fig, axlist = mpf.plot(df, type=self.current_plot_type, style='charles', addplot=add_plots, ylabel='Price',
                               volume=False, figsize=(14, 7), returnfig=True)
        self.ax = axlist[0]
        self.ax.set_title(f'{self.asset} Price Chart')
        self.add_widget_box(fig)

    def update_plot(self) -> None:
        self.ax.clear()
        self.ax.set_title(f'{self.asset} Price Chart')

        add_plots_updated = [
            mpf.make_addplot(self.df['SMA'], color='green', label='SMA', width=self.indicators_width, ax=self.ax),
            mpf.make_addplot(self.df['Upper_Bollinger_Band'], color='red', linestyle='--', label='Upper Bollinger',
                             width=self.indicators_width, ax=self.ax),
            mpf.make_addplot(self.df['Lower_Bollinger_Band'], color='blue', linestyle='--', label='Lower Bollinger',
                             width=self.indicators_width, ax=self.ax)
        ]

        mpf.plot(self.df, type=self.current_plot_type, style='charles', addplot=add_plots_updated, ax=self.ax,
                 volume=False)

        plt.draw()

    def add_widget_box(self, fig) -> None:
        ax_radio_plot_type = plt.axes([0.05, 0.85, 0.1, 0.1])
        radio_plot_type = RadioButtons(ax_radio_plot_type, ['candle', 'line', 'ohlc'])
        radio_plot_type.on_clicked(self.change_plot_type)

        ax_radio_period = plt.axes([0.05, 0.6, 0.1, 0.25])
        radio_period = RadioButtons(ax_radio_period, ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], active=2)
        radio_period.on_clicked(self.change_period)

        ax_radio_interval = plt.axes([0.05, 0.3, 0.1, 0.25])
        radio_interval = RadioButtons(ax_radio_interval, ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'], active=3)
        radio_interval.on_clicked(self.change_interval)

        ax_textbox = plt.axes([0.05, 0.10, 0.1, 0.05])
        textbox = TextBox(ax_textbox, 'Input', initial=self.asset)
        textbox.on_submit(self.submit_text)

        plt.show()

    def update_asset_data(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value.strip() if isinstance(value, str) else value)

        if 'asset' in kwargs or 'current_period' in kwargs or 'current_interval' in kwargs:
            self.df = self.download_historical_data(self.asset, self.current_period, self.current_interval)
            self.df = self.calculate_indicators(self.df)

        self.update_plot()

    def change_plot_type(self, label: str) -> None:
        self.update_asset_data(current_plot_type=label)

    def change_period(self, label: str) -> None:
        self.update_asset_data(current_period=label)

    def change_interval(self, label: str) -> None:
        self.update_asset_data(current_interval=label)

    def submit_text(self, text: str) -> None:
        self.update_asset_data(asset=text)

def run_stocks_analysis(asset: str) -> None:
    stock_analysis = Stonks(asset)
    stock_analysis.plot_fetched_data()
