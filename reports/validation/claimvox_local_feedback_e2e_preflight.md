# Preflight estático de feedback local extremo a extremo

Fecha: `2026-07-29`
Jira: `PG-13`
Cambio OpenSpec: `verify-local-feedback-e2e`

## Contratos confirmados

- La predicción local usa el contrato versionado de once clases canónicas y
  genera un identificador, versión de modelo y versión de taxonomía que son
  metadatos permitidos para feedback.
- La API registra `POST /api/v1/feedback` y expone
  `GET /api/v1/feedback/summary`; la creación devuelve solo estado y el resumen
  usa una respuesta tipada agregada.
- La política permite exclusivamente los campos, decisiones y finalidades
  cerrados; prohíbe narrativa, identidad, texto libre, audio, transcripción y
  probabilidades completas.
- La persistencia local controlada se limita a `data/local/feedback`, con
  retención de 30 días, sin red, base compartida ni exportación individual.

## Requisitos aún no comprobados en ejecución

- El backend espera por defecto un artefacto local ignorado por Git en
  `models/cfpb_baseline.pkl`; este preflight no afirma que exista ni que cargue.
- La API debe iniciar localmente y responder salud antes de ejecutar el
  recorrido. Comando mínimo de comprobación:

```bash
curl -s http://127.0.0.1:8000/api/v1/health
```

- La ejecución posterior deberá usar solo una entrada sintética y conservar
  fuera de Git tanto la raíz local como registros, UUID y contenido enviado.

## Plan de prueba minimizado

- Usar el ejemplo sintético ya proporcionado por la interfaz, sin copiarlo en
  comandos, informes ni registros versionados.
- Tras una respuesta local válida, construir la solicitud únicamente con
  `prediction_id`, `model_version`, `taxonomy_version`, `suggested_class`, la
  decisión `confirmed` y la finalidad `human_review_quality_assurance`.
- Omitir `reviewed_class` para la decisión `confirmed`; no generar ni conservar
  UUID adicionales, texto libre, identidad, narrativa ni probabilidades.
- Comprobar después que el resumen contiene solo grupos por versión, clase
  sugerida y decisión; una prueba negativa añadirá únicamente el nombre de un
  campo prohibido, sin ningún valor asociado.

## Límites

Este documento confirma la preparación estática y el plan minimizado. No demuestra predicción real,
persistencia operativa, autenticación, permisos reales, operación compartida,
despliegue, MLOps ni reentrenamiento.
