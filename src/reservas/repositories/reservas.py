from ..db import get_connection
from ..services.reservas import (
    ReservaError,
    ahora_utc,
    buscar_alternativas,
    calcular_fin,
    formato_local,
    hay_superposicion,
)


def crear(datos):
    connection = get_connection()

    try:
        connection.start_transaction(isolation_level="READ COMMITTED")
        cursor = connection.cursor(dictionary=True, buffered=True)

        try:
            # Todas las escrituras de disponibilidad deben tomar
            # primero este mismo bloqueo.
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
            connection.commit()

            return {
                "id": reserva_id,
                "cliente_id": datos["cliente_id"],
                "servicio_id": datos["servicio_id"],
                "inicio": formato_local(inicio),
                "fin": formato_local(fin),
                "precio_aplicado": format(servicio["precio"], ".2f"),
                "duracion_minutos": duracion,
                "estado": "Confirmada",
            }
        finally:
            cursor.close()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()