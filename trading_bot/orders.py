import logging
from typing import Optional

from .client import BinanceFuturesClient

logger = logging.getLogger(__name__)


def place_order(client: BinanceFuturesClient, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None, dry_run: bool = False):
    logger.info("Placing order: %s %s %s qty=%s price=%s dry_run=%s", side, order_type, symbol, quantity, price, dry_run)
    try:
        resp = client.place_order(symbol=symbol, side=side, type_=order_type, quantity=quantity, price=price, dry_run=dry_run)
        logger.info("Order response: %s", resp)
        return resp
    except Exception as e:
        logger.exception("Order placement failed")
        raise
