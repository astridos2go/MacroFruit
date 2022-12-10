import logging
import os
import sys
from ctypes import windll
from logging import INFO, Formatter, StreamHandler, info
from os.path import dirname

import confuse
from confuse import Configuration
from user_interface import user_interface

FROZEN = getattr(sys, "frozen", False)

LOCATION = dirname(__file__) if not FROZEN else dirname(sys.executable)


def configureLogging(config_dir):
    # Save the log file location
    log_path = os.path.join(config_dir, "latest.log")

    # Set up logging to file
    logging.basicConfig(
        filename=log_path,
        level=INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Check if frozen
    if not FROZEN:
        # Define console logger
        console = StreamHandler()
        # Set logging level
        console.setLevel(INFO)
        # Define formatter
        console_formatter = Formatter("[%(levelname)s] %(message)s")
        # Set formatter
        console.setFormatter(console_formatter)
        # Add stream handler
        logging.getLogger().addHandler(console)


if __name__ == "__main__":
    # Set program DPI aware
    windll.shcore.SetProcessDpiAwareness(2)

    # Get the configuration
    config = Configuration("MacroFruit", "__init__")

    # Set up logging
    configureLogging(config.config_dir())

    info(confuse.util.find_package_path("MacroFruit"))
    App = user_interface(FROZEN, LOCATION, config)
    App.mainloop()
