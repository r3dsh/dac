from logging import *  # noqa
import logging.config
import sys

blue = "\x1b[38;5;75m"
grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"

logFormat = f"%(levelname)s: %(asctime)s {blue}%(name)s{reset} %(message)s"


def getLogger(name, format=None):
    logg = logging.getLogger(name)
    stream_handler = logging.StreamHandler(sys.stderr)

    # f"%(levelname)s: %(asctime)s {yellow}%(name)s{reset} %(message)s"
    logFormat = logging.Formatter(f"%(levelname)s: %(asctime)s {red}%(name)s{reset} %(message)s")

    if format is not None:
        logFormat = logging.Formatter(format)

    stream_handler.setFormatter(logFormat)
    logg.addHandler(stream_handler)

    return logg


logger = getLogger(__name__)


def configure_logging():
    logging_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[%(asctime)s: %(levelname)s] [%(pathname)s:%(lineno)d] %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "loggers": {
            "project": {
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {
                "propagate": True,
            },
        },
    }

    logging.config.dictConfig(logging_dict)
