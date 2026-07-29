# Evidencia: persistencia local gobernada de feedback

Fecha: `2026-07-29`

Cambio OpenSpec: `add-governed-feedback-persistence`

## Alcance verificado

- Política versionada: `config/claimvox_feedback_persistence_policy.json`.
- Contrato mínimo: UUID técnicos, versiones de modelo y taxonomía, clases
  canónicas, decisión, finalidad y marcas UTC de creación y vencimiento.
- Privacidad: se rechazan narrativa, texto libre, identidad, cuenta, dirección,
  IP, cabeceras, audio y transcripción sin incluir valores en los errores.
- Almacén: SQLite exclusivamente local bajo `data/local/feedback`, con esquema
  versionado, inicialización idempotente y rechazo de rutas externas.
- Retención: purga idempotente por vencimiento y resumen agregado solo por
  versión de modelo, clase sugerida y decisión.

## Verificación proporcional

`python -m unittest tests.unit.test_feedback_persistence -v` superado el 29 de
julio de 2026: 10 pruebas sintéticas, 0 fallos. Cubren validación, ruta
controlada, inicialización repetible, registro explícito, retención, purga y
resumen privado. `python -m py_compile app/api/schemas/feedback.py
app/api/services/feedback_repository.py` y la validación estricta OpenSpec
también se superaron durante el cambio.

## Límites explícitos

No existe endpoint ni interfaz de feedback, autenticación, autorización,
servicio compartido, base de datos productiva, despliegue, métricas operativas
reales, incorporación a reentrenamiento, backup, observabilidad ni MLOps. La
persistencia local no procesa datos CFPB reales y no selecciona, promueve ni
reentrena modelos automáticamente.
