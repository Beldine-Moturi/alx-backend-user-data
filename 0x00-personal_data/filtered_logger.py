#!/usr/bin/env python3
"""Defines a function that returns the log message obfuscated"""
import re
import logging
from typing import List


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
