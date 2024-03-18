"""
etl-pipelines logging.
"""
import configparser
import logging
import os
import pathlib
import typing
from logging import config as logcfg

LOGGER = logging.getLogger(__name__)
OPTIONS = {}
CONFIG = "logging.ini"


def setup(path: typing.Optional[typing.Union[pathlib.Path, str]] = None, **options: typing.Any):
    """Setup logger according to the params."""
    parser = configparser.ConfigParser(OPTIONS | options)
    used = parser.read([path or pathlib.Path(__file__).parent / os.getenv("LOG_CONFIG", CONFIG)])
    logcfg.fileConfig(parser, disable_existing_loggers=True)
    logging.captureWarnings(capture=True)
    LOGGER.debug("Logging config: %s", ", ".join(used) or "none")
