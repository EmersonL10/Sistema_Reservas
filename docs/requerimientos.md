# Requerimientos del Sistema de Gestión de Reservas

## 1. Identificación

- Actividad: ACT-01.
- Issue: #1.
- Responsable: EmersonL10.
- Modalidad: individual.
- Fecha de elaboración: 19/10/2026.
- Fecha límite de entrega: 21/10/2026.
- Estado: en autorrevisión documental.
- Pull Request relacionado: #21.

## 2. Objetivo

Centralizar el registro y consulta de clientes, servicios y reservas,
reemplazando la información dispersa en llamadas, WhatsApp y hojas
de cálculo.

## 3. Alcance de la primera versión

### RF-01. Registrar clientes

Entrada: nombre, teléfono y correo electrónico opcional.

Resultados esperados:

- Crear un cliente con identificador único.
- Mostrar confirmación y permitir su consulta.
- Rechazar nombre o teléfono vacíos.
- Validar el formato del correo cuando se proporcione.
- Conservar el teléfono como texto para mantener prefijos y ceros.

### RF-02. Modificar información de clientes

Entrada: identificador del cliente y datos modificados.

Resultados esperados:

- Actualizar los datos válidos conservando el identificador.
- Aplicar las mismas validaciones que en el registro.
- Informar cuando el cliente no exista.
- Conservar la asociación del cliente con sus reservas existentes.

### RF-03. Consultar clientes

Entrada: solicitud del listado o identificador de un cliente.

Resultados esperados:

- Mostrar los clientes registrados o el detalle solicitado.
- Informar cuando el listado esté vacío o el cliente no exista.

### RF-04. Registrar servicios con precio y duración

Entrada: nombre, precio en soles y duración en minutos.

Resultados esperados:

- Crear un servicio con identificador único.
- Rechazar nombres vacíos.
- Admitir precios mayores o iguales a cero, con hasta dos decimales.
- Exigir duración expresada en minutos enteros mayores que cero.
- Evitar errores de precisión en el almacenamiento del precio.

### RF-05. Consultar servicios

Entrada: solicitud del listado o identificador de un servicio.

Resultados esperados:

- Mostrar nombre, precio y duración.
- Informar cuando no existan servicios o el identificador no exista.

### RF-06. Registrar reservas y consultar alternativas disponibles

Entrada: cliente, servicio, fecha y hora de inicio.

Resultados esperados:

- Verificar que el cliente y el servicio existan.
- Validar fecha y hora y exigir un inicio posterior al momento actual.
- Calcular la finalización con la duración del servicio.
- Comprobar la disponibilidad de todo el intervalo solicitado.
- Si el intervalo está ocupado, rechazar el registro y mostrar
  horarios alternativos disponibles.
- Buscar alternativas desde el inicio solicitado, en pasos de
  30 minutos y hasta siete días después.
- Mostrar como máximo cinco alternativas, ordenadas desde la
  más próxima, cuyo intervalo completo esté libre y cuyo inicio
  sea posterior al momento actual.
- Si no existen alternativas en ese período, informar al operador
  y permitir consultar otra fecha.
- La consulta de alternativas no bloquea ni registra una reserva.
- Revalidar la disponibilidad al confirmar una alternativa,
  porque otro registro podría haber ocupado ese intervalo.
- Crear una reserva con identificador único y estado Confirmada.
- Rechazar datos inválidos sin guardar registros parciales.

### RF-07. Consultar reservas

Entrada: solicitud del listado o identificador de una reserva.

Resultados esperados:

- Mostrar cliente, servicio, inicio, finalización y estado.
- Incluir reservas confirmadas y canceladas.
- Informar cuando el listado esté vacío o la reserva no exista.

### RF-08. Cancelar reservas

Entrada: identificador de una reserva.

Resultados esperados:

- Permitir cancelar reservas confirmadas cuyo inicio sea futuro.
- Solicitar confirmación en la interfaz.
- Cambiar el estado a Cancelada y registrar el momento de cancelación.
- Conservar el registro.
- Liberar su disponibilidad.
- Repetir la solicitud sin duplicar efectos ni cambiar la fecha
  de una cancelación ya realizada.
