# Bitácora del proyecto

## Datos generales

- Proyecto: Sistema de Gestión de Reservas.
- Responsable: EmersonL10.
- Modalidad: individual.
- Repositorio: https://github.com/EmersonL10/Sistema_Reservas
- Entrega prevista: 21/10/2026.

## Registro inicial — 19/10/2026

### Preparación del repositorio

- Se publicó README.md con problema, objetivo, alcance inicial
  y funcionalidades futuras.
- Commit publicado: 0ce5dbd.
- Se verificó develop sincronizada con origin/develop
  y sin cambios pendientes.

### Planificación de actividades

- Se registraron 20 actividades en GitHub Issues y Projects.
- ACT-01 a ACT-15 corresponden a la entrega.
- ACT-16 a ACT-20 corresponden a mejoras futuras.
- La captura del tablero muestra 19 actividades pendientes
  y ACT-01 en Por hacer en ese momento.
- Se configuraron responsable, prioridad, fecha de entrega
  y bloqueo. La revisión completa de los 20 registros sigue pendiente.

### ACT-01 — Definición de requisitos

- Issue: https://github.com/EmersonL10/Sistema_Reservas/issues/1
- Rama: docs/act-01-requerimientos.
- Se creó docs/requerimientos.md con RF-01 a RF-08,
  reglas de negocio, supuestos y trazabilidad inicial.
- Los supuestos permanecen pendientes de autorrevisión.
- Se verificó la existencia y lectura del archivo.
- La lectura inicial de PowerShell mostró caracteres incorrectos.
- Se repitió la lectura con -Encoding UTF8 y las tildes
  se visualizaron correctamente; no se modificó el documento.
- Al registrar esta entrada, los requisitos todavía no tienen
  commit, push, Pull Request ni integración.

## Flujo de trabajo acordado

Crear rama → Desarrollar → Commit → Push → Pull Request
→ Revisión y pruebas → Decisión de aprobación → Merge.

Las revisiones son propias del autor y no constituyen
aprobación independiente de otro integrante.

## Registro de próximos hitos

Cada entrada incluirá:
- Fecha y actividad.
- Acción y motivo.
- Resultado observado.
- Comandos ejecutados, cuando corresponda.
- Evidencia disponible.
- Referencias reales a commits, Issues y Pull Requests.

Los hitos se registrarán cuando ocurran, sin anticipar resultados.

## Cierre de ACT-01 e inicio de ACT-02 — 19/10/2026

### Requisitos integrados

- PR: https://github.com/EmersonL10/Sistema_Reservas/pull/21
- Commit inicial de documentación: b94a330.
- Corrección de validación temporal: 6e9cdd4.
- Ampliación de disponibilidad y alternativas: b932527.
- Autorrevisión previa a la integración:
  https://github.com/EmersonL10/Sistema_Reservas/pull/21#issuecomment-6277977528
- Commit de merge: 5a30164b1b44f36bf2b7e2ddca83baac00dd5d67.
- Integración: 19/10/2026 a las 16:39, hora de Lima.
- Se verificó develop sincronizado y sin cambios pendientes.
- ACT-01 aparece cerrada y en Hecho en el tablero.
- El cierre corresponde a la especificación, no a código funcional.

### Selección tecnológica de ACT-02

- Rama: docs/act-02-arquitectura.
- Python observado: 3.13.14.
- Node.js observado: v24.18.0; no se requiere para la solución elegida.
- MySQL verificado mediante SELECT VERSION(): 8.0.46.
- Se sustituyó la propuesta inicial de SQLite por MySQL
  por elección del responsable.
- Se seleccionaron Flask, HTML/CSS, Jinja y MySQL Connector/Python.
- Se redactó docs/arquitectura.md y se actualizó README.md.
- La instalación del framework, del conector y el arranque
  permanecen pendientes; no se afirma compatibilidad verificada.
  ## Implementación base de ACT-03

- Se preparó la rama feature/act-03-estructura-base.
- Se verificaron Flask 3.1.3 y MySQL Connector/Python 26.7.0.
- Se verificó la disponibilidad de America/Lima.
- Se creó la aplicación con fábrica create_app y ruta inicial.
- El responsable comprobó su apertura en http://127.0.0.1:5000.
- Se incorporaron .gitignore, requirements.txt y .env.example.
- Se corrigió la configuración para leer variables después de cargar .env.
- El responsable confirmó un nuevo arranque satisfactorio.
- La base de datos y la conexión todavía no están implementadas.
- Durante la revisión del PR #23 se detectó una contraseña escrita
  en la plantilla y en el valor predeterminado de configuración.
- Se corrigieron ambos archivos para utilizar un valor vacío.
- La revisión del PR continúa pendiente de comprobar la corrección.
## Implementación y verificación de ACT-04 — 20/10/2026

- Se creó el esquema sistema_reservas y sus cuatro tablas.
- Se corrigieron advertencias del operador BINARY utilizando CAST.
- Se verificaron las restricciones activas y la agenda principal.
- Se configuró reservas_app con SELECT, INSERT y UPDATE.
- Se resolvió el rechazo de autenticación haciendo coincidir
  la contraseña configurada en MySQL y el archivo local .env.
- Se verificó la conexión desde Python y el comando Flask check-db.
- Se ejecutaron cinco pruebas de integridad con resultado OK.
- Durante las pruebas se corrigieron el descubrimiento del archivo,
  la expectativa del código de error referencial y la ubicación
  de la variable utilizada para inspeccionar la excepción.
