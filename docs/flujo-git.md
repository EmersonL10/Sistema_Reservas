# Flujo de desarrollo

- main: versiones estables verificadas.
- develop: integración de cambios.
- feature/act-XX-descripcion: implementación.
- docs/act-XX-descripcion: documentación.

## Procedimiento
1. Actualizar develop y crear una rama.
2. Desarrollar y comprobar los cambios.
3. Registrar commits descriptivos vinculados al Issue.
4. Publicar la rama.
5. Crear un Pull Request hacia develop.
6. Revisar diferencias y registrar pruebas y observaciones.
7. Corregir los hallazgos y documentar la decisión de integración.
8. Integrar mediante merge y verificar el resultado.

La modalidad es individual. La autorrevisión no constituye
aprobación independiente de otro integrante.

Las credenciales, .env y el entorno virtual se excluyen de Git.