#!/usr/bin/env python3
"""Defines a function that returns the log message obfuscated"""
import re
import logging


def filter_datum(fields, redaction, message, separator):
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
