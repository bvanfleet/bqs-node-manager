import logging
import sys
import yaml

from .data_access.config import Config as SqliteConfig


DAY_IN_SECONDS = 86400


def initialize_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)
    

def initialize_config():
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)
    
    if config['database']['type'] != 'sqlite':
        raise Exception("Only sqlite database type is supported.")
    
    range_start = config['database'].get('node_id_range_start', 1)
    range_end = config['database'].get('node_id_range_end', None)
    
    return SqliteConfig(config['database']['path'], range_start, range_end), config


def default_interrupt_handler(signum, frame):
    logging.info("Interrupt received, shutting down...")
    sys.exit(0)


def register_interrupts():
    import signal
    signal.signal(signal.SIGINT, default_interrupt_handler)
    signal.signal(signal.SIGTERM, default_interrupt_handler)
