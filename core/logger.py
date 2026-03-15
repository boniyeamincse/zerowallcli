import logging
import sys
import os

LOG_FILE = "/var/log/zerowall/firewall.log"
LOG_DIR = os.path.dirname(LOG_FILE)

def setup_logger():
    """Sets up the application logger."""
    # Ensure log directory exists
    try:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR, exist_ok=True)
    except Exception as e:
        print(f"Error creating log directory {LOG_DIR}: {e}", file=sys.stderr)
        # Fallback to current directory if /var/log/zerowall is not writable
        LOG_FILE = "firewall.log"

    logger = logging.getLogger("ZeroWall")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File Handler
    try:
        fh = logging.FileHandler(LOG_FILE)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception as e:
        print(f"Warning: Could not write to log file {LOG_FILE}: {e}", file=sys.stderr)

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    ch.setLevel(logging.WARNING) # Only log warnings/errors to console
    logger.addHandler(ch)

    return logger

logger = setup_logger()
