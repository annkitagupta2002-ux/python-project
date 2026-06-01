import os
import sys
import argparse
import logging
from trading_bot.logging_config import setup_logging
from trading_bot.client import BinanceFuturesClient
from trading_bot.validators import validate_order_args
from trading_bot.orders import place_order


def load_api_credentials():
	api_key = os.environ.get("BINANCE_API_KEY")
	api_secret = os.environ.get("BINANCE_API_SECRET")
	if not api_key or not api_secret:
		raise RuntimeError(
			"BINANCE_API_KEY and BINANCE_API_SECRET must be set in environment variables"
		)
	return api_key, api_secret


def main():
	parser = argparse.ArgumentParser(description="Simple Binance Futures Testnet trading CLI")
	parser.add_argument("--symbol", required=False, help="Trading symbol, e.g., BTCUSDT")
	parser.add_argument("--side", required=False, help="BUY or SELL")
	parser.add_argument("--type", required=False, choices=["MARKET", "LIMIT"], help="Order type")
	parser.add_argument("--quantity", required=False, help="Quantity to buy/sell")
	parser.add_argument("--price", required=False, help="Price for LIMIT orders")
	parser.add_argument("--base-url", required=False, default="https://testnet.binancefuture.com", help="Binance Futures testnet base URL")
	parser.add_argument("--dry-run", action="store_true", help="Simulate order without sending to testnet")

	args = parser.parse_args()
	if len(sys.argv) == 1:
		print("No CLI arguments detected.")
		choice = input("Choose: [1] Run default dry-run, [2] Enter order interactively, [3] Exit (1/2/3): ").strip()
		if choice == "" or choice == "1":
			print("Running default dry-run order.")
			args.symbol = "BTCUSDT"
			args.side = "BUY"
			args.type = "MARKET"
			args.quantity = "0.001"
			args.dry_run = True
		elif choice == "2":
			args.symbol = input("symbol (default BTCUSDT): ").strip() or "BTCUSDT"
			args.side = input("side BUY/SELL (default BUY): ").strip() or "BUY"
			args.type = input("type MARKET/LIMIT (default MARKET): ").strip() or "MARKET"
			args.quantity = input("quantity (default 0.001): ").strip() or "0.001"
			if args.type.upper() == "LIMIT":
				args.price = input("price: ").strip()
			args.dry_run = input("dry-run? y/N: ").strip().lower() in ("y", "yes")
		else:
			print("Exiting.")
			return
	elif args.dry_run and (not args.symbol or not args.side or not args.type or not args.quantity):
		print("Dry-run mode with missing order details; defaulting to BTCUSDT BUY MARKET 0.001.")
		args.symbol = args.symbol or "BTCUSDT"
		args.side = args.side or "BUY"
		args.type = args.type or "MARKET"
		args.quantity = args.quantity or "0.001"

	setup_logging()
	logger = logging.getLogger(__name__)

	try:
		symbol, side, order_type, quantity, price = validate_order_args(args.symbol, args.side, args.type, args.quantity, args.price)
	except Exception as e:
		logger.error("Invalid input: %s", e)
		print(f"Invalid input: {e}")
		return

	# For dry-run skip requiring real API keys
	if args.dry_run:
		logger.info("Dry-run mode: API calls will be simulated")
		api_key = os.environ.get("BINANCE_API_KEY", "dry")
		api_secret = os.environ.get("BINANCE_API_SECRET", "dry")
	else:
		try:
			api_key, api_secret = load_api_credentials()
		except RuntimeError as e:
			logger.error(e)
			print(e)
			return

	client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret, base_url=args.base_url)

	# print summary
	print("Order Request Summary:")
	print(f"  symbol: {symbol}")
	print(f"  side: {side}")
	print(f"  type: {order_type}")
	print(f"  quantity: {quantity}")
	if price is not None:
		print(f"  price: {price}")

	try:
		resp = place_order(client, symbol, side, order_type, quantity, price, dry_run=args.dry_run)
	except Exception as e:
		logger.error("Order failed: %s", e)
		print(f"Order failed: {e}")
		return

	# display response details
	print("Order Response:")
	print(f"  orderId: {resp.get('orderId')}")
	print(f"  status: {resp.get('status')}")
	print(f"  executedQty: {resp.get('executedQty')}")
	print(f"  avgPrice: {resp.get('avgPrice')}")
	print("Order placed (or queued) — see logs for full request/response details.")


if __name__ == "__main__":
	main()

