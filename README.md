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

Centralizar la gestión de clientes, servicios y reservas mediante
una aplicación web con persistencia MySQL.

## Funcionalidades de la primera versión

### Clientes

- Registrar clientes.
- Modificar sus datos.
- Consultar clientes.

### Servicios

- Registrar servicios.
- Establecer precio y duración.
- Consultar servicios.

### Reservas

- Registrar reservas seleccionando cliente, servicio, fecha y hora.
- Comprobar disponibilidad durante toda la duración del servicio.
- Ofrecer horarios alternativos cuando el intervalo esté ocupado.
- Consultar reservas.
- Cancelar reservas conservando su registro.

La agenda admite una sola atención simultánea.
Los horarios se presentan en America/Lima.

## Funcionalidades futuras

Fuera del alcance de la primera versión:

- Recordatorios automáticos.
- Reportes.
- Dashboard de indicadores.
- Pagos en línea.
- Historial de clientes.

## Tecnologías

- Python y Flask para el backend.
- HTML, CSS, JavaScript y Jinja para la interfaz.
- MySQL 8.0 con InnoDB para persistencia.
- MySQL Connector/Python para conexión a datos.
- MySQL Workbench para administración.
- unittest para pruebas automatizadas.

Decisiones técnicas: [Arquitectura](docs/arquitectura.md).

## Estado actual

Clientes, servicios y reservas implementados e integrados
en develop, con interfaz web y persistencia MySQL.

Quince pruebas automatizadas satisfactorias y arranque comprobado
desde una copia nueva con entorno virtual independiente,
reutilizando el esquema MySQL existente.

La publicación de v1.0.0 está en preparación.

## Instalación y ejecución

Consultar primero la [guía completa de instalación](docs/instalacion.md)
para preparar MySQL, la cuenta de aplicación y el archivo .env.

Desde la raíz del proyecto, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app src.reservas check-db
.\.venv\Scripts\python.exe -m flask --app src.reservas run --host 127.0.0.1
```

Abrir http://127.0.0.1:5000.

Detener el servidor con Ctrl+C.

El archivo .env contiene configuración privada y está excluido de Git.
.env.example documenta las variables sin incluir credenciales reales.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

La suite incluye:

- Ocho pruebas de API con repositorios simulados.
- Dos pruebas de reglas de fechas.
- Cinco pruebas de integridad contra MySQL real.

Las pruebas de integridad requieren la base configurada y utilizan
rollback. Los contadores autoincrementales pueden avanzar.

Los ensayos adicionales verificar_servicios.py, verificar_reservas.py
y verificar_cancelacion.py conservan datos ficticios.

Resultados y límites:

- [Informe de pruebas](docs/pruebas.md).
- [Verificación desde una copia nueva](docs/verificacion-entrega.md).

## Organización del desarrollo

- Git y GitHub para registrar cambios y controlar versiones.
- GitHub Issues para actividades y criterios de aceptación.
- GitHub Projects para estados, prioridades y responsables.
- Ramas de trabajo para aislar cambios.
- Pull Requests para revisar antes de integrar.

Flujo aplicado:

Crear rama → Desarrollar → Commit → Push → Pull Request
→ Revisión y pruebas → Decisión de aprobación → Merge.

La modalidad es individual. Las revisiones propias y los conflictos
controlados entre ramas se identifican como tales, sin atribuir
participación a otras personas.

Procedimiento: [Flujo Git](docs/flujo-git.md).

## Trazabilidad

Requerimiento → Issue → Responsable → Commits
→ Revisión → Integración → Evidencia de prueba.

Consultar la [matriz de trazabilidad](docs/trazabilidad.md).

## Evidencias técnicas

- [Requerimientos](docs/requerimientos.md).
- [Modelo de datos](docs/modelo-datos.md).
- [Registro de revisiones](docs/revisiones.md).
- [Resolución del conflicto](docs/resolucion-conflicto.md).
- [Bitácora](docs/bitacora.md).

## Límites de uso

Prototipo académico local sin autenticación.
El servidor de desarrollo no constituye un despliegue de producción.

La verificación desde una copia nueva reutilizó MySQL existente;
no acredita una instalación nueva del servidor ni del esquema.

No se realizó una prueba de carga.
La concurrencia observada corresponde a dos solicitudes simultáneas.