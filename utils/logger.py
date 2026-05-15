import logging
from datetime import datetime
from pathlib import Path
from config.logging_config import logger as global_logger 

def initialize_logger(module_name: str):
    log_dir = Path("logs") / str(datetime.today().date()) / module_name
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    log_file = log_dir / f"{timestamp}.log"

    logger = logging.getLogger(module_name)
    
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    return logger