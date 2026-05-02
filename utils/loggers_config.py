import logging
import sys 
import os

def setup_Logger():
    logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
    
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok = True)
    
    logging.basicConfig(
        level=logging.INFO,
        format=logging_str,
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "running_logs.log")),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger("churn_logger")

logger = setup_Logger()