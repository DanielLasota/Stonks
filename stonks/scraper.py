import yfinance as yf


def run_stocks_analysis(asset: str) -> None:
    data = yf.download(asset, period='1mo', interval='5m')

    if data.empty:
        print('No data fetched. Check the ticker symbol')
    else:
        print(data)
