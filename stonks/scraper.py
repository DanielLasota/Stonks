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
        self.indicators_width = 0.2
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

        add_plots = [
            mpf.make_addplot(df['SMA'], color='green', label='SMA', width=self.indicators_width),
            mpf.make_addplot(df['Upper_Bollinger_Band'], color='red', linestyle='--', label='Upper Bollinger',
                             width=self.indicators_width),
            mpf.make_addplot(df['Lower_Bollinger_Band'], color='blue', linestyle='--', label='Lower Bollinger',
                             width=self.indicators_width)
        ]

        fig, axlist = mpf.plot(df, type=self.current_plot_type, style='charles', addplot=add_plots,
                               title=f'{self.asset} Px Chart', ylabel='Price', volume=False, figsize=(14, 7),
                               returnfig=True)
        self.ax = axlist[0]
        self.add_widget_box(fig)

    def update_plot(self) -> None:
        self.ax.clear()
        self.ax.set_title(f'{self.asset} Px Chart')

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
        ax_radio = plt.axes([0.05, 0.7, 0.1, 0.15])
        radio = RadioButtons(ax_radio, ['candle', 'line', 'ohlc'])
        radio.on_clicked(self.change_plot_type)

        ax_textbox = plt.axes([0.05, 0.45, 0.1, 0.05])
        textbox = TextBox(ax_textbox, 'Input', initial=self.asset)
        textbox.on_submit(self.submit_text)

        plt.show()

    def change_plot_type(self, label: str) -> None:
        self.current_plot_type = label
        self.update_plot()

    def submit_text(self, text: str) -> None:
        new_asset = text.strip()
        self.asset = new_asset
        self.df = self.download_historical_data(new_asset)
        self.df = self.calculate_indicators(self.df)
        self.update_plot()


def run_stocks_analysis(asset: str) -> None:
    stock_analysis = Stonks(asset)
    stock_analysis.plot_fetched_data()
