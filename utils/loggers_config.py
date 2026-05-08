import logging
import sys 
import os
from pathlib import Path

def setup_Logger():
    logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
    
    base_dir = Path(__file__).resolve().parent.parent
    log_dir = base_dir / "logs"
    os.makedirs(log_dir, exist_ok = True)
    
    logging.basicConfig(
        level=logging.INFO,
        format=logging_str,
        handlers=[
            logging.FileHandler(log_dir / "running_logs.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger("churn_logger")

logger = setup_Logger()