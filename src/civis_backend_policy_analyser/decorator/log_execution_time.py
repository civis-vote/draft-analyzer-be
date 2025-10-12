import time
from civis_backend_policy_analyser.config.logging_config import logger
from functools import wraps

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Starting '{func.__name__}'...")
        start_time = time.time()

        result = func(*args, **kwargs)

        duration = time.time() - start_time
        logger.info(f"Finished '{func.__name__}' in {duration:.2f} seconds.")
        return result
    return wrapper
