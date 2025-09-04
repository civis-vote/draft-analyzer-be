import sys
from loguru import logger
from civis_backend_policy_analyser.utils.constants import (
    LOG_COMPRESSION,
    LOG_LEVEL,
    LOG_PATH,
    LOG_RETENTION,
    LOG_ROTATION,
)

# Remove default logger to avoid duplicate messages
logger.remove()

if LOG_PATH:
    # Log to file with rotation
    logger.add(
        LOG_PATH,
        level=LOG_LEVEL,
        rotation=LOG_ROTATION,
        retention=LOG_RETENTION,
        compression=LOG_COMPRESSION,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    )
else:
    # Log to stdout
    logger.add(
        sys.stdout,
        level=LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    )

__all__ = ["logger"]
