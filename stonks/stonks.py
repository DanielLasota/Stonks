import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, RadioButtons


class DataFetcher:
    def __init__(self, asset: str, period: str = '1mo', interval: str = '15m'):
        self.asset = asset
        self.period = period
        self.interval = interval

    def fetch_data(self) -> pd.DataFrame:
        try:
            data = yf.download(self.asset, period=self.period, interval=self.interval)
            if data.empty:
                raise ValueError(f"No data fetched for ticker symbol '{self.asset}'. Check the ticker symbol.")
            return data
        except Exception as e:
            raise ValueError(f"Error fetching data: {str(e)}")


class DataManipulator:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def add_indicators(self) -> pd.DataFrame:
        df_with_bollinger = self.add_bollinger_bands(df=self.df)
        return df_with_bollinger

    @staticmethod
    def add_bollinger_bands(df: pd.DataFrame) -> pd.DataFrame:
        df['SMA'] = df['Close'].rolling(window=20).mean()
        df['STD'] = df['Close'].rolling(window=20).std()
        df['Upper_Bollinger_Band'] = df['SMA'] + (df['STD'] * 2)
        df['Lower_Bollinger_Band'] = df['SMA'] - (df['STD'] * 2)
        return df


class ChartRenderer:

    def __init__(
            self,
            asset: str,
            df: pd.DataFrame
    ):
        self.asset = asset
        self.df = df
        self.current_plot_type = 'candle'
        self.current_period = '1mo'
        self.current_interval = '15m'
        self.indicators_width = 0.35
        self.ax = None
        self.fig = None
        self.error_displayed = False

    def plot_data(self) -> None:
        df = self.df.copy()
        df.index.name = 'Date'

        add_plots = [
            mpf.make_addplot(df['SMA'], color='green', label='SMA', width=self.indicators_width),
            mpf.make_addplot(df['Upper_Bollinger_Band'], color='red', linestyle='--', label='Upper Bollinger',
                             width=self.indicators_width),
            mpf.make_addplot(df['Lower_Bollinger_Band'], color='blue', linestyle='--', label='Lower Bollinger',
                             width=self.indicators_width)
        ]

        self.fig, axlist = mpf.plot(df, type=self.current_plot_type, style='charles', addplot=add_plots, ylabel='Price',
                                    volume=False, figsize=(14, 7), returnfig=True)
        self.ax = axlist[0]
        self.ax.set_title(f'{self.asset} Price Chart')

        self.add_widget_box(self.fig)
        plt.show()

    def update_plot(self, error_message: str = "") -> None:
        self.ax.clear()
        self.ax.set_title(f'{self.asset} Price Chart')

        if error_message:
            self.ax.text(0.5, 0.02, error_message, horizontalalignment='center', verticalalignment='center',
                         transform=self.ax.transAxes, color='red', fontsize=12)
            self.error_displayed = True
        else:
            self.error_displayed = False
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
        ax_radio_plot_type = plt.axes([0.05, 0.8, 0.1, 0.1])
        plt.text(0.05, 0.90, "Plot Type", transform=fig.transFigure)
        radio_plot_type = RadioButtons(ax_radio_plot_type, ['candle', 'line', 'ohlc'])
        radio_plot_type.on_clicked(self.change_plot_type)

        ax_radio_period = plt.axes([0.05, 0.50, 0.1, 0.25])
        plt.text(0.05, 0.75, "Period", transform=fig.transFigure)
        radio_period = RadioButtons(ax_radio_period,
                                    ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                                    active=2)
        radio_period.on_clicked(self.change_period)

        ax_radio_interval = plt.axes([0.05, 0.20, 0.1, 0.25])
        plt.text(0.05, 0.45, "Interval", transform=fig.transFigure)
        radio_interval = RadioButtons(ax_radio_interval,
                                      ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk',
                                       '1mo', '3mo'], active=3)
        radio_interval.on_clicked(self.change_interval)


        ax_textbox = plt.axes([0.05, 0.10, 0.1, 0.05])
        textbox = TextBox(ax_textbox, 'Input', initial=self.asset)
        textbox.on_submit(self.submit_text)

        plt.show()

    def change_plot_type(self, label: str) -> None:
        self.current_plot_type = label
        self.update_plot()

    def change_period(self, label: str) -> None:
        self.current_period = label
        self.update_asset_data()

    def change_interval(self, label: str) -> None:
        self.current_interval = label
        self.update_asset_data()

    def submit_text(self, text: str) -> None:
        self.asset = text
        self.update_asset_data()

    def update_asset_data(self) -> None:
        try:
            fetcher = DataFetcher(self.asset, self.current_period, self.current_interval)
            self.df = fetcher.fetch_data()
            manipulator = DataManipulator(self.df)
            self.df = manipulator.add_indicators()
            self.update_plot()
        except ValueError as e:
            self.update_plot(error_message=str(e))


class Stonks:
    def __init__(self):
        self.asset = 'EURUSD=X'
        self.data_fetcher = DataFetcher(self.asset)
        self.data_frame = self.data_fetcher.fetch_data()
        self.data_manipulator = DataManipulator(self.data_frame)
        self.data_frame = self.data_manipulator.add_indicators()
        self.chart_renderer = ChartRenderer(self.asset, self.data_frame)

    def run(self) -> None:
        self.chart_renderer.plot_data()


def run_stonks_analysis() -> None:
    stonks = Stonks()
    stonks.run()