- Las pruebas revierten sus registros mediante rollback.
- La revisión del Pull Request y la integración siguen pendientes.
## Desarrollo y verificación de ACT-05 — 20/10/2026

- Se implementaron repositorio, validaciones y rutas de clientes.
- Se comprobaron registro, modificación, listado y consulta individual.
- Se verificaron respuestas 400 para datos inválidos y 404 para
  identificadores inexistentes.
- Se comprobó que una modificación inválida no alteró el cliente.
- El cliente ficticio id 13 persistió desde un nuevo proceso Python.
- Las cinco pruebas de integridad existentes volvieron a pasar.
- Resultados documentados en docs/pruebas-clientes.md.
- Revisión e integración del módulo pendientes.
## Desarrollo y verificación de ACT-06 — 20/10/2026

- Se implementaron registro, listado y consulta individual de servicios.
- Se utilizó Decimal para validar y conservar importes exactos.
- El precio se devuelve como texto decimal con dos posiciones.
- El servicio ficticio id 16 se registró con precio 50.25
  y duración de 60 minutos.
- Once entradas inválidas fueron rechazadas sin insertar registros.
- La consulta de un servicio inexistente devolvió HTTP 404.
- Se verificó persistencia entre instancias y desde un nuevo proceso.
- Las cinco pruebas de integridad volvieron a pasar.
- El ensayo reproducible está en tests/verificar_servicios.py.
- El ensayo conserva un servicio ficticio por ejecución.
- No se reinició MySQL ni se utilizó un esquema de pruebas separado.
- Revisión e integración pendientes.
## Desarrollo y verificación de ACT-07 — 20/10/2026

- Se implementó POST /api/reservas.
- Se validaron identificadores, fecha futura y conversión Lima/UTC.
- Se conservaron precio y duración aplicados a la reserva.
- Se implementó bloqueo transaccional de la agenda antes de
  comprobar disponibilidad e insertar.
- El ensayo tests/verificar_reservas.py terminó satisfactoriamente.
- Reserva inicial generada: id 19.
- Cliente y servicio ficticios generados: ambos con id 20.
- Se verificaron superposición rechazada, cinco alternativas,
  reserva consecutiva y entradas inválidas.
- Dos solicitudes concurrentes generaron una respuesta 201,
  una respuesta 409 y una sola reserva para el intervalo.
- El ensayo conservó datos ficticios en el esquema local.
- La concurrencia se comprobó en un escenario de dos solicitudes;
  no constituye una prueba de carga.
- Revisión e integración pendientes.
- - Durante la revisión del PR #27 se detectó un posible desbordamiento
  al convertir fechas extremas de Lima a UTC.
- Se incorporó un error de validación controlado y dos pruebas
  unitarias de fechas.
- La suite ejecutó siete pruebas con resultado satisfactorio.
## Desarrollo y verificación de ACT-08 — 20/10/2026

- Se implementaron listado, consulta y cancelación de reservas.
- La cancelación utiliza el mismo bloqueo de agenda que el registro.
- El ensayo tests/verificar_cancelacion.py terminó satisfactoriamente.
- Se verificó cancelación repetida sin cambiar su fecha original.
- La reserva 28 quedó cancelada y la 29 fue aceptada en su horario.
- Se rechazó una cancelación posterior al inicio mediante reloj simulado.
- Las reservas inexistentes devolvieron HTTP 404.
- Se verificó la cancelación persistida desde un nuevo proceso.
- Las siete pruebas automatizadas existentes volvieron a pasar.
- El ensayo conservó datos ficticios en el esquema local.
- La confirmación visual permanece pendiente de ACT-09.
- Revisión e integración pendientes.
  ## Desarrollo y verificación de ACT-09 — 20/10/2026

- Se implementó la interfaz de clientes, servicios y reservas.
- Las tres tablas cargaron datos de MySQL.
- Se incorporaron edición de clientes, registro de servicios,
  registro de reservas y cancelación con confirmación.
- Durante la prueba visual se detectó falta de indicación
  de la alternativa de horario seleccionada.
- Se corrigió mediante resaltado, aria-pressed y mensaje de selección.
- El responsable confirmó el funcionamiento de la selección
  y del recorrido visual solicitado.
- Se solicitaron comprobaciones a 360 y 1280 px y navegación
  por teclado; los resultados específicos deben registrarse
  antes de dar esos criterios por verificados.
- Revisión e integración pendientes.
  ## Validación integral de ACT-10 — 21/10/2026

- Se inició la rama test/act-10-validacion-integral desde 1471738.
- Se verificaron conexión y sintaxis JavaScript.
- Se agregaron ocho pruebas de API en el commit 19be696.
- La suite completa ejecutó 15 pruebas con resultado OK.
- Los errores MySQL 2003 fueron simulados deliberadamente.
- Se consolidaron cobertura, evidencias y limitaciones
  en docs/pruebas.md.
- Revisión e integración de ACT-10 pendientes.
## Consolidación de revisiones — ACT-11 — 21/10/2026

- Se consultaron los PR integrados y el detalle del PR #23.
- Se verificó que su autorrevisión precedió al merge.
- Se documentaron corrección, comentario, fechas y commit de integración
  en docs/revisiones.md.
- Se distinguió autorrevisión de aprobación independiente.