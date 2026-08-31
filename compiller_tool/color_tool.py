# -*- coding: utf-8 -*-

"""
This module has the class Colors for ANSI codes.
"""

import logging
from os import system, name

if name == "nt":
    system("color")     # replace by subprocess.run ?

class Colors:
    """Class to store the color codes for terminal output."""
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"

    BOLD = "\033[1m"

    RESET = "\033[0m"



class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": Colors.CYAN,
        "INFO": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
        "CRITICAL": Colors.RED,
    }
    RESET = Colors.RESET

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        log_message = super().format(record)

        # Ajoute un newline sauf si no_newline est True
        if not record.__dict__.get('no_newline', False):
            log_message += '\n'

        return log_message

