from ..db import get_connection
from ..services.reservas import (
    ReservaError,
    ahora_utc,
    buscar_alternativas,
    calcular_fin,
    formato_local,
    hay_superposicion,
)


COLUMNAS_CONSULTA = """
    r.id, r.cliente_id, c.nombre AS cliente,
    r.servicio_id, s.nombre AS servicio,
    r.inicio_utc, r.fin_utc, r.precio_aplicado,
    r.duracion_aplicada_minutos, r.estado, r.cancelado_en
"""

TABLAS_CONSULTA = """
    FROM reservas AS r
    JOIN clientes AS c ON c.id = r.cliente_id
    JOIN servicios AS s ON s.id = r.servicio_id
"""


def serializar(fila):
    return {
        "id": fila["id"],
        "cliente_id": fila["cliente_id"],
        "cliente": fila["cliente"],
        "servicio_id": fila["servicio_id"],
        "servicio": fila["servicio"],
        "inicio": formato_local(fila["inicio_utc"]),
        "fin": formato_local(fila["fin_utc"]),
        "precio_aplicado": format(fila["precio_aplicado"], ".2f"),
        "duracion_minutos": fila["duracion_aplicada_minutos"],
        "estado": fila["estado"],
        "cancelado_en": (
            fila["cancelado_en"].isoformat(timespec="microseconds") + "Z"
            if fila["cancelado_en"] is not None
            else None
        ),
    }


def crear(datos):
    connection = get_connection()

    try:
        connection.start_transaction(isolation_level="READ COMMITTED")
        cursor = connection.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(
                "SELECT id FROM agenda WHERE id = 1 FOR UPDATE"
            )
            if cursor.fetchone() is None:
                raise ReservaError(
                    "La agenda no está disponible.", status=503
                )

            cursor.execute(
                "SELECT id FROM clientes WHERE id = %s FOR SHARE",
                (datos["cliente_id"],),
            )
            if cursor.fetchone() is None:
                raise ReservaError(
                    "Cliente no encontrado.", status=404
                )

            cursor.execute(
                """
                SELECT id, precio, duracion_minutos
                FROM servicios
                WHERE id = %s FOR SHARE
                """,
                (datos["servicio_id"],),
            )
            servicio = cursor.fetchone()

            if servicio is None:
                raise ReservaError(
                    "Servicio no encontrado.", status=404
                )

            inicio = datos["inicio_utc"]
            if inicio <= ahora_utc():
                raise ReservaError(
                    "El inicio debe ser posterior al momento actual."
                )

            duracion = servicio["duracion_minutos"]
            fin = calcular_fin(inicio, duracion)

            cursor.execute(
                """
                SELECT inicio_utc, fin_utc
                FROM reservas
                WHERE agenda_id = 1 AND estado = 'Confirmada'
                ORDER BY inicio_utc
                FOR UPDATE
                """
            )
            intervalos = [
                (fila["inicio_utc"], fila["fin_utc"])
                for fila in cursor.fetchall()
            ]

            if hay_superposicion(inicio, fin, intervalos):
                alternativas = buscar_alternativas(
                    inicio, duracion, intervalos
                )
                mensaje = "El intervalo solicitado está ocupado."

                if not alternativas:
                    mensaje += (
                        " No hay alternativas en los próximos siete días;"
                        " consulte otra fecha."
                    )

                raise ReservaError(
                    mensaje,
                    status=409,
                    alternativas=alternativas,
                )

            cursor.execute(
                """
                INSERT INTO reservas (
                    agenda_id, cliente_id, servicio_id,
                    inicio_utc, fin_utc, precio_aplicado,
                    duracion_aplicada_minutos
                )
                VALUES (1, %s, %s, %s, %s, %s, %s)
                """,
                (
                    datos["cliente_id"],
                    datos["servicio_id"],
                    inicio,
                    fin,
                    servicio["precio"],
                    duracion,
                ),
            )
            reserva_id = cursor.lastrowid

            resultado = {
                "id": reserva_id,
                "cliente_id": datos["cliente_id"],
                "servicio_id": datos["servicio_id"],
                "inicio": formato_local(inicio),
                "fin": formato_local(fin),
                "precio_aplicado": format(servicio["precio"], ".2f"),
                "duracion_minutos": duracion,
                "estado": "Confirmada",
            }

            connection.commit()
            return resultado
        finally:
            cursor.close()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def listar():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(
                f"""
                SELECT {COLUMNAS_CONSULTA}
                {TABLAS_CONSULTA}
                ORDER BY r.inicio_utc, r.id
                """
            )
            return [serializar(fila) for fila in cursor.fetchall()]
        finally:
            cursor.close()
    finally:
        connection.close()


def obtener(reserva_id):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(
                f"""
                SELECT {COLUMNAS_CONSULTA}
                {TABLAS_CONSULTA}
                WHERE r.id = %s
                """,
                (reserva_id,),
            )
            fila = cursor.fetchone()
            return serializar(fila) if fila is not None else None
        finally:
            cursor.close()
    finally:
        connection.close()


def cancelar(reserva_id):
    connection = get_connection()

    try:
        connection.start_transaction(isolation_level="READ COMMITTED")
        cursor = connection.cursor(dictionary=True, buffered=True)

        try:
            # Mismo orden de bloqueo que en el registro de reservas.
            cursor.execute(
                "SELECT id FROM agenda WHERE id = 1 FOR UPDATE"
            )
            if cursor.fetchone() is None:
                raise ReservaError(
                    "La agenda no está disponible.", status=503
                )

            cursor.execute(
                """
                SELECT id, inicio_utc, estado
                FROM reservas
                WHERE id = %s
                FOR UPDATE
                """,
                (reserva_id,),
            )
            reserva = cursor.fetchone()

            if reserva is None:
                raise ReservaError(
                    "Reserva no encontrada.", status=404
                )

            # Una cancelación repetida conserva su fecha original.
            if reserva["estado"] != "Cancelada":
                if reserva["inicio_utc"] <= ahora_utc():
                    raise ReservaError(
                        "No se puede cancelar una reserva ya iniciada.",
                        status=409,
                    )

                cursor.execute(
                    """
                    UPDATE reservas
                    SET estado = 'Cancelada',
                        cancelado_en = UTC_TIMESTAMP(6)
                    WHERE id = %s
                    """,
                    (reserva_id,),
                )

            cursor.execute(
                f"""
                SELECT {COLUMNAS_CONSULTA}
                {TABLAS_CONSULTA}
                WHERE r.id = %s
                """,
                (reserva_id,),
            )
            resultado = serializar(cursor.fetchone())

            connection.commit()
            return resultado
        finally:
            cursor.close()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()