# Requerimientos del Sistema de Gestión de Reservas

## 1. Identificación

- Actividad: ACT-01.
- Issue: #1.
- Responsable: EmersonL10.
- Modalidad: individual.
- Fecha de elaboración: 19/10/2026.
- Fecha límite de entrega: 21/10/2026.
- Estado: propuesta pendiente de autorrevisión.

## 2. Objetivo

Centralizar el registro y consulta de clientes, servicios y reservas,
reemplazando la información dispersa en llamadas, WhatsApp y hojas
de cálculo.

## 3. Alcance de la primera versión

### RF-01. Registrar clientes

Entrada: nombre, teléfono y correo electrónico opcional.

Resultado esperado:
- Crear un cliente con identificador único.
- Mostrar confirmación y permitir su consulta.
- Rechazar nombre o teléfono vacíos.
- Validar el formato del correo cuando se proporcione.
- Conservar el teléfono como texto para mantener prefijos y ceros.

### RF-02. Modificar información de clientes

Entrada: identificador del cliente y datos modificados.

Resultado esperado:
- Actualizar los datos válidos conservando el identificador.
- Aplicar las mismas validaciones que en el registro.
- Informar cuando el cliente no exista.
- No modificar sus reservas históricas.

### RF-03. Consultar clientes

Entrada: solicitud del listado o identificador de un cliente.

Resultado esperado:
- Mostrar los clientes registrados o el detalle solicitado.
- Informar cuando el listado esté vacío o el cliente no exista.

### RF-04. Registrar servicios con precio y duración

Entrada: nombre, precio en soles y duración en minutos.

Resultado esperado:
- Crear un servicio con identificador único.
- Rechazar nombres vacíos.
- Admitir precios mayores o iguales a cero, con hasta dos decimales.
- Exigir duración expresada en minutos enteros mayores que cero.
- Evitar errores de precisión en el almacenamiento del precio.

### RF-05. Consultar servicios

Entrada: solicitud del listado o identificador de un servicio.

Resultado esperado:
- Mostrar nombre, precio y duración.
- Informar cuando no existan servicios o el identificador no exista.

### RF-06. Registrar reservas

Entrada: cliente, servicio, fecha y hora de inicio.

Resultado esperado:
- Verificar que el cliente y el servicio existan.
- Validar fecha y hora y exigir un inicio posterior al momento actual.
- Calcular la finalización con la duración del servicio.
- Comprobar disponibilidad.
- Crear una reserva con identificador único y estado Confirmada.
- Rechazar datos inválidos sin guardar registros parciales.

### RF-07. Consultar reservas

Entrada: solicitud del listado o identificador de una reserva.

Resultado esperado:
- Mostrar cliente, servicio, inicio, finalización y estado.
- Incluir reservas confirmadas y canceladas.
- Informar cuando el listado esté vacío o la reserva no exista.

### RF-08. Cancelar reservas

Entrada: identificador de una reserva.

Resultado esperado:
- Permitir cancelar reservas confirmadas cuyo inicio sea futuro.
- Solicitar confirmación en la interfaz.
- Cambiar el estado a Cancelada y registrar el momento de cancelación.
- Conservar el registro.
- Liberar su disponibilidad.
- Repetir la solicitud sin duplicar efectos ni cambiar la fecha
  de una cancelación ya realizada.
- Rechazar la cancelación de una reserva confirmada ya iniciada.
- Informar cuando la reserva no exista.

## 4. Supuestos y decisiones de alcance

Las siguientes reglas no están detalladas en la consigna.
Se proponen para hacer verificable la primera versión y deben
confirmarse durante la autorrevisión:

- La empresa dispone de una sola agenda y capacidad para atender
  una reserva a la vez, independientemente del servicio.
- No se gestionan empleados, sucursales ni recursos múltiples.
- No se aplican horarios comerciales en esta versión.
- La zona horaria de operación es America/Lima.
- El operador administra clientes, servicios y reservas.
- No se incluye autenticación en este prototipo académico local.
  No se considera preparado para exposición pública.

## 5. Reglas de integridad y disponibilidad

- Todos los campos obligatorios se validan en el backend.
- Los nombres no pueden contener únicamente espacios.
- Los identificadores se generan automáticamente.
- No se impone unicidad de nombre, teléfono o correo de clientes,
  porque la consigna no define un identificador personal único.
- El precio y la duración aplicados se conservan en la reserva,
  evitando que futuros cambios alteren su información histórica.
- Dos reservas confirmadas son incompatibles cuando:
  inicio_nuevo < fin_existente y fin_nuevo > inicio_existente.
- Una reserva puede comenzar exactamente cuando termina otra.
- Las reservas canceladas no bloquean disponibilidad.
- La comprobación de disponibilidad y el registro deben ser atómicos.
- Dos solicitudes simultáneas incompatibles no pueden aceptarse ambas.
- Los estados de la primera versión son Confirmada y Cancelada.
- La transición permitida es Confirmada → Cancelada.
- No se permite reactivar ni eliminar reservas desde la aplicación.

## 6. Requisitos de calidad

- Los datos deben conservarse después de reiniciar la aplicación.
- Los errores deben ser comprensibles y no revelar información interna.
- Los formularios deben tener etiquetas y permitir uso por teclado.
- Las pantallas deben ser utilizables en anchos de 360 px y 1280 px.
- La entrega debe incluir instrucciones reproducibles de ejecución.
- Las pruebas utilizarán datos ficticios.
- La primera versión debe permitir el recorrido:
  cliente → servicio → reserva → consulta → cancelación.

## 7. Funcionalidades futuras

Fuera de v1.0.0 y de la entrega del 21/10/2026:

- ACT-16: recordatorios automáticos.
- ACT-17: reportes.
- ACT-18: dashboard de indicadores.
- ACT-19: pagos en línea.
- ACT-20: historial de clientes.

Las fechas futuras del tablero son tentativas, no compromisos
de implementación para esta evaluación.

## 8. Trazabilidad inicial

| Requisito | Actividad principal | Interfaz | Verificación |
|---|---|---|---|
| RF-01, RF-02, RF-03 | ACT-05 | ACT-09 | ACT-10 |
| RF-04, RF-05 | ACT-06 | ACT-09 | ACT-10 |
| RF-06 | ACT-07 | ACT-09 | ACT-10 |
| RF-07, RF-08 | ACT-08 | ACT-09 | ACT-10 |

Las referencias reales a commits, Pull Requests, revisión e integración
se incorporarán conforme se produzcan, sin anticipar evidencias.