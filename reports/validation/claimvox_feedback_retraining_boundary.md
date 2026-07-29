# Frontera de candidatos de reentrenamiento de feedback local

Fecha: `2026-07-29`

Cambio OpenSpec: `add-feedback-operational-flow`

## Alcance de la finalidad

La finalidad `future_retraining_candidate` identifica una revisión humana como candidata trazable para una futura evaluación. No incorpora ningún dato a un corpus ni modifica una predicción, una métrica, un modelo o una decisión de selección.

## Metadatos permitidos y trazabilidad

Por cada candidato, la política permite exclusivamente identificadores técnicos, versión de modelo, versión de taxonomía, clase sugerida, clase revisada cuando corresponda, decisión, finalidad y marcas UTC de creación y expiración. La trazabilidad se limita a esos metadatos minimizados y a su resumen agregado por versión de modelo, clase sugerida y decisión.

La persistencia es local, bajo la raíz controlada `data/local/feedback`, sin red ni servicio compartido. La política exige una expiración y conserva los registros como máximo durante 30 días; la consulta de resumen purga primero los vencidos.

## Límites explícitos

Esta capacidad no crea ni contiene un corpus de entrenamiento. No persiste narrativas, texto introducido, identidad, audio, transcripciones ni probabilidades completas. Tampoco existe validación de candidatos para entrenamiento, deduplicación, política de incorporación al corpus, selección de Champion, evaluación de modelo ni reentrenamiento automático.

La finalidad es una señal local pendiente de una revisión y un proceso futuro gobernado. No acredita autenticación, permisos reales, operación compartida, base de datos productiva, despliegue ni MLOps.
