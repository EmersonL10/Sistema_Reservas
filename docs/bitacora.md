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