# Guion de presentación · ClaimVox MVP local

> Audiencia: cliente o evaluador. Empezar por el problema y el valor; explicar
> método y arquitectura solo como prueba de que la demostración es fiable.

## 1. El problema

Clasificar reclamaciones escritas lleva tiempo y puede ser inconsistente. Una
persona necesita una primera orientación, no una decisión automática.

## 2. La propuesta

ClaimVox propone una de once familias de producto y muestra alternativas para
que una persona revise el resultado. La persona conserva la decisión final.

## 3. La demostración

Mostrar ClaimVox con el ejemplo sintético incorporado. Si el entorno local está
configurado, señalar `Prediction response`; si no, señalar claramente el mock.
En ambos casos, mostrar `Human review required` y evitar introducir datos
personales o narrativas CFPB reales.

## 4. La evidencia

- EDA reproducible y contrato de once clases.
- Baseline evaluado localmente: macro F1 validation `0.6390`, accuracy `0.8684`
  y gap `0.0078`.
- Métricas por clase, matriz de confusión, importancia TF-IDF y análisis
  agregado de errores.
- Diez de diez criterios del nivel esencial verificados para ejecución local.

## 5. Por qué es una entrega responsable

La aplicación no almacena narrativas, audio ni transcripciones. La API local
limita tamaño y frecuencia, no usa CORS abierto y devuelve errores seguros. La
salida sigue siendo una recomendación revisable: no hay decisión financiera ni
enrutamiento automático.

## 6. Cómo puede crecer sin rehacerse

La PWA, el servicio y el predictor están desacoplados mediante contratos. Esto
permite añadir feedback gobernado, otra versión de modelo, persistencia o
despliegue en cambios posteriores sin convertir esas capacidades futuras en
promesas actuales.

## 7. Cierre honesto

ClaimVox es un MVP local verificable, no un producto desplegado. No hay cuentas
reales, base de datos, cloud, Champion ni MLOps. Es precisamente esa claridad la
que permite decidir el siguiente paso con evidencia.

## Material de apoyo

- `README.md`: recorrido, arquitectura y límites.
- `reports/validation/cfpb_essential_evaluation.md`: métricas y diagnósticos.
- `reports/validation/claimvox_local_inference_smoke.md`: integración local.
- `docs/assets/charts/delivery-status-2026-07-28.svg`: resumen visual del estado
  del briefing; `docs/project_management/delivery_levels.md` es la fuente
  canónica.
- `docs/security/threat_model.md`: límites y riesgos.
