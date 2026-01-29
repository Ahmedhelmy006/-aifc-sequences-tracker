import logging
import os
from config import settings
from pathlib import Path
import sys

os.makedirs("logs", exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
