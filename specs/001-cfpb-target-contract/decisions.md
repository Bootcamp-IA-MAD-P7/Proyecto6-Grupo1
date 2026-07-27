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

Al aprobar esta decisión, el EDA se planteó como trabajo paralelo. La responsabilidad operativa vigente corresponde a Víctor. Mezclar notebooks con la definición del target duplicaría trabajo y podría fijar decisiones de modelado antes de observar la evidencia.

### Decisión

El EDA describe y devuelve evidencia agregada. Esta spec fija las invariantes comunes. El entrenamiento queda bloqueado hasta incorporar esa evidencia y cerrar idioma, privacidad, duplicados y partición.

### Consecuencias

- El equipo puede trabajar en paralelo desde hoy.
- Los notebooks no necesitan contener la lógica definitiva del pipeline.
- La evidencia puede cambiar decisiones abiertas, pero no silenciosamente las reglas ya aceptadas.

## ADR-003 Adoptar Jupytext con formato percent para notebooks reproducibles

- Fecha: `2026-07-23`
- Estado: `accepted`
- Relacionada con: `T-004, T-007`

### Contexto

Los notebooks .ipynb generan diffs JSON difíciles de revisar, no son evaluables
con Ruff y mezclan código con salidas. El equipo necesita una forma de trabajar
con celdas que sea lintable, versionable y sincronizable con Jupyter.

### Decisión

Los notebooks se editarán como `.py` con celdas `# %%` (formato percent). Esta
sintaxis es soportada nativamente por VS Code. Se añade Jupytext para
sincronizar un `.ipynb` efímero cuando se necesite Jupyter Notebook/Lab o
ejecución headless con nbconvert.

El `.py` es fuente de verdad; el `.ipynb` se genera por sincronización y no se
versiona (`*.ipynb` en `.gitignore`).

Configuración:
- `.jupytext.toml` con `formats = "ipynb,py:percent"`
- Makefile opcional (comandos oficiales vía Python, no dependen de make)
- `notebooks/README.md` actualizado con el flujo

Los cambios nuevos de producto se gobernarán con OpenSpec; esta decisión se
gestiona como tarea heredada dentro de la spec numerada `001`.

### Consecuencias

- Positivas: diffs limpios, Ruff analiza todo, el `.ipynb` se regenera desde
  el `.py`, cualquiera puede ejecutar celdas en VS Code sin Jupytext.
- Negativas: quien ejecute con Jupyter Notebook/Lab necesita Jupytext; los
  `.ipynb` no están disponibles tras clonar sin ejecutar sincronización.
- Neutral: el flujo se documenta en `notebooks/README.md`.

### Evidencia

- Propuesta registrada y revisada desde el arnés (`004-agentic-harness`).
- Prueba de concepto validada contra `001/T-004` y `001/T-007`.

## ADR-004 Fijar la política inicial antes del baseline

- Fecha: `2026-07-27`
- Estado: `accepted`
- Relacionada con: `T-005, T-006, PG-2`

### Contexto

El constructor local de T-005 ya produce un corpus contractual reproducible, pero una fuente CFPB puede cambiar entre descargas y todavía faltaba una regla verificable para idioma, duplicados, partición y desbalanceo. Entrenar sin esa regla permitiría comparar resultados sobre poblaciones diferentes o introducir leakage entre duplicados.

### Decisión

Se aprueba `config/cfpb_training_policy.json` como política inicial de preparación. Fija la huella de la fuente local y del contrato actual; usa únicamente inglés para el primer baseline; excluye grupos con target contradictorio y mantiene juntos los grupos no conflictivos; requiere un split temporal por fecha máxima de grupo con objetivo 70/15/15; establece macro F1 como métrica primaria y `class_weight="balanced"` sin re-muestreo. El test queda reservado para una evaluación final.

### Consecuencias

- Cualquier fuente o contrato distinto falla antes de preparar particiones y exige una decisión nueva.
- El siguiente trabajo debe implementar un detector de idioma determinista, el split local y sus manifiestos agregados.
- Esta decisión no entrena, selecciona ni evalúa modelos; no verifica criterios de entrega ni cierra PG-2.
- Los textos CFPB siguen exclusivamente en artefactos locales ignorados por Git; las evidencias compartidas solo contienen huellas y recuentos.

### Evidencia

- `openspec/changes/decide-cfpb-training-policy/`.
- `config/cfpb_training_policy.json`.
- `scripts/data/cfpb_training_policy.py`.
- `tests/unit/test_cfpb_training_policy.py`.
