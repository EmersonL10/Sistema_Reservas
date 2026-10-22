import re


EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def validar_cliente(payload):
    if not isinstance(payload, dict):
        raise ValueError("Se requiere un objeto JSON.")

    datos = {}

    for campo, limite in (("nombre", 120), ("telefono", 30)):
        valor = payload.get(campo)

        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                f"El campo {campo} es obligatorio y debe ser texto."
            )

        valor = valor.strip()
        if len(valor) > limite:
            raise ValueError(
                f"El campo {campo} admite hasta {limite} caracteres."
            )

        datos[campo] = valor

    email = payload.get("email")

    if email is None:
        datos["email"] = None
    elif not isinstance(email, str):
        raise ValueError("El correo debe ser texto.")
    else:
        email = email.strip()
        if email and (
            len(email) > 254 or EMAIL_PATTERN.fullmatch(email) is None
        ):
            raise ValueError("El formato del correo no es válido.")
        datos["email"] = email or None

    return datos