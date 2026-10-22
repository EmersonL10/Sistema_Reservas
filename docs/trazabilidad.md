# Matriz de trazabilidad — ACT-13

## Identificación

- Proyecto: Sistema de Gestión de Reservas.
- Responsable de todas las actividades: EmersonL10.
- Modalidad: individual.
- Fecha de consolidación: 21/10/2026.
- Base de integración consultada: 4272f82.
- Requisitos: [requerimientos.md](requerimientos.md).
- Resultados y limitaciones: [pruebas.md](pruebas.md).

## Cadena de trazabilidad

Requerimiento → Issue → Responsable → Desarrollo → Revisión
→ Integración → Evidencia de prueba.

## Requisitos de la primera versión

| Requisito | Actividad | Responsable | Commit de desarrollo | PR y revisión | Merge en develop | Evidencia |
|---|---|---|---|---|---|---|
| RF-01: registrar clientes | [ACT-05](https://github.com/EmersonL10/Sistema_Reservas/issues/5) | EmersonL10 | dfce1a8 | [PR #25](https://github.com/EmersonL10/Sistema_Reservas/pull/25) | fa37eec | Registro HTTP 201; cliente 13 |
| RF-02: modificar clientes | [ACT-05](https://github.com/EmersonL10/Sistema_Reservas/issues/5) | EmersonL10 | dfce1a8 | [PR #25](https://github.com/EmersonL10/Sistema_Reservas/pull/25) | fa37eec | Modificación, rechazo sin alterar datos y persistencia |
| RF-03: consultar clientes | [ACT-05](https://github.com/EmersonL10/Sistema_Reservas/issues/5) | EmersonL10 | dfce1a8 | [PR #25](https://github.com/EmersonL10/Sistema_Reservas/pull/25) | fa37eec | Listado, detalle e inexistente |
| RF-04: registrar servicios con precio y duración | [ACT-06](https://github.com/EmersonL10/Sistema_Reservas/issues/6) | EmersonL10 | e28dddf | [PR #26](https://github.com/EmersonL10/Sistema_Reservas/pull/26) | 94a9566 | tests/verificar_servicios.py; servicio 16 |
| RF-05: consultar servicios | [ACT-06](https://github.com/EmersonL10/Sistema_Reservas/issues/6) | EmersonL10 | e28dddf | [PR #26](https://github.com/EmersonL10/Sistema_Reservas/pull/26) | 94a9566 | Listado, detalle e inexistente |
| RF-06: registrar reservas y ofrecer alternativas | [ACT-07](https://github.com/EmersonL10/Sistema_Reservas/issues/7) | EmersonL10 | 21d7dfa; corrección 0f16eee | [PR #27](https://github.com/EmersonL10/Sistema_Reservas/pull/27) | 6c1eee0 | tests/verificar_reservas.py; concurrencia 201/409 |
| RF-07: consultar reservas | [ACT-08](https://github.com/EmersonL10/Sistema_Reservas/issues/8) | EmersonL10 | 12d48cb | [PR #28](https://github.com/EmersonL10/Sistema_Reservas/pull/28) | 13a5537 | tests/verificar_cancelacion.py; listado y detalle |
| RF-08: cancelar reservas | [ACT-08](https://github.com/EmersonL10/Sistema_Reservas/issues/8) | EmersonL10 | 12d48cb | [PR #28](https://github.com/EmersonL10/Sistema_Reservas/pull/28) | 13a5537 | Cancelación repetida, liberación y persistencia de reserva 28 |

Los PR contienen las conversaciones de autorrevisión.
La secuencia temporal se detalla explícitamente para el PR #25
en el apartado siguiente.

## Ejemplo completo: RF-01

1. Requisito: registrar clientes, definido en ACT-01.
2. Actividad: ACT-05, Issue #5.
3. Responsable: EmersonL10.
4. Desarrollo: dfce1a892464c110120068ba43048316d1365fd8.
5. Revisión:
   https://github.com/EmersonL10/Sistema_Reservas/pull/25#issuecomment-6296477420
6. Integración: fa37eec8c34dd0e68697344f33c9950f29dac2ee.
7. Prueba: registro del cliente ficticio 13 y consulta desde otro proceso,
   documentados en docs/pruebas-clientes.md.

Secuencia comprobada del 20/10/2026, hora de Lima:

| Evento | Hora |
|---|---|
| Commit de desarrollo | 11:59:11 |
| Comentario de autorrevisión | 12:02:00 |
| Merge | 12:02:28 |

## Interfaz y validación transversal

| Actividad | Desarrollo | PR | Merge | Evidencia |
|---|---|---|---|---|
| ACT-09: interfaz RF-01 a RF-08 | db23654; corrección 43e9356 | [#29](https://github.com/EmersonL10/Sistema_Reservas/pull/29) | 1471738 | Recorrido visual, alternativas, cancelación, tamaños y teclado confirmados por el responsable |
| ACT-10: validación | 19be696 y documentación asociada | [#31](https://github.com/EmersonL10/Sistema_Reservas/pull/31) | 5fef521 | 15 pruebas satisfactorias; docs/pruebas.md |

## Archivos de implementación

- Clientes:
  src/reservas/routes/clientes.py,
  src/reservas/services/clientes.py,
  src/reservas/repositories/clientes.py.
- Servicios:
  src/reservas/routes/servicios.py,
  src/reservas/services/servicios.py,
  src/reservas/repositories/servicios.py.
- Reservas:
  src/reservas/routes/reservas.py,
  src/reservas/services/reservas.py,
  src/reservas/repositories/reservas.py.
- Persistencia: database/schema.sql y src/reservas/db.py.
- Interfaz: src/reservas/templates/index.html
  y src/reservas/static/.

## Mejoras futuras

ACT-16 a ACT-20 corresponden a recordatorios, reportes, dashboard,
pagos en línea e historial de clientes.

Permanecen fuera de la primera versión.
No se les atribuye implementación, pruebas ni integración funcional.

## Límites de la evidencia

- Revisión propia del autor, sin aprobación independiente.
- Las pruebas de API con simulaciones no acreditan persistencia.
- Los ensayos integrales utilizaron datos ficticios en el esquema local.
- Concurrencia observada con dos solicitudes, sin prueba de carga.
- La publicación de la versión estable sigue pendiente de ACT-14.
- Las capturas deben conservarse y seleccionarse para el informe final.

## Consultas utilizadas

    gh pr list --state merged --base develop --limit 40 --json number,url,mergeCommit

    gh pr view 25 --json commits,comments,mergedAt

Las fechas originales se obtuvieron en UTC y se convirtieron
a America/Lima.