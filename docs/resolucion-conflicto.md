# Resolución de conflicto — ACT-12

## Contexto

Ejercicio controlado entre ramas del mismo autor.
Archivo: docs/ejercicio-conflicto.md.

No modifica el código ni las reglas de la aplicación.
No acredita trabajo simultáneo de varios integrantes.

## Base común

Commit: 284a0a0.

Las ramas docs/act-12-mensaje-a y docs/act-12-mensaje-b
se crearon desde esa misma base.

## Cambios incompatibles

### Variante A

Commit: 110e12e9fc77c8e56c2e66b6a2de3f610b07a2cd.
Pull Request: #34.

Mensaje:
Reserva confirmada correctamente.

### Variante B

Commit: f0ae036bd77c1039edd217549e4f07e42b103207.
Pull Request: #35.

Mensaje:
Reserva registrada; consulte los detalles de su atención.

## Origen del conflicto

Después de integrar A en develop, se intentó incorporar
origin/develop en B mediante:

    git merge --no-commit origin/develop

Git informó CONFLICT (content) porque ambas ramas modificaron
la misma línea con contenidos diferentes.

git status mostró el archivo como both modified.

## Decisión de resolución

Se conservó la confirmación explícita de A y la orientación de B:

Mensaje de confirmación: Reserva confirmada correctamente;
consulte los detalles de su atención.

En el archivo final el mensaje se conserva en una sola línea.
Se eliminaron los marcadores de conflicto.

## Verificación y registro

- Se revisó la diferencia preparada.
- git diff --cached --check no reportó incidencias.
- git diff --name-only --diff-filter=U no mostró archivos.
- Se registró la resolución mediante un commit de merge.
- Se publicó la rama B.
- git status confirmó árbol limpio y sincronizado.

Commit de resolución:
d16c07b07ec91c269d1ae563b3e60ba34827fde4

Padres:
- f0ae036bd77c1039edd217549e4f07e42b103207
- 85a5db0e443372228cc2c31198018ae433de136b

## Evidencias

- Base: PR #33.
- Variante A: https://github.com/EmersonL10/Sistema_Reservas/pull/34
- Variante B y resolución:
  https://github.com/EmersonL10/Sistema_Reservas/pull/35
- Captura del conflicto conservada por el responsable.
- Salidas de Git antes y después de resolverlo.

## Incidencia de ejecución

Durante el procedimiento se pegó una frase del documento
en PowerShell. La terminal respondió CommandNotFoundException.

La resolución se realizó posteriormente en el editor y se verificó
mediante el diff preparado. Ese error de terminal no fue el conflicto
de Git ni produjo la pérdida del archivo.

## Estado

Conflicto resuelto y publicado en B.
Revisión final e integración del PR #35 pendientes.