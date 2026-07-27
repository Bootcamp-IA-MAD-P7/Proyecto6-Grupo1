## Context

El repositorio ya dispone de `scripts/data/convert_cfpb_to_parquet.py`, que aplica parcialmente el contrato de target para producir `data/interim/cfpb.parquet`, utilizado por el EDA. El script actual confirma la viabilidad del mapping y de la huella de narrativa, pero no constituye todavía un constructor de entrenamiento completo: selecciona implícitamente la primera fuente local, no genera un manifiesto agregado reproducible, no excluye grupos con targets contradictorios y no dispone de pruebas de integración específicas del constructor.

`PG-2` y la tarea heredada `001/T-005` requieren transformar esa base existente en un proceso repetible y verificable. El proceso debe consumir una fuente local CFPB, respetar `config/cfpb_target_contract.json`, mantener los datos sensibles fuera de Git y preparar el corpus que necesitará el baseline de `PG-3`. Víctor es el responsable funcional de Datos y EDA; Miguel coordina esta adaptación al flujo OpenSpec y Harness.

## Goals / Non-Goals

**Goals:**

- Convertir el conversor existente en una ruta de construcción explícita, repetible y probada para el dataset local candidato a entrenamiento.
- Mantener un límite claro entre datos locales con narrativas y evidencia agregada versionable.
- Garantizar el mapping de once clases, las exclusiones, las huellas de narrativa y la exclusión de grupos con target conflictivo.
- Producir un manifiesto agregado de control que permita comparar ejecuciones sin exponer datos sensibles.
- Dejar el corpus preparado para que un cambio posterior decida idioma, política intra-grupo, partición y desbalanceo antes del entrenamiento.

**Non-Goals:**

- Entrenar o evaluar un modelo.
- Crear la partición definitiva de train, validation y test.
- Elegir un filtro de idioma, una política intra-grupo o una estrategia de desbalanceo.
- Descargar datos, añadir datos CFPB al repositorio o publicar narrativas.
- Cambiar el contrato de once clases, la interfaz React, el backend o la infraestructura.

## Decisions

### Evolucionar el conversor existente en lugar de crear un pipeline paralelo

El cambio extenderá o reorganizará `scripts/data/convert_cfpb_to_parquet.py` y sus pruebas, conservando el contrato ya utilizado por el EDA. Crear un segundo constructor con reglas similares duplicaría lógica de filtros, mapping y hashing, con riesgo de que EDA y entrenamiento describan poblaciones distintas.

Alternativa considerada: crear un script de entrenamiento independiente desde cero. Se descarta porque separaría dos implementaciones del mismo contrato y dificultaría detectar divergencias.

### Entrada y salida explícitas, locales e ignoradas por Git

Nota de implementación: la fuente oficial llega como ZIP. El constructor extrae localmente un único CSV del ZIP antes de procesarlo; tanto ZIP como CSV extraído permanecen bajo `data/raw/` e ignorados por Git.

La construcción materializa una etapa local e ignorada en `data/interim/` antes de calcular conflictos y duplicados. Así se evita releer el CSV completo para cada recuento y se limita el uso de memoria con el corpus real.

El constructor recibirá una fuente local explícita y escribirá el corpus resultante en `data/processed/`, mientras que la fuente permanece en `data/raw/` y el Parquet de EDA puede conservarse en `data/interim/`. Las rutas locales de datos no se versionarán. La salida contendrá solo las columnas necesarias para pasos posteriores: narrativa local, fecha de recepción cuando sea necesaria para una futura política temporal, target canónico y huella de narrativa; no necesita conservar identificadores de reclamación.

Alternativa considerada: seleccionar automáticamente el primer CSV disponible y reutilizar `data/interim/cfpb.parquet` como salida final. Se descarta porque una selección implícita no es reproducible y mezcla el artefacto de exploración con el candidato a entrenamiento.

### Manifiesto agregado separado del corpus

Cada ejecución generará un manifiesto agregado con identificador o huella de la fuente local, versión o huella del contrato, recuentos de entrada, elegibles, exclusiones, clases, grupos duplicados y conflictos. El manifiesto no incluirá narrativas, identificadores de reclamación ni etiquetas de filas individuales.

Alternativa considerada: versionar un extracto de filas para facilitar revisión manual. Se descarta por el riesgo de privacidad y porque los tests pueden usar fixtures sintéticas.

### Aplicar la política de conflictos, preservar decisiones abiertas

El constructor calculará la huella normalizada de narrativa indicada por el contrato y excluirá completamente los grupos con targets canónicos contradictorios. Para grupos no conflictivos conservará la huella y las filas necesarias, sin colapsarlos ni ponderarlos todavía. La política intra-grupo, idioma, split y desbalanceo se resolverá en `001/T-006` mediante un cambio OpenSpec posterior.

Alternativa considerada: elegir ahora una fila representativa por grupo o aplicar pesos. Se descarta porque ambas opciones afectan la evaluación y requieren evidencia y acuerdo de equipo.

### Polars lazy y pruebas con datos sintéticos

Se conservará Polars y su procesamiento lazy para manejar un corpus de millones de filas sin cargarlo innecesariamente en memoria. Las pruebas unitarias e integración construirán CSVs sintéticos temporales y verificarán mapping, desconocidos, exclusiones, conflictos, determinismo y ausencia de narrativas en el manifiesto.

Alternativa considerada: ejecutar pruebas sobre la fuente CFPB real. Se descarta porque sería lenta, no portable y contraria a las restricciones de privacidad.

## Risks / Trade-offs

- [La fuente local cambia o se sustituye] → El manifiesto incluirá una huella de fuente y el constructor requerirá una ruta explícita.
- [El procesamiento de grupos duplicados aumenta memoria o tiempo] → Se medirá el rendimiento sobre el corpus local y se mantendrá el procesamiento lazy o por etapas si fuera necesario.
- [El manifiesto expone información sensible por error] → El esquema del manifiesto se limitará a contadores y metadatos técnicos; pruebas y quality gates rechazarán texto de narrativa.
- [Los datos elegibles contienen nueva taxonomía] → La política `unknown_label_policy = fail` detendrá la construcción y exigirá revisar el contrato.
- [Se interpreta el corpus construido como listo para entrenar] → Documentación y manifiesto declararán que siguen abiertas las decisiones de `T-006`.

## Migration Plan

1. Añadir pruebas sintéticas que definan el comportamiento esperado del constructor.
2. Adaptar el conversor existente para aceptar rutas explícitas, crear el corpus procesado y producir el manifiesto agregado.
3. Ejecutar el constructor solo sobre la fuente local autorizada y comprobar los recuentos contra el EDA.
4. Versionar únicamente código, pruebas, configuración y evidencia agregada; verificar que los datos locales siguen ignorados.
5. Actualizar la tarea heredada `T-005`, el cambio OpenSpec y la documentación mínima afectada.

No hay migración de producción. La reversión consiste en revertir el cambio de código y eliminar los artefactos locales regenerables de `data/processed/`; no se eliminan fuentes originales ni se reescribe el contrato.

## Open Questions

- Qué detector y umbral de idioma se aprobarán para el entrenamiento.
- Si los grupos duplicados no conflictivos se colapsarán, se ponderarán o se mantendrán completos.
- Qué partición temporal o estratificada se adoptará y qué periodo se reservará como test final.
- Qué estrategia de desbalanceo se comparará en el baseline.
- Qué metadatos de fuente se pueden conservar en el manifiesto sin aumentar el riesgo de privacidad.
