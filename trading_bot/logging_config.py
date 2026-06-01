import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(log_dir: str = "logs", level=logging.INFO):
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "trading_bot.log")

    root = logging.getLogger()
    root.setLevel(level)

    if not any(isinstance(h, RotatingFileHandler) for h in root.handlers):
        fh = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s"))
        root.addHandler(fh)

    # Console handler
    if not any(h for h in root.handlers if isinstance(h, logging.StreamHandler)):
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        root.addHandler(ch)

    # reduce requests noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)
