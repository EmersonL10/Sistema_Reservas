import unittest
from unittest.mock import patch

import mysql.connector

from src.reservas import create_app


class ValidacionesAPITest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_cliente_correo_invalido_no_llega_al_repositorio(self):
        with patch(
            "src.reservas.routes.clientes.repository.crear"
        ) as crear:
            response = self.client.post("/api/clientes", json={
                "nombre": "Cliente ficticio",
                "telefono": "000000000",
                "email": "correo-invalido",
            })

        self.assertEqual(response.status_code, 400)
        crear.assert_not_called()

    def test_cliente_campos_invalidos_no_se_guardan(self):
        casos = [
            {"nombre": "   "},
            {"telefono": ""},
            {"telefono": 123456},
            {"nombre": "x" * 121},
            {"telefono": "1" * 31},
            {"email": ["correo@example.com"]},
        ]

        for cambio in casos:
            with self.subTest(cambio=cambio):
                with patch(
                    "src.reservas.routes.clientes.repository.crear"
                ) as crear:
                    response = self.client.post("/api/clientes", json={
                        "nombre": "Cliente ficticio",
                        "telefono": "000000000",
                        **cambio,
                    })

                self.assertEqual(response.status_code, 400)
                crear.assert_not_called()

    def test_json_malformado_se_rechaza(self):
        for ruta in (
            "/api/clientes",
            "/api/servicios",
            "/api/reservas",
        ):
            with self.subTest(ruta=ruta):
                response = self.client.post(
                    ruta,
                    data='{"dato":',
                    content_type="application/json",
                )

                self.assertEqual(response.status_code, 400)
                self.assertIsInstance(response.get_json()["error"], str)

    def test_servicio_importes_invalidos_no_se_guardan(self):
        precios = [
            "-0.01",
            "100000000.00",
            "10.123",
            "NaN",
            "Infinity",
            True,
            None,
        ]

        for precio in precios:
            with self.subTest(precio=precio):
                with patch(
                    "src.reservas.routes.servicios.repository.crear"
                ) as crear:
                    response = self.client.post("/api/servicios", json={
                        "nombre": "Servicio ficticio",
                        "precio": precio,
                        "duracion_minutos": 30,
                    })

                self.assertEqual(response.status_code, 400)
                crear.assert_not_called()

    def test_servicio_gratuito_es_valido(self):
        with patch(
            "src.reservas.routes.servicios.repository.crear"
        ) as crear:
            crear.side_effect = lambda datos: {"id": 1, **datos}

            response = self.client.post("/api/servicios", json={
                "nombre": "Servicio gratuito",
                "precio": "0.00",
                "duracion_minutos": 30,
            })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["precio"], "0.00")
        crear.assert_called_once()

    def test_servicio_duracion_invalida_no_se_guarda(self):
        for duracion in (0, -1, 1.5, True, "30", 65536):
            with self.subTest(duracion=duracion):
                with patch(
                    "src.reservas.routes.servicios.repository.crear"
                ) as crear:
                    response = self.client.post("/api/servicios", json={
                        "nombre": "Servicio ficticio",
                        "precio": "10.00",
                        "duracion_minutos": duracion,
                    })

                self.assertEqual(response.status_code, 400)
                crear.assert_not_called()

    def test_modificacion_invalida_no_llega_al_repositorio(self):
        with patch(
            "src.reservas.routes.clientes.repository.actualizar"
        ) as actualizar:
            response = self.client.put("/api/clientes/1", json={
                "nombre": " ",
                "telefono": "000000000",
            })

        self.assertEqual(response.status_code, 400)
        actualizar.assert_not_called()

    def test_fallo_mysql_no_expone_detalles_internos(self):
        escenarios = [
            (
                "/api/clientes",
                "src.reservas.routes.clientes.repository.listar",
            ),
            (
                "/api/servicios",
                "src.reservas.routes.servicios.repository.listar",
            ),
            (
                "/api/reservas",
                "src.reservas.routes.reservas.repository.listar",
            ),
        ]

        for ruta, destino in escenarios:
            with self.subTest(ruta=ruta):
                with patch(destino) as listar:
                    listar.side_effect = mysql.connector.Error(
                        msg="DETALLE_INTERNO_NO_PUBLICAR",
                        errno=2003,
                    )
                    response = self.client.get(ruta)

                self.assertEqual(response.status_code, 503)
                self.assertNotIn(
                    "DETALLE_INTERNO_NO_PUBLICAR",
                    response.get_data(as_text=True),
                )
                self.assertIsInstance(response.get_json()["error"], str)


if __name__ == "__main__":
    unittest.main()