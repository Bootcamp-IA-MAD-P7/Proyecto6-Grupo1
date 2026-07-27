# Configuración

Configuración versionada y no sensible: rutas, parámetros de entrenamiento, umbrales y perfiles por entorno.

Los secretos nunca se almacenarán aquí; se documentarán mediante variables de entorno y archivos de ejemplo.

## CFPB

- `cfpb_target_contract.json`: las once clases canónicas, aliases y campos permitidos.
- `cfpb_training_policy.json`: política aprobada para el baseline inicial: huellas de fuente y contrato, inglés, grupos de duplicados, partición temporal, soporte mínimo y métricas. No contiene narrativas, rutas locales ni secretos.
