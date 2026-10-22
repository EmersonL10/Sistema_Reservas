# Arquitectura del Sistema de Gestión de Reservas

## 1. Identificación

- Actividad: ACT-02.
- Issue: #2.
- Responsable: EmersonL10.
- Modalidad: individual.
- Fecha: 19/10/2026.
- Entrega: 21/10/2026.
- Estado: propuesta en revisión; implementación pendiente.

## 2. Tecnologías seleccionadas

| Componente | Tecnología | Función |
|---|---|---|
| Backend | Python y Flask | Procesar solicitudes y reglas de negocio |
| Frontend | HTML, CSS y Jinja | Presentar formularios y resultados |
| Persistencia | MySQL con InnoDB | Almacenar datos y ejecutar transacciones |
| Conector | MySQL Connector/Python | Comunicar Python con MySQL |
| Administración | MySQL Workbench | Ejecutar SQL e inspeccionar el esquema |
| Pruebas | unittest y cliente de pruebas de Flask | Verificar reglas e integración |
| Versionamiento | Git y GitHub | Registrar, revisar e integrar cambios |

### Entorno verificado

- Python: 3.13.14, mediante python --version.
- Node.js: v24.18.0, disponible pero no requerido.
- Servidor MySQL: 8.0.46, mediante SELECT VERSION().
- Flask y MySQL Connector/Python: instalación y compatibilidad
  efectiva pendientes de verificar en ACT-03.
- La versión de MySQL Workbench no se ha verificado.

## 3. Justificación

Se utilizará una aplicación monolítica modular para reducir
la complejidad de configuración y entrega, conservando
la separación de responsabilidades.

Flask permitirá integrar formularios y lógica de negocio
en una misma aplicación. MySQL aprovechará el servidor
ya disponible y permitirá trabajar con integridad referencial
y transacciones.

La interfaz se generará mediante plantillas Jinja.
No se requiere una aplicación frontend independiente.

## 4. Flujo de componentes

Navegador → Rutas Flask → Servicios de negocio → Acceso a datos → MySQL.

- Presentación: formularios, navegación, mensajes y confirmaciones.
- Rutas: recepción de solicitudes y construcción de respuestas.
- Servicios: validaciones, disponibilidad, alternativas y cancelación.
- Acceso a datos: consultas parametrizadas y límites transaccionales.
- Base de datos: persistencia, restricciones y relaciones.

## 5. Estructura prevista

- src/reservas/__init__.py: creación de la aplicación.
- src/reservas/config.py: configuración desde variables de entorno.
- src/reservas/routes/: rutas de clientes, servicios y reservas.
- src/reservas/services/: reglas de negocio.
- src/reservas/repositories/: consultas y operaciones de persistencia.
- src/reservas/db.py: conexiones y gestión de transacciones.
- src/reservas/templates/: páginas HTML.
- src/reservas/static/: estilos y recursos.
- database/schema.sql: definición reproducible del esquema.
- tests/: pruebas automatizadas.
- docs/: documentación y evidencias.
- requirements.txt: dependencias con versiones verificadas.
- .env.example: variables necesarias sin credenciales reales.
- .gitignore: exclusiones del repositorio.

La estructura se creará en ACT-03 y el esquema en ACT-04.

## 6. Persistencia e integridad

- Esquema propuesto exclusivo: sistema_reservas.
- Motor: InnoDB.
- Codificación: utf8mb4.
- Entidades principales: clientes, servicios y reservas.
- Relaciones mediante claves foráneas.
- Precio mediante DECIMAL con dos posiciones decimales;
  Python lo tratará con Decimal, evitando cálculos con float.
- Duración mediante minutos enteros mayores que cero.
- La reserva conservará el precio y la duración aplicados.
- Fechas almacenadas en UTC y convertidas desde y hacia
  America/Lima en los límites de la aplicación.
- Consultas SQL parametrizadas.
- Reservas canceladas conservadas para trazabilidad.

Los tipos definitivos, índices y restricciones se definirán
y verificarán en ACT-04.

## 7. Disponibilidad y concurrencia

Existe una sola agenda compartida por todos los servicios.

Para impedir que dos solicitudes simultáneas registren
intervalos incompatibles:

1. Iniciar una transacción.
2. Bloquear mediante SELECT ... FOR UPDATE una fila permanente
   que represente la agenda.
3. Comprobar los intervalos de reservas confirmadas mediante
   una lectura actual dentro de la misma transacción.
4. Insertar únicamente si el intervalo está disponible.
5. Confirmar la transacción o revertirla ante error.

Todos los flujos que modifiquen disponibilidad deberán
utilizar el mismo protocolo de bloqueo.

El bloqueo de la agenda permite serializar las decisiones
incluso cuando todavía no existen reservas.

Las sugerencias no bloquean horarios. La disponibilidad
se comprueba nuevamente al confirmar una alternativa.

Este mecanismo es un diseño pendiente de implementación
y prueba de concurrencia; todavía no se considera validado.

## 8. Configuración y ejecución

- Utilizar un entorno virtual de Python.
- Leer host, puerto, usuario, contraseña y esquema mediante
  variables de entorno.
- No publicar contraseñas ni archivos locales de configuración.
- Crear una cuenta de aplicación con permisos limitados
  sobre el esquema del proyecto.
- Separar las credenciales administrativas de las de ejecución.
- Ejecutar el prototipo en 127.0.0.1.

Los comandos definitivos de instalación, inicialización
y arranque se incorporarán al README después de verificarlos.

## 9. Estrategia de pruebas

- Pruebas unitarias de validaciones y reglas temporales.
- Pruebas de integración contra un esquema MySQL de pruebas separado.
- Pruebas funcionales mediante el cliente de pruebas de Flask.
- Verificación manual del recorrido completo en el navegador.
- Prueba de dos solicitudes incompatibles concurrentes.
- Datos ficticios y resultados reproducibles.
- Las pruebas no modificarán bases de datos ajenas al proyecto.

## 10. Límites de la primera versión

- Prototipo académico local sin autenticación.
- Una sola agenda, sin empleados ni sucursales.
- Sin restricciones de horario comercial.
- Recordatorios, reportes, dashboard, pagos e historial
  quedan fuera de v1.0.0.
- No está preparado para exposición pública.

## 11. Verificación pendiente

- Instalar y verificar Flask y el conector en el entorno virtual.
- Comprobar conexión con MySQL desde Python.
- Crear y arrancar la aplicación base.
- Implementar el esquema y sus restricciones.
- Validar transacciones, concurrencia y recuperación ante errores.