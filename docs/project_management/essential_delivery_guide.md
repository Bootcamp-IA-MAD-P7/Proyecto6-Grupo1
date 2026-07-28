# Guía de entrega esencial

## Qué está verificado

ClaimVox recibe una narrativa, la envía al servicio FastAPI local configurado y
presenta una predicción multiclase con revisión humana obligatoria. El modelo
esencial local es un LogisticRegression TF-IDF entrenado con las once clases del
contrato CFPB. No existe despliegue, autenticación, persistencia ni MLOps.

## Reconstruir el modelo y sus evidencias

Los datos CFPB preparados son locales y no se versionan. Con las particiones
aprobadas disponibles, ejecutar:

```bash
python scripts/ml/train_essential_baseline.py
python -m unittest tests.unit.test_cfpb_baseline tests.unit.test_essential_model_evaluation -v
```

El comando usa exclusivamente train y validation. Genera el artefacto local
`models/cfpb_essential_baseline.pkl`, ignorado por Git, y evidencia agregada en
`reports/validation/`. No carga el test protegido.

## Ejecutar el servicio y la PWA localmente

```bash
python -m uvicorn app.api.main:app --port 8000
cd app/interface
npm ci
$env:VITE_PREDICTION_API_BASE_URL = "http://127.0.0.1:8000"
npm run dev
```

Sin la variable de entorno, ClaimVox conserva el mock de forma explícita. La
respuesta real sigue siendo una recomendación revisable, no una decisión ni un
enrutamiento automático.

## Evidencia principal

- EDA: `reports/validation/cfpb_eda.md`.
- Métricas y diagnóstico final: `reports/validation/cfpb_essential_evaluation.md`.
- Manifiesto del artefacto: `reports/validation/cfpb_essential_model_manifest.json`.
- Integración PWA ↔ API local: `reports/validation/claimvox_local_inference_smoke.md`.

## Límites

No se incorporan narrativas CFPB, predicciones por fila, datasets ni binarios de
modelo a Git. Las clases débiles requieren revisión humana reforzada. El modelo
no está desplegado ni se monitoriza en producción.
