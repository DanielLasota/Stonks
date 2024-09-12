# Market Data Scraper and Analysis Tool

This script is designed to scrape market data from the Yahoo Finance API, calculate base indicators, and visualize the results using various plots

## Installation

```bash
pip install stonks
```

## Usage

import the `run_stonks_analysis` function from the `stonks` module and run the script:

```python
from stonks import run_stonks_analysis

if __name__ == '__main__':
    run_stonks_analysis()
```

![Moving Average Example](https://github.com/user-attachments/assets/197e4219-a829-4aae-a785-52a60020a8ea)

![RSI Indicator Example](https://github.com/user-attachments/assets/a8252ae8-071b-48b7-ab23-fd1f555d3d5a)

![Candlestick Chart](https://github.com/user-attachments/assets/16833b84-a5ed-4d83-8ef5-ea1c5564d0a1)

# Appendix
1. Yahoo decommissioned their historical data API
2. You should use 'EURUSD=X' instead of 'EURUSD'
3. Not every Period, Interval will fetch data (api limitations and/or decomission)
4. 
