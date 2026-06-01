from typing import Tuple


def validate_symbol(symbol: str) -> str:
    if not symbol or not symbol.isalnum():
        raise ValueError("symbol must be an alphanumeric string, e.g., BTCUSDT")
    return symbol.upper()


def validate_side(side: str) -> str:
    s = side.upper()
    if s not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.upper()
    if t not in ("MARKET", "LIMIT"):
        raise ValueError("order type must be MARKET or LIMIT")
    return t


def validate_quantity(qty: str) -> float:
    try:
        q = float(qty)
    except Exception:
        raise ValueError("quantity must be a number")
    if q <= 0:
        raise ValueError("quantity must be > 0")
    return q


def validate_price(price: str) -> float:
    try:
        p = float(price)
    except Exception:
        raise ValueError("price must be a number")
    if p <= 0:
        raise ValueError("price must be > 0")
    return p


def validate_order_args(symbol: str, side: str, order_type: str, quantity: str, price: str = None):
    s = validate_symbol(symbol)
    sd = validate_side(side)
    t = validate_order_type(order_type)
    q = validate_quantity(quantity)
    p = None
    if t == "LIMIT":
        if price is None:
            raise ValueError("price is required for LIMIT orders")
        p = validate_price(price)
    return s, sd, t, q, p
