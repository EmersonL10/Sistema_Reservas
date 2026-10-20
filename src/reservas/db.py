import mysql.connector
from flask import current_app


def get_connection():
    return mysql.connector.connect(
        **current_app.config["MYSQL"],
        connection_timeout=5,
        autocommit=False,
        time_zone="+00:00",
    )