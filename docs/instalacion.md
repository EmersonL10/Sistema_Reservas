# Instalación y ejecución local

## 1. Requisitos

Entorno utilizado durante el desarrollo:

- Windows y PowerShell.
- Python 3.13.14.
- MySQL Server 8.0.46.
- MySQL Workbench.
- Git.
- Node.js para comprobar sintaxis de JavaScript; no es necesario
  para ejecutar la aplicación.

Las dependencias Python están fijadas en requirements.txt.

## 2. Obtener el código

    git clone https://github.com/EmersonL10/Sistema_Reservas.git
    cd Sistema_Reservas

Durante la preparación de la entrega, el código integrado está
en develop:

    git switch develop

La referencia definitiva de entrega se identificará mediante
la etiqueta publicada de la versión.

## 3. Crear el entorno e instalar dependencias

    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe -m pip check

No es necesario activar el entorno si se utiliza su ejecutable.

## 4. Inicializar MySQL

Desde una conexión administrativa de MySQL Workbench:

1. Abrir database/schema.sql desde la carpeta clonada.
2. Ejecutar el script completo para crear sistema_reservas
   y las tablas clientes, servicios, agenda y reservas.
3. Comprobar la agenda con:

```sql
SELECT * FROM sistema_reservas.agenda;
```

El resultado esperado es una fila con id 1.

El script está destinado a la inicialización de tablas nuevas.
No debe ejecutarse completo sobre un esquema ya inicializado.
No elimina ni migra tablas existentes.

Si el esquema ya existe, comprobar su estructura antes de utilizarlo.
No eliminar datos para repetir una instalación.

## 5. Configurar la cuenta de aplicación

Para una instalación nueva, ejecutar como administrador,
sustituyendo el marcador por una contraseña privada antes
de enviar la instrucción:

```sql
CREATE USER 'reservas_app'@'localhost'
IDENTIFIED BY 'SUSTITUIR_POR_UNA_CLAVE_PRIVADA';

GRANT SELECT, INSERT, UPDATE
ON sistema_reservas.*
TO 'reservas_app'@'localhost';
```

Si la cuenta ya existe, verificar su configuración y permisos;
no repetir CREATE USER ni cambiar su contraseña innecesariamente.

No guardar contraseñas reales en scripts versionados.

## 6. Configurar el entorno local

    Copy-Item .env.example .env

Editar .env con estos parámetros:

```dotenv
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=reservas_app
MYSQL_PASSWORD=
MYSQL_DATABASE=sistema_reservas
```

Completar MYSQL_PASSWORD con la contraseña privada de la cuenta.
El valor vacío de la plantilla no constituye una contraseña configurada.

Verificar que el archivo esté excluido:

    git check-ignore .env

Resultado esperado: .env.

## 7. Comprobar conexión

    .\.venv\Scripts\python.exe -m flask --app src.reservas check-db

Resultado esperado:

    OK: database=sistema_reservas; user=reservas_app@localhost; timezone=+00:00; agenda=1

## 8. Ejecutar

    .\.venv\Scripts\python.exe -m flask --app src.reservas run --host 127.0.0.1

Abrir http://127.0.0.1:5000.

Detener el servidor con Ctrl+C.

## 9. Verificar funcionamiento

Utilizar datos ficticios:

1. Registrar y modificar un cliente.
2. Registrar un servicio con precio y duración.
3. Registrar una reserva futura.
4. Consultar la reserva en la agenda.
5. Intentar reservar el mismo intervalo y revisar alternativas.
6. Cancelar una reserva y comprobar su conservación.
7. Actualizar la página para verificar persistencia.

La agenda admite una atención simultánea.
Los formularios utilizan horarios de America/Lima.

## 10. Ejecutar pruebas

    .\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v

Las pruebas de integridad necesitan MySQL y utilizan transacciones
con rollback sobre el esquema configurado. Sus contadores
autoincrementales pueden avanzar.

Los scripts verificar_servicios.py, verificar_reservas.py
y verificar_cancelacion.py son ensayos adicionales:
conservan datos ficticios y no deben confundirse con pruebas aisladas.

## 11. Límites de uso

Prototipo académico local sin autenticación.
El servidor de desarrollo no constituye un despliegue de producción.

Recordatorios, reportes, dashboard, pagos en línea e historial
de clientes quedan fuera de la primera versión.