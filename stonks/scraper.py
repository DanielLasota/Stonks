import pandas
import yfinance as yf
import matplotlib.pyplot as plt


def run_stocks_analysis(asset: str) -> None:
    data = yf.download(asset, period='1mo', interval='5m')

    if data.empty:
        print('No data fetched. Check the ticker symbol')
    else:
        data = calculate_indicators(df=data)
        plot_fetched_data(df=data)

def calculate_indicators(df: pandas.DataFrame) -> pandas.DataFrame:
    df['SMA'] = df['Close'].rolling(window=20).mean()

    df['STD'] = df['Close'].rolling(window=20).std()

    df['Upper_Bollinger_Band'] = df['SMA'] + (df['STD'] * 2)
    df['Lower_Bollinger_Band'] = df['SMA'] - (df['STD'] * 2)

    return df

def plot_fetched_data(df: pandas.DataFrame) -> None:
    plt.figure(figsize=(14, 7))
    plt.plot(df['Close'], label='Close Price', color='black')
    plt.plot(df['SMA'], label='SMA', color='green', linewidth=0.8)
    plt.plot(df['Upper_Bollinger_Band'], label='Upper Bollinger Band', color='red', linewidth=0.8)
    plt.plot(df['Lower_Bollinger_Band'], label='Lower Bollinger Band', color='cyan', linewidth=0.8)

    plt.title(f'Some Asset')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend(loc='upper left')
    plt.grid(True)

    plt.show()