- Rechazar la cancelación de una reserva confirmada ya iniciada.
- Informar cuando la reserva no exista.

## 4. Decisiones de alcance y supuestos

### 4.1. Regla de atención confirmada por el responsable

La empresa dispone de una sola agenda compartida por todos
los servicios y puede atender una sola reserva a la vez.

El sistema permite registrar múltiples reservas en fechas y horarios
diferentes, pero no acepta intervalos superpuestos entre reservas
confirmadas, independientemente del servicio seleccionado.

Ejemplo:

- Una reserva de 10:00 a 11:00 ocupa ese intervalo.
- Otra reserva no puede comenzar a las 10:30.
- Otra reserva sí puede comenzar a las 11:00.

### 4.2. Decisiones propuestas para la primera versión

Las siguientes decisiones complementan la consigna y permanecen
sujetas a autorrevisión antes de integrar la especificación:

- No se gestionan empleados, sucursales ni recursos múltiples.
- No se aplican horarios comerciales en esta versión.
- La zona horaria de operación es America/Lima.
- El operador administra clientes, servicios y reservas.
- La búsqueda de alternativas utiliza pasos de 30 minutos,
  un horizonte de siete días desde el inicio solicitado
  y un máximo de cinco resultados.
- Los pasos de 30 minutos se aplican a las sugerencias;
  no restringen por sí mismos los horarios de registro manual.
- No se incluye autenticación en este prototipo académico local.
  No se considera preparado para exposición pública.

## 5. Reglas de integridad y disponibilidad

- Todos los campos obligatorios se validan en el backend.
- Los nombres no pueden contener únicamente espacios.
- Los identificadores se generan automáticamente.
- No se impone unicidad de nombre, teléfono o correo de clientes,
  porque la consigna no define un identificador personal único.
- Una reserva debe referenciar un cliente y un servicio existentes.
- El precio y la duración aplicados se conservan en la reserva,
  evitando que futuros cambios del servicio alteren esos valores.
- La finalización se calcula sumando la duración al inicio.
- Todos los intervalos se comparan con una interpretación temporal
  consistente con la zona horaria de operación.

### 5.1. Regla de superposición

Dos reservas son incompatibles cuando ambas están confirmadas
y se cumple la siguiente condición:

    inicio_nuevo < fin_existente
    y
    fin_nuevo > inicio_existente

Reglas complementarias:

- Una reserva puede comenzar exactamente cuando termina otra.
- Una reserva puede finalizar exactamente cuando comienza otra.
- Las reservas canceladas no bloquean disponibilidad.
- La búsqueda de alternativas debe considerar la duración completa
  del servicio y las reservas confirmadas de toda la agenda.
- Las alternativas son informativas y no garantizan disponibilidad
  hasta confirmar el registro.
- La comprobación final de disponibilidad y el registro deben
  ejecutarse de manera atómica.
- Dos solicitudes simultáneas incompatibles no pueden aceptarse ambas.

### 5.2. Estados de la reserva

- Estados de la primera versión: Confirmada y Cancelada.
- Estado inicial: Confirmada.
- Transición permitida: Confirmada → Cancelada.
- La transición solo se permite antes del inicio de la reserva.
- Una cancelación repetida conserva el estado y el momento
  de cancelación previamente registrados.
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
- La verificación debe incluir intervalos ocupados, límites entre
  reservas, sugerencias disponibles y solicitudes concurrentes.

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

La sugerencia de horarios alternativos forma parte de RF-06
y deberá reflejarse en los criterios de ACT-07, ACT-09 y ACT-10.

Las referencias reales a commits, Pull Requests, revisión e integración
se incorporarán conforme se produzcan, sin anticipar evidencias.

## 9. Estado de verificación

Este documento especifica el comportamiento esperado.
No acredita que las funcionalidades estén implementadas.

La implementación, las pruebas funcionales y la validación
de concurrencia permanecen pendientes.

La autorrevisión documental se registra en el Pull Request #21.
Su integración no equivale a la aprobación independiente
de otro integrante.