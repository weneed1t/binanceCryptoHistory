import argparse
import json
import logging
import os
from datetime import datetime

from binance.client import Client
from binance.exceptions import BinanceAPIException
from dateutil import parser

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BinanceDataFetcher:
    def __init__(self):
        self.client = Client()

    def map_resolution(self, resolution):
        resolution_map = {
            "15m": Client.KLINE_INTERVAL_15MINUTE,
            "30m": Client.KLINE_INTERVAL_30MINUTE,
            "1h": Client.KLINE_INTERVAL_1HOUR,
            "4h": Client.KLINE_INTERVAL_4HOUR,
            "12h": Client.KLINE_INTERVAL_12HOUR,
            "1d": Client.KLINE_INTERVAL_1DAY,
            "1w": Client.KLINE_INTERVAL_1WEEK,
        }
        return resolution_map.get(resolution, None)

    def parse_date(self, date_str):
        # Try different date formats
        formats = ["%Y:%m:%d", "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        # If none of the formats work, try dateutil parser as fallback
        try:
            return parser.parse(date_str)
        except ValueError as e:
            logger.error(f"Could not parse date: {date_str}")
            raise ValueError(f"Invalid date format: {date_str}") from e

    def fetch_data(self, asset, resolution, start_date, end_date):
        binance_interval = self.map_resolution(resolution)
        if not binance_interval:
            raise ValueError(f"Unsupported resolution: {resolution}")

        # Parse dates with explicit format handling
        start_dt = self.parse_date(start_date)
        end_dt = self.parse_date(end_date)

        start_ts = int(start_dt.timestamp() * 1000)
        end_ts = int(end_dt.timestamp() * 1000)

        klines = []
        while start_ts < end_ts:
            try:
                batch = self.client.get_klines(
                    symbol=asset,
                    interval=binance_interval,
                    startTime=start_ts,
                    endTime=end_ts,
                    limit=1000,
                )
                if not batch:
                    break
                logger.info(f"Fetched {len(batch)} records for {asset}")

                klines.extend(batch)
                start_ts = batch[-1][0] + 1
            except BinanceAPIException as e:
                logger.error(f"API error fetching data for {asset}: {e}")
                break

        return klines

    def process_klines(self, klines):
        processed = []
        for k in klines:
            timestamp = k[0] / 1000
            dt = datetime.utcfromtimestamp(timestamp)
            processed.append(
                {
                    "open_time": k[0],
                    "open": k[1],
                    "high": k[2],
                    "low": k[3],
                    "close": k[4],
                    "volume": k[5],
                    "close_time": k[6],
                    "quote_asset_volume": k[7],
                    "number_of_trades": k[8],
                    "taker_buy_base_volume": k[9],
                    "taker_buy_quote_volume": k[10],
                    "ignore": k[11],
                    "day_of_month": dt.day,
                    "hour_of_day": dt.hour,
                    "day_of_year": dt.timetuple().tm_yday,
                }
            )
        return processed


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Fetch cryptocurrency historical data from Binance"
    )

    parser.add_argument(
        "--assets",
        nargs="+",
        default=["BTC", "ETH"],
        help="List of cryptocurrency symbols (e.g., BTC ETH BNB)",
    )

    parser.add_argument(
        "--resolution",
        default="1h",
        choices=["15m", "30m", "1h", "4h", "12h", "1d", "1w"],
        help="Time resolution for the data",
    )

    parser.add_argument(
        "--start-date", default="2020-01-01", help="Start date in format YYYY-MM-DD"
    )

    parser.add_argument(
        "--end-date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="End date in format YYYY-MM-DD",
    )

    parser.add_argument(
        "--output-folder", default="crypto_data", help="Output folder for JSON files"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    fetcher = BinanceDataFetcher()
    os.makedirs(args.output_folder, exist_ok=True)

    for asset in args.assets:
        all_data = {}
        logger.info(f"Fetching data for {asset}")
        try:
            # Add 'USDT' if not present (assuming trading pairs against USDT)
            asset_symbol = asset if "USDT" in asset else f"{asset}USDT"
            klines = fetcher.fetch_data(
                asset_symbol, args.resolution, args.start_date, args.end_date
            )
            processed_data = fetcher.process_klines(klines)
            all_data[asset] = processed_data
            logger.info(f"Total fetched {len(processed_data)} records for {asset}")

            # Create filename with asset and resolution
            file_name = f"{asset}_{args.resolution}.json"
            file_path = os.path.join(args.output_folder, file_name)

            with open(file_path, "w") as f:
                json.dump(all_data, f, indent=4)
                logger.info(f"Data saved to {file_path}")

        except Exception as e:
            logger.error(f"Failed to fetch data for {asset}: {e}")


if __name__ == "__main__":
    main()
