import time
import inspect
from civis_backend_policy_analyser.config.logging_config import logger
from functools import wraps

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get function signature
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # Format input parameters
        params_str = ', '.join(f"{name}={value!r}" for name, value in bound_args.arguments.items())

        logger.info(f"Starting '{func.__name__}' with args: {params_str}")
        start_time = time.time()

        result = func(*args, **kwargs)

        duration = time.time() - start_time
        logger.info(f"Finished '{func.__name__}' in {duration:.2f} seconds.")
        return result
    return wrapper
