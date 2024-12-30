import ccxt
import pandas as pd
import json
import argparse
from datetime import datetime

def list_exchanges():
    """Lists all exchanges supported by CCXT."""
    exchanges = ccxt.exchanges
    print("Supported Exchanges:")
    for exchange in exchanges:
        print(f"- {exchange}")

def list_pairs(exchange_name):
    """Lists all trading pairs available on the specified exchange."""
    try:
        exchange = getattr(ccxt, exchange_name)()
        markets = exchange.load_markets()
        print(f"Trading Pairs on {exchange_name}:")
        for pair in markets.keys():
            print(f"- {pair}")
    except Exception as e:
        print(f"Error: {e}. Please ensure the exchange name is correct.")

def download_crypto_data(pair, exchange_name, start_date, end_date, intervals):
    """
    Download historical price and volume data for a cryptocurrency pair.

    Args:
        pair (str): Cryptocurrency trading pair (e.g., 'BTC/USDT').
        exchange_name (str): Exchange name (e.g., 'binance').
        start_date (str): Start date (format: YYYY-MM-DD).
        end_date (str): End date (format: YYYY-MM-DD).
        intervals (list): List of intervals (e.g., ['1d', '1h', '15m']).

    Returns:
        dict: Data organized by interval.
    """
    exchange = getattr(ccxt, exchange_name)({'rateLimit': True})
    data = {}

    for interval in intervals:
        try:
            print(f"Downloading {pair} data for interval: {interval}...")
            
            since = exchange.parse8601(f"{start_date}T00:00:00Z")
            end = exchange.parse8601(f"{end_date}T23:59:59Z")
            
            ohlcv = []
            while since < end:
                candles = exchange.fetch_ohlcv(pair, timeframe=interval, since=since, limit=500)
                if len(candles) == 0:
                    break
                ohlcv += candles
                since = candles[-1][0] + 1
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
            df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            
            # Save to dictionary
            data[interval] = df.to_dict(orient='records')
        
        except Exception as e:
            print(f"Error fetching data for {interval}: {e}")
    
    return data

def save_to_json(data, output_file):
    """
    Save data to a JSON file.

    Args:
        data (dict): Data to save.
        output_file (str): Path to output JSON file.
    """
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Charti: Cryptocurrency chart downloader")
    parser.add_argument("--list-exchanges", action="store_true", help="List all supported exchanges")
    parser.add_argument("--list-pairs", type=str, help="List all trading pairs for a specific exchange")
    parser.add_argument("--download", action="store_true", help="Download chart data")
    parser.add_argument("--pair", type=str, help="Trading pair (e.g., 'BTC/USDT')")
    parser.add_argument("--exchange", type=str, help="Exchange name (e.g., 'binance')")
    parser.add_argument("--start-date", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, help="End date (YYYY-MM-DD)")
    parser.add_argument("--intervals", type=str, nargs='+', default=['1d'], help="Time intervals (e.g., '1d', '1h')")
    parser.add_argument("--output-file", type=str, default="chart_data.json", help="Output JSON file name")
    
    args = parser.parse_args()

    if args.list_exchanges:
        list_exchanges()
    elif args.list_pairs:
        list_pairs(args.list_pairs)
    elif args.download:
        if not all([args.pair, args.exchange, args.start_date, args.end_date]):
            print("Error: Missing required arguments for downloading data.")
            print("Required: --pair, --exchange, --start-date, --end-date")
        else:
            data = download_crypto_data(
                pair=args.pair,
                exchange_name=args.exchange,
                start_date=args.start_date,
                end_date=args.end_date,
                intervals=args.intervals
            )
            save_to_json(data, args.output_file)
    else:
        parser.print_help()
