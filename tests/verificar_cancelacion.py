from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from uuid import uuid4
from zoneinfo import ZoneInfo

from src.reservas import create_app
from src.reservas.db import get_connection


def verificar():
    app = create_app()
    app.config["TESTING"] = True
    marca = uuid4().hex[:8]

    # Elegir un intervalo posterior a las reservas existentes.
    with app.app_context():
        connection = get_connection()
        try:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """
                    SELECT MAX(fin_utc)
                    FROM reservas
                    WHERE estado = 'Confirmada'
                    """
                )
                ultimo_fin = cursor.fetchone()[0]
            finally:
                cursor.close()
        finally:
            connection.close()

    referencia = datetime.now(timezone.utc).replace(tzinfo=None)
    if ultimo_fin is not None:
        referencia = max(referencia, ultimo_fin)

    inicio = (referencia + timedelta(days=2)).replace(
        hour=15, minute=0, second=0, microsecond=0
    )
    inicio_local = (
        inicio.replace(tzinfo=timezone.utc)
        .astimezone(ZoneInfo("America/Lima"))
        .strftime("%Y-%m-%dT%H:%M")
    )

    with app.test_client() as client:
        response = client.post("/api/clientes", json={
            "nombre": f"Prueba cancelacion {marca}",
            "telefono": "000000000",
        })
        assert response.status_code == 201, response.get_json()
        cliente_id = response.get_json()["id"]

        response = client.post("/api/servicios", json={
            "nombre": f"Prueba cancelacion {marca}",
            "precio": "30.00",
            "duracion_minutos": 60,
        })
        assert response.status_code == 201, response.get_json()
        servicio_id = response.get_json()["id"]

        payload = {
            "cliente_id": cliente_id,
            "servicio_id": servicio_id,
            "inicio": inicio_local,
        }

        response = client.post("/api/reservas", json=payload)
        assert response.status_code == 201, response.get_json()
        reserva_id = response.get_json()["id"]

        response = client.get(f"/api/reservas/{reserva_id}")
        assert response.status_code == 200
        assert response.get_json()["estado"] == "Confirmada"
        assert response.get_json()["cliente_id"] == cliente_id

        response = client.get("/api/reservas")
        assert response.status_code == 200
        assert any(
            item["id"] == reserva_id for item in response.get_json()
        )
        print("Consulta individual y listado: OK")

        response = client.post(f"/api/reservas/{reserva_id}/cancelar")
        assert response.status_code == 200, response.get_json()
        cancelada = response.get_json()
        assert cancelada["estado"] == "Cancelada"
        assert cancelada["cancelado_en"] is not None
        print("Cancelacion con fecha y registro conservado: OK")

        response = client.post(f"/api/reservas/{reserva_id}/cancelar")
        assert response.status_code == 200
        assert response.get_json() == cancelada
        print("Cancelacion repetida sin alterar fecha: OK")

        response = client.post("/api/reservas", json=payload)
        assert response.status_code == 201, response.get_json()
        nueva_id = response.get_json()["id"]
        assert nueva_id != reserva_id
        print("Horario liberado y nueva reserva aceptada: OK")

        # Simular el reloj después del inicio sin modificar fechas en MySQL.
        with patch(
            "src.reservas.repositories.reservas.ahora_utc",
            return_value=inicio + timedelta(minutes=1),
        ):
            response = client.post(
                f"/api/reservas/{nueva_id}/cancelar"
            )
        assert response.status_code == 409, response.get_json()

        response = client.get(f"/api/reservas/{nueva_id}")
        assert response.get_json()["estado"] == "Confirmada"
        print("Reserva iniciada rechazada con reloj simulado: OK")

        assert client.get("/api/reservas/0").status_code == 404
        assert client.post(
            "/api/reservas/0/cancelar"
        ).status_code == 404
        print("Reserva inexistente: OK")

    print("ENSAYO ACT-08 COMPLETADO")
    print("Reserva cancelada:", reserva_id)
    print("Reserva confirmada de reemplazo:", nueva_id)


if __name__ == "__main__":
    verificar()