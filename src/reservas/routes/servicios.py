import mysql.connector
from flask import Blueprint, current_app, jsonify, request

from ..repositories import servicios as repository
from ..services.servicios import validar_servicio


bp = Blueprint("servicios", __name__, url_prefix="/api/servicios")


def serializar(servicio):
    return {
        **servicio,
        "precio": format(servicio["precio"], ".2f"),
    }


@bp.errorhandler(mysql.connector.Error)
def database_error(error):
    current_app.logger.error(
        "Fallo MySQL en servicios; codigo=%s", error.errno
    )
    return jsonify(error="No se pudo completar la operación."), 503


@bp.get("")
def listar_servicios():
    return jsonify([serializar(item) for item in repository.listar()])


@bp.get("/<int:servicio_id>")
def consultar_servicio(servicio_id):
    servicio = repository.obtener(servicio_id)
    if servicio is None:
        return jsonify(error="Servicio no encontrado."), 404
    return jsonify(serializar(servicio))


@bp.post("")
def registrar_servicio():
    try:
        datos = validar_servicio(request.get_json(silent=True))
    except ValueError as error:
        return jsonify(error=str(error)), 400

    servicio = repository.crear(datos)
    return jsonify(serializar(servicio)), 201