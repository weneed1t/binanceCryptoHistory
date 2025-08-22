# binanceCryptoHistory
# 📊 Binance Historical Crypto Data Fetcher

A robust Python script designed to fetch, process, and store historical cryptocurrency market data from Binance exchange with professional-grade reliability and comprehensive data formatting.

## 🚀 Overview

This tool automatically retrieves historical OHLCV (Open, High, Low, Close, Volume) market data for specified cryptocurrencies from Binance's API. It processes the raw data into structured JSON format with additional temporal features, making it ideal for:

- **Quantitative analysis** and algorithmic trading research
- **Machine learning** datasets for price prediction
- **Technical analysis** and backtesting strategies
- **Academic research** in cryptocurrency markets
- **Data visualization** projects

## ✨ Key Features

- **📈 Multi-Asset Support**: Fetch data for multiple cryptocurrencies simultaneously
- **⏰ Flexible Time Resolutions**: Support for 15min, 30min, 1h, 4h, 12h, daily, and weekly intervals
- **📅 Custom Date Ranges**: Specify exact start and end dates for data retrieval
- **🔍 Comprehensive Data**: OHLCV + additional market metrics (trades, taker volumes, etc.)
- **⏰ Temporal Features**: Automatic extraction of day/month/hour/year components from timestamps
- **💾 Organized Storage**: Clean JSON output with proper file naming conventions
- **📋 Detailed Logging**: Comprehensive progress tracking and error reporting
- **⚡ Efficient Pagination**: Handles large date ranges with automatic API pagination

## 📋 Data Output Structure

Each JSON file contains complete market data with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `open_time` | int | Opening timestamp (milliseconds) |
| `open` | string | Opening price |
| `high` | string | Highest price in interval |
| `low` | string | Lowest price in interval |
| `close` | string | Closing price |
| `volume` | string | Base asset volume |
| `close_time` | int | Closing timestamp (milliseconds) |
| `quote_asset_volume` | string | Quote asset volume (usually USDT) |
| `number_of_trades` | int | Number of trades in interval |
| `taker_buy_base_volume` | string | Taker buy base asset volume |
| `taker_buy_quote_volume` | string | Taker buy quote asset volume |
| `ignore` | string | Ignore field (always 0) |
| `day_of_month` | int | Calendar day (1-31) |
| `hour_of_day` | int | Hour of day (0-23) |
| `day_of_year` | int | Day of year (1-366) |

## 🛠 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/binance-historical-data-fetcher.git
cd binance-historical-data-fetcher
