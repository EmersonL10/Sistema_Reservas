from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from .config import get_database_config


def create_app():
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env", override=False)

    app = Flask(__name__)
    app.config["MYSQL"] = get_database_config()

    @app.get("/")
    def index():
        return (
            "<h1>Sistema de Gestión de Reservas</h1>"
            "<p>Aplicación base en funcionamiento.</p>"
            "<p>Clientes, servicios y reservas: pendientes de implementación.</p>"
        )

    return app