#!/usr/bin/env python3
"""
This module contains the filter_datum funtion.
"""
import logging
import re
from os import getenv
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

        # call the format method of the parent class
        mes = super().format(record)

        return filter_datum(self.fields, self.REDACTION, mes, self.SEPARATOR)


# Task 2
def get_logger() -> logging.Logger:
    """Returns a logging.Logger object."""
    # creating logger, handler and formatter:
    logger = logging.getLogger("user_data")
    handler_name = logging.StreamHandler()
    formater = RedactingFormatter(list(PII_FIELDS))

    # setting the formatter and level of the handler
    handler_name.setLevel(logging.INFO)
    handler_name.setFormatter(formater)

    # adding the handler to the logger
    logger.addHandler(handler_name)

    # logger.setLevel(logging.INFO)

    # prevent the propagation of the log message to the parent logger
    logger.propagate = False

    return logger


PII_FIELDS = ("ssn", "password", "name", "email", "phone")


# Task 3
def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to a MySQL database."""

    # get the environment variables
    USERNAME = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    PASSWORD = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    HOST = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    DB_NAME = getenv("PERSONAL_DATA_DB_NAME")

    # check if the database name is provided
    if not DB_NAME:
        print("No database name provided")
        exit(1)

    # create the connection
    connection = mysql.connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
        database=DB_NAME)

    return connection


# Task4
def main():
    """ Main function. """
    # getting the logger and the database connector
    logger = get_logger()
    db = get_db()

    # getting the headers
    cursor = db.cursor()
    cursor.execute("describe users;")
    headers = [i[0] for i in cursor if i]
    cursor.close()

    # getting the data
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    # logging the data
    for row in cursor.fetchall():
        message = ''
        for i in range(len(headers)):
            # format the message, exaple:
            # ssn=12;password=pwd;name=fullname;email=email;phone=67890;
            message += f"{headers[i]}={row[i]};"

        # log the message
        logger.info(message)

    # close the cursor and the database connector
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
