#!/usr/bin/env python3
"""
This module contains the filter_datum funtion.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated."""
    for f in fields:
        message = re.sub(f"{f}=(.+?){separator}",
                         f"{f}={redaction}{separator}", message)
    return message
