import logging
import sys
import os

LOG_FILE = "/var/log/zerowall/firewall.log"
LOG_DIR = os.path.dirname(LOG_FILE)

def setup_logger():
    """Sets up the application logger."""
    log_path = "/var/log/zerowall/firewall.log"
    log_dir = os.path.dirname(log_path)

    # Ensure log directory exists
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating log directory {log_dir}: {e}", file=sys.stderr)
        # Fallback to current directory if /var/log/zerowall is not writable
        log_path = "firewall.log"

    logger = logging.getLogger("ZeroWall")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File Handler
    try:
        fh = logging.FileHandler(log_path)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception as e:
        print(f"Warning: Could not write to log file {log_path}: {e}", file=sys.stderr)

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    ch.setLevel(logging.WARNING) # Only log warnings/errors to console
    logger.addHandler(ch)

    return logger

logger = setup_logger()
