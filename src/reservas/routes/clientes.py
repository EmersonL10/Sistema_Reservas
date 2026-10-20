import mysql.connector
from flask import Blueprint, current_app, jsonify, request

from ..repositories import clientes as repository
from ..services.clientes import validar_cliente


bp = Blueprint("clientes", __name__, url_prefix="/api/clientes")


@bp.errorhandler(mysql.connector.Error)
def database_error(error):
    current_app.logger.error(
        "Fallo MySQL en clientes; codigo=%s", error.errno
    )
    return jsonify(error="No se pudo completar la operación."), 503


@bp.get("")
def listar_clientes():
    return jsonify(repository.listar())


@bp.get("/<int:cliente_id>")
def consultar_cliente(cliente_id):
    cliente = repository.obtener(cliente_id)
    if cliente is None:
        return jsonify(error="Cliente no encontrado."), 404
    return jsonify(cliente)


@bp.post("")
def registrar_cliente():
    try:
        datos = validar_cliente(request.get_json(silent=True))
    except ValueError as error:
        return jsonify(error=str(error)), 400

    cliente = repository.crear(datos)
    return jsonify(cliente), 201


@bp.put("/<int:cliente_id>")
def modificar_cliente(cliente_id):
    try:
        datos = validar_cliente(request.get_json(silent=True))
    except ValueError as error:
        return jsonify(error=str(error)), 400

    cliente = repository.actualizar(cliente_id, datos)
    if cliente is None:
        return jsonify(error="Cliente no encontrado."), 404
    return jsonify(cliente)