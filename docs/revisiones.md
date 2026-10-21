# Registro de revisión e integración — ACT-11

## Modalidad y procedimiento

Responsable: EmersonL10.
Modalidad: individual.

Los cambios se desarrollaron en ramas y se presentaron mediante
Pull Requests hacia develop. Antes de integrar se inspeccionaron
los cambios, resultados de pruebas y limitaciones.

Las decisiones se registraron como autorrevisión.
No constituyen aprobación independiente de otro integrante.

## Caso verificable: PR #23

Actividad: ACT-03.
Propósito: preparar la aplicación Flask base.

Pull Request:
https://github.com/EmersonL10/Sistema_Reservas/pull/23

### Hallazgo

Durante la revisión se identificó una contraseña escrita
en la plantilla de entorno y en la configuración de Python.

### Corrección

Se sustituyeron ambos valores por cadenas vacías.
La configuración privada se mantiene fuera del repositorio.

Commit:
9d7931d05e90b176c97a297b849914acb34317ec

La corrección de los archivos actuales no elimina el valor
del historial anterior. Este registro no acredita por sí mismo
la rotación de una credencial.

### Secuencia comprobada

Todas las horas siguientes corresponden a America/Lima,
el 20/10/2026.

| Evento | Hora |
|---|---|
| Commit inicial 50fcd53 | 09:26:09 |
| Commit correctivo 9d7931d | 09:36:23 |
| Comentario de autorrevisión | 09:38:44 |
| Merge hacia develop | 09:38:53 |

Comentario previo a la integración:
https://github.com/EmersonL10/Sistema_Reservas/pull/23#issuecomment-6293454333

Commit de merge:
7699e75a9967824cd333e25ecc967f6e1836f067

### Verificaciones declaradas en la revisión

- Arranque local con respuesta HTTP 200.
- pip check sin conflictos.
- Compilación de Python sin errores reportados.
- Comprobación de espacios sin incidencias.
- Esquema y conexión MySQL todavía pendientes en ese momento.

## Inventario de integraciones

Los siguientes PR aparecen integrados en develop.
Esta tabla acredita su integración; el detalle temporal de
los comentarios se verificó específicamente para el PR #23.

| Actividad | PR | Commit de merge |
|---|---|---|
| ACT-01 | #21 | 5a30164 |
| ACT-02 | #22 | 59db010 |
| ACT-03 | #23 | 7699e75 |
| ACT-04 | #24 | 8a2d5d5 |
| ACT-05 | #25 | fa37eec |
| ACT-06 | #26 | 94a9566 |
| ACT-07 | #27 | 6c1eee0 |
| ACT-08 | #28 | 13a5537 |
| ACT-09 | #29 | 1471738 |
| ACT-10 | #31 | 5fef521 |

## Consulta reproducible de evidencia

    gh pr list --state merged --base develop --limit 30 --json number,title,url,mergedAt,mergeCommit

    gh pr view 23 --json number,url,commits,comments,mergedAt,mergeCommit

GitHub devuelve las fechas en UTC. Las horas de este documento
se calcularon restando cinco horas para America/Lima.

## Conclusión

El PR #23 demuestra una corrección seguida de una decisión
de autorrevisión documentada antes de la integración.

El proyecto no acredita revisión independiente ni participación
de varios desarrolladores, debido a su modalidad individual.