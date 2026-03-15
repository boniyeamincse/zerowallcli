import logging
import sys
import os

LOG_FILE = "/var/log/zerowall/firewall.log"
LOG_DIR = os.path.dirname(LOG_FILE)

def setup_logger():
    """Sets up the application logger with secure permissions."""
    log_path = "/var/log/zerowall/firewall.log"
    log_dir = os.path.dirname(log_path)
    logger = logging.getLogger("ZeroWall")
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File Handler
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # Open file with 0600 permissions if it doesn't exist
        if not os.path.exists(log_path):
            fd = os.open(log_path, os.O_WRONLY | os.O_CREAT, 0o600)
            os.close(fd)
        else:
            # Ensure existing file is 0600
            os.chmod(log_path, 0o600)

        fh = logging.FileHandler(log_path)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception as e:
        print(f"Warning: Could not setup secure file logging: {e}. Logging to console only.", file=sys.stderr)

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    ch.setLevel(logging.WARNING) # Only log warnings/errors to console
    logger.addHandler(ch)

    return logger

logger = setup_logger()
