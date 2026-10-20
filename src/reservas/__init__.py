from pathlib import Path

import click
import mysql.connector
from dotenv import load_dotenv
from flask import Flask
from .routes.clientes import bp as clientes_bp

from .config import get_database_config
from .db import get_connection


def create_app():
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env", override=False)

    app = Flask(__name__)
    app.config["MYSQL"] = get_database_config()

    app.register_blueprint(clientes_bp)

    @app.get("/")
    def index():
        return (
            "<h1>Sistema de Gestión de Reservas</h1>"
            "<p>Aplicación base en funcionamiento.</p>"
            "<p>Clientes, servicios y reservas: pendientes de implementación.</p>"
        )

    @app.cli.command("check-db")
    def check_db():
        """Verifica la conexión y la agenda sin modificar datos."""
        try:
            connection = get_connection()
            try:
                cursor = connection.cursor()
                try:
                    cursor.execute(
                        "SELECT DATABASE(), CURRENT_USER(), "
                        "@@session.time_zone"
                    )
                    database, user, timezone = cursor.fetchone()

                    cursor.execute(
                        "SELECT id FROM agenda WHERE id = 1"
                    )
                    if cursor.fetchone() is None:
                        raise click.ClickException(
                            "No existe la agenda principal."
                        )

                    click.echo(
                        f"OK: database={database}; "
                        f"user={user}; timezone={timezone}; agenda=1"
                    )
                finally:
                    cursor.close()
            finally:
                connection.close()
        except mysql.connector.Error as error:
            raise click.ClickException(
                f"Fallo de conexion MySQL. Codigo: {error.errno}"
            ) from None

    return app