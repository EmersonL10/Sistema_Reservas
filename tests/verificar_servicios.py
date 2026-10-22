from src.reservas import create_app


def verificar():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.post("/api/servicios", json={
            "nombre": "Servicio ficticio ACT-06",
            "precio": "50.25",
            "duracion_minutos": 60,
        })
        assert response.status_code == 201, response.get_json()
        servicio = response.get_json()
        servicio_id = servicio["id"]
        assert servicio["precio"] == "50.25"
        assert servicio["duracion_minutos"] == 60
        print("Registro y precio exacto: OK; id =", servicio_id)

        response = client.get(f"/api/servicios/{servicio_id}")
        assert response.status_code == 200
        assert response.get_json() == servicio
        print("Consulta individual: OK")

        response = client.get("/api/servicios")
        assert response.status_code == 200
        assert any(
            item["id"] == servicio_id for item in response.get_json()
        )
        print("Listado: OK")

        casos_invalidos = [
            {"nombre": "   "},
            {"precio": "-1.00"},
            {"precio": "abc"},
            {"precio": "10.123"},
            {"precio": "NaN"},
            {"precio": "Infinity"},
            {"precio": True},
            {"duracion_minutos": 0},
            {"duracion_minutos": -1},
            {"duracion_minutos": 1.5},
            {"duracion_minutos": True},
        ]

        cantidad_inicial = len(
            client.get("/api/servicios").get_json()
        )

        for cambio in casos_invalidos:
            payload = {
                "nombre": "Servicio invalido",
                "precio": "10.00",
                "duracion_minutos": 30,
                **cambio,
            }
            response = client.post("/api/servicios", json=payload)
            assert response.status_code == 400, (
                cambio, response.status_code, response.get_json()
            )

        cantidad_final = len(
            client.get("/api/servicios").get_json()
        )
        assert cantidad_final == cantidad_inicial
        print("Once entradas invalidas rechazadas sin insertar: OK")

        assert client.get("/api/servicios/0").status_code == 404
        print("Servicio inexistente: OK")

    nueva_app = create_app()
    with nueva_app.test_client() as client:
        response = client.get(f"/api/servicios/{servicio_id}")
        assert response.status_code == 200
        assert response.get_json() == servicio

    print("Persistencia entre instancias: OK")
    print("Identificador para comprobar en otro proceso:", servicio_id)


if __name__ == "__main__":
    verificar()