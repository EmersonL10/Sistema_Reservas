from decimal import Decimal, InvalidOperation


def validar_servicio(payload):
    if not isinstance(payload, dict):
        raise ValueError("Se requiere un objeto JSON.")

    nombre = payload.get("nombre")
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre es obligatorio.")
    nombre = nombre.strip()
    if len(nombre) > 120:
        raise ValueError("El nombre admite hasta 120 caracteres.")

    valor_precio = payload.get("precio")
    if (
        isinstance(valor_precio, bool)
        or not isinstance(valor_precio, (str, int, float))
        or len(str(valor_precio)) > 40
    ):
        raise ValueError("El precio debe ser un importe válido.")

    try:
        precio = Decimal(str(valor_precio))
    except InvalidOperation:
        raise ValueError("El precio debe ser numérico.") from None

    if (
        not precio.is_finite()
        or precio < 0
        or precio > Decimal("99999999.99")
    ):
        raise ValueError("El precio está fuera del rango permitido.")

    if precio.as_tuple().exponent < -2:
        raise ValueError("El precio admite hasta dos decimales.")

    duracion = payload.get("duracion_minutos")
    if type(duracion) is not int or not 1 <= duracion <= 65535:
        raise ValueError(
            "La duración debe ser un entero entre 1 y 65535 minutos."
        )

    return {
        "nombre": nombre,
        "precio": precio.quantize(Decimal("0.01")),
        "duracion_minutos": duracion,
    }