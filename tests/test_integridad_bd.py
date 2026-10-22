import unittest
from datetime import datetime, timedelta, timezone

import mysql.connector

from src.reservas import create_app
from src.reservas.db import get_connection


class IntegridadBDTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.context = self.app.app_context()
        self.context.push()
        self.addCleanup(self.context.pop)

        self.connection = get_connection()
        self.addCleanup(self.connection.close)

        self.cursor = self.connection.cursor()
        self.addCleanup(self.cursor.close)

        # Las limpiezas se ejecutan en orden inverso:
        # rollback, cerrar cursor, cerrar conexión y retirar contexto.
        self.addCleanup(self.connection.rollback)

    def crear_cliente(self):
        self.cursor.execute(
            """
            INSERT INTO clientes (nombre, telefono)
            VALUES (%s, %s)
            """,
            ("Cliente de prueba ACT-04", "000000000"),
        )
        return self.cursor.lastrowid

    def crear_servicio(self):
        self.cursor.execute(
            """
            INSERT INTO servicios (nombre, precio, duracion_minutos)
            VALUES (%s, %s, %s)
            """,
            ("Servicio de prueba ACT-04", "50.00", 60),
        )
        return self.cursor.lastrowid

    def crear_reserva(self, cliente_id, servicio_id):
        inicio = (
            datetime.now(timezone.utc) + timedelta(days=1)
        ).replace(tzinfo=None, microsecond=0)

        fin = inicio + timedelta(minutes=60)

        self.cursor.execute(
            """
            INSERT INTO reservas (
                cliente_id,
                servicio_id,
                inicio_utc,
                fin_utc,
                precio_aplicado,
                duracion_aplicada_minutos
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                cliente_id,
                servicio_id,
                inicio,
                fin,
                "50.00",
                60,
            ),
        )
        return self.cursor.lastrowid

    def test_registro_valido_y_cancelacion(self):
        cliente = self.crear_cliente()
        servicio = self.crear_servicio()
        reserva = self.crear_reserva(cliente, servicio)

        self.cursor.execute(
            """
            UPDATE reservas
            SET estado = 'Cancelada',
                cancelado_en = UTC_TIMESTAMP(6)
            WHERE id = %s
            """,
            (reserva,),
        )

        self.cursor.execute(
            """
            SELECT estado, cancelado_en
            FROM reservas
            WHERE id = %s
            """,
            (reserva,),
        )

        resultado = self.cursor.fetchone()
        self.assertIsNotNone(resultado)

        estado, cancelado_en = resultado
        self.assertEqual(estado, "Cancelada")
        self.assertIsNotNone(cancelado_en)

    def test_duracion_cero_rechazada(self):
        with self.assertRaises(mysql.connector.Error) as result:
            self.cursor.execute(
                """
                INSERT INTO servicios (
                    nombre, precio, duracion_minutos
                )
                VALUES (%s, %s, %s)
                """,
                ("Duracion invalida", "50.00", 0),
            )

        self.assertEqual(result.exception.errno, 3819)

    def test_precio_negativo_rechazado(self):
        with self.assertRaises(mysql.connector.Error) as result:
            self.cursor.execute(
                """
                INSERT INTO servicios (
                    nombre, precio, duracion_minutos
                )
                VALUES (%s, %s, %s)
                """,
                ("Precio invalido", "-1.00", 60),
            )

        self.assertEqual(result.exception.errno, 3819)

    def test_cliente_inexistente_rechazado(self):
        cliente = self.crear_cliente()
        servicio = self.crear_servicio()
        reserva = self.crear_reserva(cliente, servicio)

        self.cursor.execute(
            "SELECT id FROM clientes WHERE id = %s",
            (0,),
        )
        self.assertIsNone(self.cursor.fetchone())

        with self.assertRaises(mysql.connector.Error) as result:
            self.cursor.execute(
                """
                UPDATE reservas
                SET cliente_id = %s
                WHERE id = %s
                """,
                (0, reserva),
            )

        error = result.exception
        self.assertIn(error.errno, (1216, 1452))
        self.assertEqual(error.sqlstate, "23000")

        self.cursor.execute(
            "SELECT cliente_id FROM reservas WHERE id = %s",
            (reserva,),
        )
        self.assertEqual(self.cursor.fetchone(), (cliente,))

    def test_cancelacion_sin_fecha_rechazada(self):
        cliente = self.crear_cliente()
        servicio = self.crear_servicio()
        reserva = self.crear_reserva(cliente, servicio)

        with self.assertRaises(mysql.connector.Error) as result:
            self.cursor.execute(
                """
                UPDATE reservas
                SET estado = 'Cancelada'
                WHERE id = %s
                """,
                (reserva,),
            )

        self.assertEqual(result.exception.errno, 3819)


if __name__ == "__main__":
    unittest.main()