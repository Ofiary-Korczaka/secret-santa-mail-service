import os
import logging


def log_environment_variables():
    """
    Logs the environment variables to the debug logger.

    This function iterates over all the environment variables and logs them
    using the debug level of the logger.

    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    for key, value in os.environ.items():
        logger.debug("%s: %s", key, value)
