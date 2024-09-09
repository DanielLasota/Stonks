import pandas
import pandas as pd
import yfinance as yf
import mplfinance as mpf


def run_stocks_analysis(asset: str) -> None:
    df = download_historical_data(asset=asset)

    if df.empty:
        print('No data fetched. Check the ticker symbol')
    else:
        print(df)
        print(df.columns)
        df = calculate_indicators(df=df)
        plot_fetched_data(df=df)

def download_historical_data(asset: str) -> pandas.DataFrame:
    data = yf.download(asset, period='1mo', interval='1h')

    return data

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df['SMA'] = df['Close'].rolling(window=20).mean()

    df['STD'] = df['Close'].rolling(window=20).std()
    df['Upper_Bollinger_Band'] = df['SMA'] + (df['STD'] * 2)
    df['Lower_Bollinger_Band'] = df['SMA'] - (df['STD'] * 2)

    return df

def plot_fetched_data(df: pd.DataFrame) -> None:
    df.index.name = 'Date'

    indicators_width = 0.2

    add_plots = [
        mpf.make_addplot(df['SMA'], color='green', label='SMA', width=indicators_width),
        mpf.make_addplot(df['Upper_Bollinger_Band'], color='red', linestyle='--', label='Upper Bollinger',
                         width=indicators_width),
        mpf.make_addplot(df['Lower_Bollinger_Band'], color='blue', linestyle='--', label='Lower Bollinger',
                         width=indicators_width)
    ]

    mpf.plot(df, type='candle', style='charles', addplot=add_plots,
             title=f'px', ylabel='Price',
             volume=False, figsize=(14, 7), show_nontrading=True)
