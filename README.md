# Charti

`charti.py` is a Python script that allows users to download historical cryptocurrency price and volume charts from various exchanges using the `ccxt` library. The script also supports listing all available exchanges and trading pairs.

## Features
- **List Supported Exchanges**: View all exchanges available through the `ccxt` library.
- **List Trading Pairs**: Query all trading pairs available on a specific exchange.
- **Download Historical Data**: Fetch historical OHLCV (Open, High, Low, Close, Volume) data for a specific trading pair.
- **Flexible Timeframes**: Supports multiple time intervals, such as `1d`, `1h`, `15m`, `5m`, and `1m`.
- **JSON Output**: Saves downloaded chart data in a structured JSON file.

## Prerequisites
Ensure you have the following installed:

- Python 3.7+
- `pip` (Python package manager)

Install the required libraries:

```bash
pip install ccxt pandas
```

## Usage

### 1. Listing Exchanges
To list all supported exchanges:

```bash
python charti.py --list-exchanges
```

### 2. Listing Trading Pairs
To list all available trading pairs on a specific exchange (e.g., OKX):

```bash
python charti.py --list-pairs okx
```

### 3. Downloading Historical Data
To download historical price and volume data for a specific trading pair:

```bash
python charti.py --download --pair BTC/USDT --exchange okx --start-date 2024-10-31 --end-date 2024-12-31 --intervals 1d 1h 15m 5m 1m --output-file btcusdt.json
```

#### Required Arguments for `--download`:
- `--pair`: The trading pair (e.g., `BTC/USDT`).
- `--exchange`: The exchange name (e.g., `okx`).
- `--start-date`: The start date for data collection in `YYYY-MM-DD` format.
- `--end-date`: The end date for data collection in `YYYY-MM-DD` format.
- `--intervals`: The time intervals for data (e.g., `1d`, `1h`, `15m`). Accepts multiple intervals.
- `--output-file`: The name of the JSON file to save the data (default: `chart_data.json`).

## Output
The script saves the downloaded data in a JSON file. The data is organized by intervals, for example:

```json
{
    "1d": [
        {"Date": "2024-01-01 00:00:00", "Open": 42297, "High": 44254, "Low": 42182, "Close": 44220, "Volume": 1200},
        ...
    ],
    "1h": [
        {"Date": "2024-01-01 00:00:00", "Open": 42274, "High": 42363, "Low": 42080, "Close": 42297, "Volume": 100},
        ...
    ]
}
```

## Examples

### Example 1: Listing Exchanges
```bash
python charti.py --list-exchanges
```
**Output:**
```
Supported Exchanges:
- binance
- coinbasepro
- kraken
- bitfinex
...
```

### Example 2: Listing Trading Pairs
```bash
python charti.py --list-pairs okx
```
**Output:**
```
Trading Pairs on okx:
- BTC/USDT
- ETH/USDT
- ADA/USDT
...
```

### Example 3: Downloading BTC/USDT Data
```bash
python charti.py --download --pair BTC/USDT --exchange okx --start-date 2024-01-01 --end-date 2023-12-31 --intervals 1d 1h --output-file btcusdt.json
```
**Output:**
The file `btcusdt.json` will contain the historical data for the specified pair and intervals.

- **Exchange or Pair Not Found**:
  Double-check the exchange name and pair using `--list-exchanges` and `--list-pairs`.

## Contributing
Feel free to contribute to this project by submitting issues or pull requests on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
