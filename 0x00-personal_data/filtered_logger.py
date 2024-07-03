#!/usr/bin/env python3
"""
This module contains the filter_datum funtion.
"""
import logging
import re
import os
from typing import List, Union
import sys
import mysql.connector


# Task 0
def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated."""
    for f in fields:
        message = re.sub(f"{f}=(.+?){separator}",
                         f"{f}={redaction}{separator}", message)
    return message


# Task 2
class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes RedactingFormatter."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum."""
        mes = super().format(record)
        return filter_datum(self.fields, self.REDACTION, mes, self.SEPARATOR)


# Task 2
def get_logger() -> logging.Logger:
    """Returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    handler_name = logging.StreamHandler()
    formater = RedactingFormatter(list(PII_FIELDS))

    handler_name.setLevel(logging.INFO)
    handler_name.setFormatter(formater)

    logger.addHandler(handler_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


PII_FIELDS = ("ssn", "password", "name", "email", "phone")


# Task 3
def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to a MySQL database."""

    USERNAME = os.getenv("PERSONAL_DATA_DB_USERNAME")
    PASSWORD = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    HOST = os.getenv("PERSONAL_DATA_DB_HOST")
    NAME = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
        database=NAME)

    return connection


# Task4
def main():
    """ Main function. """
    logger = get_logger()
    db = get_db()

    cursor = db.cursor()
    cursor.execute("describe users;")
    headers = [i[0] for i in cursor if i]
    cursor.close()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor.fetchall():
        message = ''
        for i in range(len(headers)):
            message += f"{headers[i]}={row[i]};"
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
