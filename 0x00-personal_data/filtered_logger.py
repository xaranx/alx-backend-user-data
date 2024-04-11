#!/usr/bin/env python3
"""`filtered_logger.py` defines a method `filter_datum`
which obfuscates specific fields from an input string."""


import re
import os
from typing import List
import logging
from mysql.connector import (connection)

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum."""
        filtered_msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        )
        record.msg = filtered_msg
        return super().format(record)


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """obfuscate specified fields from input string."""
    pattern = re.compile(
        r"(?P<field>{})=(?P<value>[^{}]+)".format("|".join(fields), separator)
    )
    out = re.sub(
        pattern, lambda m: m.group("field") + "=" + redaction, message)
    return out


def get_logger() -> logging.Logger:
    """returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def get_db() -> connection.MySQLConnection:
    """returns a connector to the database."""
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return connection.MySQLConnection(
        user=user, password=password, host=host, database=db_name
    )


def main():
    """reads and filters data from `users` table and inserts it into
    `filtered_data` table.
    """
    conn = get_db()
    cur = conn.cursor()
    lg = get_logger()

    fmt = "name={}; email={}; phone={}; ssn={}; password={}; ip={};\
     last_login={}; user_agent={};"

    cur.execute("SELECT * FROM users;")
    for row in cur:
        msg = fmt.format(row[0], row[1], row[2], row[3], row[4], row[5],
                         row[6], row[7])
        lg.info(msg)
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
