# Sistema de Gestión de Reservas

Proyecto académico del curso Herramientas de Desarrollo
de la Universidad Tecnológica del Perú (UTP).

## Responsable

- Usuario de GitHub: EmersonL10.
- Modalidad: individual.

## Descripción del problema

Una empresa de servicios administra sus reservas mediante llamadas,
WhatsApp y hojas de cálculo. Esta dispersión dificulta consultar
la información y mantener un registro organizado.

## Objetivo

Desarrollar una aplicación que centralice la gestión de clientes,
servicios y reservas.

## Alcance de la primera versión

### Gestión de clientes
- Registrar clientes.
- Modificar sus datos.
- Consultar clientes.

### Gestión de servicios
- Registrar servicios.
- Establecer precio y duración.
- Consultar servicios.

### Gestión de reservas
- Registrar reservas seleccionando cliente y servicio.
- Registrar fecha y hora.
- Consultar reservas.
- Cancelar reservas.

## Funcionalidades para versiones futuras

- Recordatorios automáticos.
- Reportes.
- Dashboard de indicadores.
- Pagos en línea.
- Historial de clientes.

Estas funcionalidades quedan fuera de la primera versión.

## Organización del desarrollo

- Git y GitHub para el control de versiones.
- GitHub Issues para registrar actividades y criterios de aceptación.
- GitHub Projects para gestionar estados, prioridades y responsables.
- Ramas de funcionalidades para desarrollar los cambios.
- Pull Requests para documentar la revisión antes de integrar.

La modalidad es individual. Las revisiones propias y los conflictos
controlados entre ramas se documentarán como tales, sin atribuir
participación a otras personas.

## Trazabilidad

Cada funcionalidad deberá relacionar:

Requerimiento → Issue → Responsable → Commits → Revisión → Integración.

## Tecnologías

- Python y Flask para el backend.
- HTML, CSS y Jinja para la interfaz.
- MySQL 8.0 con InnoDB para persistencia.
- MySQL Connector/Python para conexión a datos.
- MySQL Workbench para administración.
- unittest para pruebas automatizadas.

Arquitectura: [docs/arquitectura.md](docs/arquitectura.md).

La instalación y el arranque de la aplicación permanecen
pendientes de verificación.

## Estado actual

Proyecto en planificación y preparación del repositorio.
Las funcionalidades todavía no están implementadas.

## Ejecución y pruebas

Las instrucciones de instalación, ejecución y pruebas se incorporarán
cuando se seleccione la tecnología y exista una implementación verificable.