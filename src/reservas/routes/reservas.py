import mysql.connector
from flask import Blueprint, current_app, jsonify, request

from ..repositories import reservas as repository
from ..services.reservas import ReservaError, validar_reserva


bp = Blueprint("reservas", __name__, url_prefix="/api/reservas")


@bp.errorhandler(ReservaError)
def reserva_error(error):
    return jsonify(
        error=str(error),
        alternativas=error.alternativas,
    ), error.status


@bp.errorhandler(mysql.connector.Error)
def database_error(error):
    current_app.logger.error(
        "Fallo MySQL en reservas; codigo=%s", error.errno
    )
    return jsonify(
        error="No se pudo completar la operación. Consulte antes de reintentar."
    ), 503


@bp.post("")
def registrar_reserva():
    datos = validar_reserva(request.get_json(silent=True))
    reserva = repository.crear(datos)
    return jsonify(reserva), 201