from ..db import get_connection


COLUMNAS = "id, nombre, telefono, email"


def listar():
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                f"SELECT {COLUMNAS} FROM clientes ORDER BY id"
            )
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()


def obtener(cliente_id):
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                f"SELECT {COLUMNAS} FROM clientes WHERE id = %s",
                (cliente_id,),
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
                INSERT INTO clientes (nombre, telefono, email)
                VALUES (%s, %s, %s)
                """,
                (datos["nombre"], datos["telefono"], datos["email"]),
            )
            cliente_id = cursor.lastrowid
            connection.commit()
            return {"id": cliente_id, **datos}
        finally:
            cursor.close()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def actualizar(cliente_id, datos):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT id FROM clientes
                WHERE id = %s FOR UPDATE
                """,
                (cliente_id,),
            )
            if cursor.fetchone() is None:
                connection.rollback()
                return None

            cursor.execute(
                """
                UPDATE clientes
                SET nombre = %s, telefono = %s, email = %s,
                    actualizado_en = UTC_TIMESTAMP(6)
                WHERE id = %s
                """,
                (
                    datos["nombre"],
                    datos["telefono"],
                    datos["email"],
                    cliente_id,
                ),
            )
            connection.commit()
            return {"id": cliente_id, **datos}
        finally:
            cursor.close()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()