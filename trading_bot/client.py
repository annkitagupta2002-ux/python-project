import time
import hmac
import hashlib
import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://testnet.binancefuture.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")

    def _sign(self, params: dict) -> str:
        query = "&".join([f"{k}={params[k]}" for k in sorted(params)])
        return hmac.new(self.api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()

    def _request(self, method: str, path: str, params: dict, dry_run: bool = False):
        url = f"{self.base_url}{path}"
        headers = {"X-MBX-APIKEY": self.api_key}
        logger.debug("Request URL: %s params: %s", url, params)
        # Dry-run: simulate a successful response without making network calls
        if dry_run:
            logger.info("Dry-run enabled — not sending request to %s", url)
            simulated = {
                "orderId": int(time.time()),
                "status": "NEW",
                "executedQty": "0",
                "avgPrice": "0",
            }
            if params.get("type", "").upper() == "MARKET":
                avg_price = params.get("price") or 30000.0
                simulated.update({
                    "status": "FILLED",
                    "executedQty": str(params.get("quantity", 0)),
                    "avgPrice": str(avg_price),
                })
            logger.debug("Simulated response: %s", simulated)
            return simulated

        try:
            if method.upper() == "POST":
                resp = requests.post(url, headers=headers, data=params, timeout=15)
            else:
                resp = requests.get(url, headers=headers, params=params, timeout=15)
            logger.debug("Response status: %s body: %s", resp.status_code, resp.text)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and data.get("code") and data.get("msg"):
                # Binance error format
                raise Exception(f"API error: {data.get('code')}: {data.get('msg')}")
            return data
        except requests.RequestException:
            logger.exception("Network or HTTP error")
            raise

    def place_order(self, symbol: str, side: str, type_: str, quantity: float, price: Optional[float] = None, timeInForce: str = "GTC", dry_run: bool = False):
        path = "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "side": side,
            "type": type_,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000),
        }
        if type_.upper() == "LIMIT":
            if price is None:
                raise ValueError("price is required for LIMIT orders")
            params.update({"price": price, "timeInForce": timeInForce})

        params["signature"] = self._sign(params)
        return self._request("POST", path, params, dry_run=dry_run)
