# Verificación del módulo de clientes — ACT-05

Fecha: 20/10/2026.
Modalidad: pruebas mediante el cliente de Flask contra MySQL local.
Datos: ficticios. Cliente generado: id 13.

| Escenario | Resultado |
|---|---|
| Registrar cliente válido | HTTP 201; identificador generado |
| Consultar cliente registrado | HTTP 200; datos correctos |
| Consultar listado | HTTP 200; contiene el cliente |
| Modificar cliente | HTTP 200; conserva identificador |
| Modificar con nombre vacío | HTTP 400; datos anteriores intactos |
| Consultar cliente inexistente | HTTP 404 |
| Modificar cliente inexistente | HTTP 404 |
| Consultar desde otra instancia Flask | Datos conservados |
| Consultar desde un nuevo proceso Python | Datos conservados |
| Regresión de integridad de ACT-04 | Cinco pruebas satisfactorias |

## Limitaciones

- Las comprobaciones de clientes se ejecutaron mediante scripts
  de terminal; todavía no forman una suite automatizada versionada.
- Se conservó un cliente ficticio en sistema_reservas.
- No se reinició el servidor MySQL.
- La interfaz visual permanece pendiente de ACT-09.