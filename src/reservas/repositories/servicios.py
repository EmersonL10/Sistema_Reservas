from ..db import get_connection


COLUMNAS = "id, nombre, precio, duracion_minutos"


def listar():
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                f"SELECT {COLUMNAS} FROM servicios ORDER BY id"
            )
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()


def obtener(servicio_id):
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                f"SELECT {COLUMNAS} FROM servicios WHERE id = %s",
                (servicio_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
    finally:
        connection.close()


def crear(datos):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO servicios (nombre, precio, duracion_minutos)
                VALUES (%s, %s, %s)
                """,
                (
                    datos["nombre"],
                    datos["precio"],
                    datos["duracion_minutos"],
                ),
            )
            servicio_id = cursor.lastrowid
            connection.commit()
            return {"id": servicio_id, **datos}
        finally:
            cursor.close()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()