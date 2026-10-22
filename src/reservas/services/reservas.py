from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


LIMA = ZoneInfo("America/Lima")


class ReservaError(ValueError):
    def __init__(self, mensaje, status=400, alternativas=None):
        super().__init__(mensaje)
        self.status = status
        self.alternativas = alternativas or []


def validar_reserva(payload):
    if not isinstance(payload, dict):
        raise ReservaError("Se requiere un objeto JSON.")

    for campo in ("cliente_id", "servicio_id"):
        valor = payload.get(campo)
        if type(valor) is not int or not 1 <= valor <= 18446744073709551615:
            raise ReservaError(
                f"{campo} debe ser un identificador entero positivo."
            )

    valor_inicio = payload.get("inicio")
    if not isinstance(valor_inicio, str):
        raise ReservaError("El inicio es obligatorio.")

    try:
        inicio_local = datetime.strptime(
            valor_inicio, "%Y-%m-%dT%H:%M"
        ).replace(tzinfo=LIMA)
    except ValueError:
        raise ReservaError(
            "El inicio debe tener formato AAAA-MM-DDTHH:MM."
        ) from None

    # MySQL DATETIME admite años desde 1000.
    if inicio_local.year < 1000:
        raise ReservaError("La fecha está fuera del rango permitido.")

    try:
        inicio_utc = inicio_local.astimezone(timezone.utc).replace(
            tzinfo=None
        )
    except (OverflowError, ValueError):
        raise ReservaError(
            "La fecha está fuera del rango permitido."
        ) from None

    if inicio_utc <= ahora_utc():
        raise ReservaError("El inicio debe ser posterior al momento actual.")

    return {
        "cliente_id": payload["cliente_id"],
        "servicio_id": payload["servicio_id"],
        "inicio_utc": inicio_utc,
    }


def ahora_utc():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def calcular_fin(inicio, duracion):
    try:
        return inicio + timedelta(minutes=duracion)
    except OverflowError:
        raise ReservaError(
            "La fecha final está fuera del rango permitido."
        ) from None


def hay_superposicion(inicio, fin, intervalos):
    return any(
        inicio < ocupado_fin and fin > ocupado_inicio
        for ocupado_inicio, ocupado_fin in intervalos
    )


def formato_local(fecha_utc):
    return (
        fecha_utc.replace(tzinfo=timezone.utc)
        .astimezone(LIMA)
        .isoformat(timespec="minutes")
    )


def buscar_alternativas(inicio, duracion, intervalos):
    alternativas = []
    candidato = inicio

    try:
        limite = inicio + timedelta(days=7)
    except OverflowError:
        limite = datetime.max

    momento_actual = ahora_utc()

    while candidato <= limite and len(alternativas) < 5:
        try:
            fin = candidato + timedelta(minutes=duracion)
        except OverflowError:
            break

        if (
            candidato > momento_actual
            and not hay_superposicion(candidato, fin, intervalos)
        ):
            alternativas.append({
                "inicio": formato_local(candidato),
                "fin": formato_local(fin),
            })

        try:
            candidato += timedelta(minutes=30)
        except OverflowError:
            break

    return alternativas