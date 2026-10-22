import unittest

from src.reservas.services.reservas import (
    ReservaError,
    validar_reserva,
)


class FechasReservasTest(unittest.TestCase):
    def test_conversion_fuera_de_rango(self):
        with self.assertRaises(ReservaError) as result:
            validar_reserva({
                "cliente_id": 1,
                "servicio_id": 1,
                "inicio": "9999-12-31T23:59",
            })

        self.assertEqual(result.exception.status, 400)
        self.assertIn("rango", str(result.exception))

    def test_fecha_invalida(self):
        with self.assertRaises(ReservaError):
            validar_reserva({
                "cliente_id": 1,
                "servicio_id": 1,
                "inicio": "2026-02-30T10:00",
            })


if __name__ == "__main__":
    unittest.main()