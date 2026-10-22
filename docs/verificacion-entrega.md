# Verificación de preparación de entrega — ACT-14

Fecha: 21/10/2026.
Responsable: EmersonL10.

## Referencia evaluada

- Rama: release/act-14-preparacion.
- Commit: 262a560.
- Copia: C:\Sistema\Sistema_Reservas_verificacion.

## Procedimiento observado

- Se clonó el código en una carpeta nueva.
- Se preparó un entorno virtual independiente.
- Se instalaron las dependencias publicadas.
- Se copió la configuración privada local, excluida de Git.
- Se reutilizaron el servidor y el esquema MySQL existentes.

## Resultados

| Comprobación | Resultado |
|---|---|
| pip check | Sin dependencias incompatibles |
| check-db | Conexión correcta, usuario reservas_app y sesión UTC |
| Agenda principal | id 1 disponible |
| Suite automatizada | 15 pruebas satisfactorias |
| Arranque en 127.0.0.1:5001 | Página cargada |
| Consulta visual de datos | Datos mostrados en la copia nueva |

Los mensajes MySQL 2003 de la suite corresponden a errores
simulados deliberadamente, no a una caída real del servidor.

## Alcance y limitaciones

La verificación acredita código clonado y entorno Python nuevo
utilizando una base de datos existente.

No acredita una inicialización nueva de MySQL ni un despliegue
de producción. Las pruebas de integridad utilizan rollback,
aunque los contadores autoincrementales pueden avanzar.

No se repitió en esta copia todo el recorrido de escritura
de los formularios. Sus evidencias previas están identificadas
en docs/pruebas.md.

## Estado de publicación

La integración de preparación, la integración hacia main,
la etiqueta y el release permanecen pendientes.