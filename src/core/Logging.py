from datetime import datetime
import logging
from pathlib import Path
from platformdirs import user_data_dir
from .GitManager import GitManager


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("CartoisGit")
    logger.setLevel(logging.DEBUG)

    log_dir = Path(user_data_dir("GitBack")) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    filename = log_dir / (datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log")
    handler = logging.FileHandler(filename, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    logger.addHandler(handler)
    _log_handler = handler

    return logger, _log_handler



def teardown_logging(logger: logging.Logger, handler: logging.FileHandler) -> None:
    handler.flush()
    handler.close()
    logger.removeHandler(handler)
