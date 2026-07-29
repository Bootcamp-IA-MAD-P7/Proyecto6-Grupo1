# Flujo local gobernado de feedback de ClaimVox

Fecha: `2026-07-29`

Cambio OpenSpec: `add-feedback-operational-flow`

## Capacidad comprobada

Tras una predicción obtenida mediante la API local, ClaimVox permite registrar una revisión humana explícita y consultar un resumen exclusivamente agregado. La creación usa los vocabularios cerrados de decisión y finalidad de la política; para una corrección requiere una clase canónica revisada. La interfaz identifica la indisponibilidad local sin fingir persistencia y el registro no modifica la predicción mostrada.

La API local expone creación y resumen bajo `/api/v1/feedback`. El resumen contiene únicamente grupos por `model_version`, `suggested_class` y `decision`, con su contador; no expone UUID, registros individuales ni contenido introducido.

## Privacidad, retención y trazabilidad

Solo se almacenan los metadatos aprobados: identificadores técnicos, versiones, clase sugerida, clase revisada cuando corresponde, decisión, finalidad y marcas UTC. La persistencia se limita a `data/local/feedback`, sin red ni servicio compartido. La retención máxima es de 30 días y el resumen purga los registros vencidos antes de agregarlos.

No se almacenan narrativas, identidad, texto libre, audio, transcripciones ni probabilidades completas. La finalidad `future_retraining_candidate` sigue siendo una señal local trazable: no existe corpus, validación de candidatos, deduplicación, política de incorporación, selección de Champion ni reentrenamiento automático.

## Verificación directa

- `python -m unittest tests.unit.test_feedback_operational_flow -v`: 3 pruebas sintéticas superadas.
- `npm exec -- vitest run src/components/PredictionResult.test.tsx`: 2 pruebas sintéticas superadas.
- `npm exec -- tsc --noEmit --pretty false`, `git diff --check` y validación estricta OpenSpec: superados.

Las pruebas cubren creación conforme, rechazo de un campo sensible sin reflejar su valor, purga previa, resumen agregado sin identificadores, indisponibilidad local y conservación de la predicción.

## Límites

No hay autenticación, permisos reales, operación compartida, base de datos productiva, analítica de usuarios, Docker, despliegue, MLOps ni reentrenamiento. Esta evidencia deja `MED-04` y `MED-05` en curso; no acredita una operación de producción.
