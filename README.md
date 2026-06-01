# Binance Futures Testnet Trading Bot (Simple)

A minimal Python app to place MARKET and LIMIT orders on Binance Futures Testnet (USDT-M). It provides a clear client layer, a CLI (with interactive fallback), input validation, structured logging, and a dry-run simulation mode for safe testing.

## Requirements

- Python 3.8+
- pip

## Install

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Provide Binance Futures Testnet API credentials via environment variables:

```powershell
$Env:BINANCE_API_KEY="your_testnet_key"
$Env:BINANCE_API_SECRET="your_testnet_secret"
```

The app uses the Testnet base URL by default: `https://testnet.binancefuture.com`.

## Usage

Run a MARKET order (dry-run simulated):

```bash
python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --dry-run
```

Run a LIMIT order (dry-run simulated):

```bash
python main.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 40000 --dry-run
```

Place a real testnet order (set env vars and omit `--dry-run`):

```powershell
$Env:BINANCE_API_KEY="your_testnet_key"
$Env:BINANCE_API_SECRET="your_testnet_secret"
python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

## Interactive / Run Button

- If you click the Run button in VS Code (or run `python main.py` with no arguments), the script now prompts you to: run a default dry-run, enter order values interactively, or exit. This makes the Run button usable for demos.

## Dry-run

- Use `--dry-run` to simulate an order without sending it to the testnet. The simulation returns a plausible response (MARKET orders are simulated as FILLED with a sample `avgPrice`).

## Output

- Console: prints `Order Request Summary` and `Order Response`.
- Log file: detailed request/response and errors are written to `logs/trading_bot.log`.
- Example logs included: `logs/example_market_order.log`, `logs/example_limit_order.log`.

## Project Structure

- `trading_bot/`
  - `client.py` — Binance Futures client wrapper (signing + request)
  - `orders.py` — high-level order placement flow
  - `validators.py` — input validation
  - `logging_config.py` — logging setup (rotating file + console)
- `main.py` — CLI entry point and interactive fallback
- `requirements.txt`
- `README.md`
- `logs/` — runtime and example logs

## Validation & Error Handling

- CLI inputs are validated (symbol format, side, type, quantity, price).
- Network/HTTP errors and API error responses are logged and surfaced to the console.
- LIMIT orders require `--price`.

## Signing

- Requests to signed endpoints include an HMAC-SHA256 signature generated from the request parameters (as required by Binance Futures API).

## Notes / Assumptions

- Targets Binance Futures Testnet (USDT-M).
- Keys are read from environment variables for safety.
- Dry-run mode is suitable for generating sample logs for submissions.




