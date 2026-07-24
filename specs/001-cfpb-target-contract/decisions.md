# Decisiones: Contrato de target CFPB

## ADR-001 Normalizar a once familias y excluir la etiqueta ambigua

- Fecha: `2026-07-22`
- Estado: `accepted`
- Relacionada con: `R-001, R-002, R-008, AC-001, AC-004, T-001`

### Contexto

La API devuelve catorce etiquetas: once vigentes, dos formulaciones históricas equivalentes y `Credit card or prepaid card`, que no permite determinar cuál de las dos clases actuales corresponde usando solo su nombre.

### Decisión

Conservar once clases canónicas, normalizar las dos equivalencias directas y excluir del corpus de modelado los 111 registros ambiguos. La exclusión se cuantifica y permanece visible en el EDA. No se crea una clase `other` y toda etiqueta nueva provoca un fallo.

### Consecuencias

- Se conserva el significado de negocio de la taxonomía vigente.
- Se evita introducir 111 targets arbitrarios por un beneficio cuantitativo irrelevante.
- Si nueva evidencia permite desambiguarlos de forma fiable, el contrato deberá versionarse antes de reincorporarlos.

### Evidencia

- [`../../reports/validation/cfpb_viability.md`](../../reports/validation/cfpb_viability.md).
- [`../../docs/product/candidates/CAND-001-cfpb-complaint-routing.md`](../../docs/product/candidates/CAND-001-cfpb-complaint-routing.md).

## ADR-002 Separar el EDA del contrato y del entrenamiento

- Fecha: `2026-07-22`
- Estado: `accepted`
- Relacionada con: `R-003 a R-009, AC-002, AC-003, AC-005, AC-006, T-002 a T-006`

### Contexto

<<<<<<< HEAD
El EDA está asignado a Víctor mediante `T-004`. Mezclar sus notebooks con la definición del target duplicaría trabajo y podría fijar decisiones de modelado antes de observar la evidencia. Miguel mantiene el contrato y revisa los cambios transversales sin sustituir el análisis.
=======
Al aprobar esta decisión, el EDA se planteó como trabajo paralelo. La responsabilidad operativa vigente corresponde a Víctor. Mezclar notebooks con la definición del target duplicaría trabajo y podría fijar decisiones de modelado antes de observar la evidencia.
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83

### Decisión

El EDA describe y devuelve evidencia agregada. Esta spec fija las invariantes comunes. El entrenamiento queda bloqueado hasta incorporar esa evidencia y cerrar idioma, privacidad, duplicados y partición.

### Consecuencias

- El equipo puede trabajar en paralelo desde hoy.
- Los notebooks no necesitan contener la lógica definitiva del pipeline.
- La evidencia puede cambiar decisiones abiertas, pero no silenciosamente las reglas ya aceptadas.
