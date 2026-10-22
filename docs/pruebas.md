# Informe de verificación — ACT-10

## Identificación

- Fecha: 21/10/2026.
- Responsable: EmersonL10.
- Versión funcional evaluada: develop, commit 1471738.
- Pruebas de API incorporadas en el commit 19be696.
- Modalidad: individual, entorno local.

## Entorno observado

- Python 3.13.14.
- Flask 3.1.3.
- MySQL Connector/Python 26.7.0.
- MySQL Server 8.0.46.
- Sesión de conexión: UTC.
- Presentación de horarios: America/Lima.

## Ejecución del 21/10/2026

Comando:

    .\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v

Resultado: 15 pruebas ejecutadas, todas satisfactorias.

| Tipo | Archivo | Pruebas | Resultado |
|---|---|---:|---|
| API con repositorios simulados | test_api_validaciones.py | 8 | OK |
| Reglas de fechas sin conexión a datos | test_fechas_reservas.py | 2 | OK |
| Integridad contra MySQL real | test_integridad_bd.py | 5 | OK |

Los mensajes de error MySQL 2003 durante las pruebas de API
fueron provocados mediante simulaciones. No representan
una caída real observada del servidor.

## Comprobaciones complementarias del 21/10/2026

- check-db: conexión correcta a sistema_reservas,
  usuario reservas_app@localhost, sesión +00:00 y agenda 1.
- node --check: sin errores de sintaxis reportados.

## Cobertura y evidencias previas

Las comprobaciones siguientes se realizaron durante el desarrollo
el 20/10/2026; no se presentan como ejecuciones nuevas de ACT-10.

| Requisito | Comprobación observada | Referencia |
|---|---|---|
| RF-01 | Registro de cliente y generación de identificador | PR #25; docs/pruebas-clientes.md |
| RF-02 | Modificación válida y rechazo sin alterar datos | PR #25; docs/pruebas-clientes.md |
| RF-03 | Consulta individual, listado e inexistente | PR #25 |
| RF-04 | Registro de servicio, precio exacto y validaciones | PR #26; tests/verificar_servicios.py |
| RF-05 | Consulta individual, listado e inexistente | PR #26 |
| RF-06 | Registro, superposición, alternativas y concurrencia | PR #27; tests/verificar_reservas.py |
| RF-07 | Listado y consulta de reservas | PR #28; tests/verificar_cancelacion.py |
| RF-08 | Cancelación, repetición y liberación del horario | PR #28; tests/verificar_cancelacion.py |

Persistencia observada desde procesos nuevos:
- Cliente 13.
- Servicio 16.
- Reserva cancelada 28.

La interfaz se verificó durante ACT-09. El responsable confirmó
recorrido funcional, selección visible de alternativas,
uso a 360 y 1280 px y navegación por teclado.
Referencia: PR #29 y capturas del responsable.

## Hallazgos y correcciones durante el desarrollo

| Hallazgo | Corrección | Referencia |
|---|---|---|
| Contraseña escrita en configuración y plantilla | Valores vacíos y configuración local | PR #23 |
| Operador SQL BINARY obsoleto | Sustitución por CAST | ACT-04; PR #24 |
| Código referencial esperado distinto al observado | Verificar códigos 1216/1452, SQLSTATE y datos intactos | PR #24 |
| Desbordamiento al convertir una fecha extrema | Error de validación y prueba unitaria | PR #27 |
| Alternativa seleccionada sin indicación visual suficiente | Mensaje, aria-pressed y estilo de selección | PR #29 |

La clasificación y el seguimiento formal de incidencias
deben relacionarse con sus evidencias, sin inventar nuevos defectos.

## Limitaciones

- No se realizó prueba de carga.
- La concurrencia observada corresponde a dos solicitudes simultáneas.
- Las pruebas de integridad usan transacciones con rollback
  sobre el esquema local, no un esquema de pruebas separado.
- Los ensayos funcionales conservaron datos ficticios.
- Los contadores autoincrementales pueden avanzar.
- No se reinició el servidor MySQL.
- La instalación desde una copia limpia sigue pendiente.
- No se ha publicado todavía una versión estable.
- El sistema es un prototipo local sin autenticación.

## Conclusión de esta ejecución

Las 15 pruebas ejecutadas resultaron satisfactorias.
Los resultados respaldan los escenarios descritos; no implican
ausencia absoluta de defectos ni validación de producción.