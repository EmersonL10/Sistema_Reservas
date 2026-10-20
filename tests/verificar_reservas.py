from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from threading import Barrier
from uuid import uuid4
from zoneinfo import ZoneInfo

from src.reservas import create_app
from src.reservas.db import get_connection


LIMA = ZoneInfo("America/Lima")


def texto_local(fecha_utc):
    return (
        fecha_utc.replace(tzinfo=timezone.utc)
        .astimezone(LIMA)
        .strftime("%Y-%m-%dT%H:%M")
    )


def verificar():
    app = create_app()
    app.config["TESTING"] = True
    marca = uuid4().hex[:8]

    # Buscar una fecha posterior a las reservas confirmadas existentes.
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

    with app.test_client() as client:
        response = client.post("/api/clientes", json={
            "nombre": f"Prueba reservas {marca}",
            "telefono": "000000000",
        })
        assert response.status_code == 201, response.get_json()
        cliente_id = response.get_json()["id"]

        response = client.post("/api/servicios", json={
            "nombre": f"Prueba reservas {marca}",
            "precio": "25.50",
            "duracion_minutos": 60,
        })
        assert response.status_code == 201, response.get_json()
        servicio_id = response.get_json()["id"]

        base = {
            "cliente_id": cliente_id,
            "servicio_id": servicio_id,
            "inicio": texto_local(inicio),
        }

        response = client.post("/api/reservas", json=base)
        assert response.status_code == 201, response.get_json()
        primera = response.get_json()
        assert primera["estado"] == "Confirmada"
        assert primera["precio_aplicado"] == "25.50"
        assert primera["duracion_minutos"] == 60
        assert datetime.fromisoformat(primera["fin"]) - (
            datetime.fromisoformat(primera["inicio"])
        ) == timedelta(minutes=60)
        print("Registro valido y duracion: OK; id =", primera["id"])

        response = client.post("/api/reservas", json={
            **base,
            "inicio": texto_local(inicio + timedelta(minutes=30)),
        })
        assert response.status_code == 409, response.get_json()
        alternativas = response.get_json()["alternativas"]
        assert len(alternativas) == 5

        fechas = [
            datetime.fromisoformat(item["inicio"])
            for item in alternativas
        ]
        assert fechas == sorted(fechas)

        solicitado = inicio + timedelta(minutes=30)
        for opcion in alternativas:
            opcion_inicio = datetime.fromisoformat(
                opcion["inicio"]
            ).astimezone(timezone.utc).replace(tzinfo=None)
            opcion_fin = datetime.fromisoformat(
                opcion["fin"]
            ).astimezone(timezone.utc).replace(tzinfo=None)

            assert opcion_fin - opcion_inicio == timedelta(minutes=60)
            assert solicitado <= opcion_inicio <= (
                solicitado + timedelta(days=7)
            )
            assert (opcion_inicio - solicitado).total_seconds() % 1800 == 0
            assert not (
                opcion_inicio < inicio + timedelta(minutes=60)
                and opcion_fin > inicio
            )

        print("Superposicion rechazada y cinco alternativas validas: OK")

        response = client.post("/api/reservas", json={
            **base,
            "inicio": texto_local(inicio + timedelta(minutes=60)),
        })
        assert response.status_code == 201, response.get_json()
        print("Reserva consecutiva sin superposicion: OK")

        response = client.post("/api/reservas", json={
            **base,
            "inicio": texto_local(
                datetime.now(timezone.utc).replace(tzinfo=None)
                - timedelta(days=1)
            ),
        })
        assert response.status_code == 400, response.get_json()

        response = client.post("/api/reservas", json={
            **base, "inicio": "fecha-invalida"
        })
        assert response.status_code == 400, response.get_json()

        response = client.post("/api/reservas", json={
            **base, "cliente_id": True
        })
        assert response.status_code == 400, response.get_json()

        response = client.post("/api/reservas", json={
            **base, "cliente_id": 18446744073709551615
        })
        assert response.status_code == 404, response.get_json()

        response = client.post("/api/reservas", json={
            **base, "servicio_id": 18446744073709551615
        })
        assert response.status_code == 404, response.get_json()

        print("Fechas, identificadores y referencias invalidas: OK")

    payload_concurrente = {
        **base,
        "inicio": texto_local(inicio + timedelta(days=1)),
    }
    barrera = Barrier(2)

    def enviar():
        with app.test_client() as client:
            barrera.wait(timeout=10)
            response = client.post(
                "/api/reservas", json=payload_concurrente
            )
            return response.status_code, response.get_json()

    with ThreadPoolExecutor(max_workers=2) as executor:
        futuros = [executor.submit(enviar) for _ in range(2)]
        resultados = [futuro.result(timeout=30) for futuro in futuros]

    assert sorted(status for status, _ in resultados) == [201, 409], resultados

    inicio_concurrente = inicio + timedelta(days=1)
    with app.app_context():
        connection = get_connection()
        try:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM reservas
                    WHERE agenda_id = 1
                      AND estado = 'Confirmada'
                      AND inicio_utc < %s
                      AND fin_utc > %s
                    """,
                    (
                        inicio_concurrente + timedelta(minutes=60),
                        inicio_concurrente,
                    ),
                )
                assert cursor.fetchone()[0] == 1
            finally:
                cursor.close()
        finally:
            connection.close()

    print("Concurrencia: una respuesta 201, otra 409 y una reserva: OK")
    print("ENSAYO ACT-07 COMPLETADO")
    print("Cliente ficticio:", cliente_id, "Servicio ficticio:", servicio_id)


if __name__ == "__main__":
    verificar()