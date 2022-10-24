#!/usr/bin/env python3
"""Defines a function that returns the log message obfuscated"""
import re
import logging
from typing import List
from os import getenv
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to MySQL database."""
    my_db = mysql.connector.connect(
        host=getenv("PERSONAL_DATA_DB_HOST"),
        user=getenv("PERSONAL_DATA_DB_USERNAME"),
        password=getenv("PERSONAL_DATA_DB_PASSWORD"),
        database=getenv("PERSONAL_DATA_DB_NAME"),
        auth_plugin='mysql_native_password'
    )
    return my_db


def main() -> None:
    """Display all rows in the user table of a database."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    message = cursor
    logger = get_logger()
    logger.info(message)

    cursor.close()
    db.close()


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """returns the log message obfuscated

    Parameters:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all
        fields in the message.
    """

    for f in fields:
        message = re.sub(
            "{}=.*?{}".format(f, separator),
            "{}={}{}".format(f, redaction, separator),
            message,
        )
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor function"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Filters incoming logs values"""

        record.msg = filter_datum(
            list(self.fields), self.REDACTION,
            record.getMessage(), self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """returns a Logger object"""

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


if __name__ == "__main__":
    """Execute main() function"""

    main()
