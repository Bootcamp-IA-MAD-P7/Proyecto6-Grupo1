# Estrategia de pruebas

## Pirámide adaptada al producto ML

```text
                 E2E y smoke
              Contratos y integración
        Unitarias de dominio, datos y ML
     Calidad de datos, seguridad y repositorio
```

## Capas

### Repositorio

- Convenciones, enlaces, archivos sensibles y estructura.

### Datos

- Esquema, tipos, rangos, nulos, duplicados, clases y leakage.

### ML

- Preprocessing determinista.
- Compatibilidad de features.
- Entrenamiento reducido.
- Inferencia y probabilidades válidas.
- Métricas mínimas y overfitting.

### Dominio y aplicación

- Casos de uso aislados.
- Validación de entradas y errores.
- Contratos de predicción y feedback.

### Integración

- Artefacto real, aplicación y persistencia.
- Migraciones y compatibilidad.
- Observabilidad y versionado.

### Operación

- Build de contenedores.
- Health/readiness.
- Seguridad y rendimiento.
- Smoke en staging y producción.

## Datos de prueba

Se utilizarán fixtures pequeños, sintéticos o anonimizados. Los tests no dependerán del dataset completo salvo jobs específicos y controlados.

## Puertas de calidad

Los umbrales se definen antes de evaluar el modelo final. CI debe fallar si un contrato crítico, una métrica mínima o una comprobación de seguridad deja de cumplirse.

## Estado verificado

- Las puertas locales de datos, artefacto y métricas (`ADV-04` a `ADV-06`)
  están verificadas con configuración versionada y 16 pruebas sintéticas.
- El flujo local de predicción y feedback tiene pruebas unitarias, de contrato,
  integración y una comprobación manual extremo a extremo.
- Siguen pendientes las pruebas propias de contenedores, base compartida,
  autenticación, staging, producción, monitorización y rollback operativo.

La evidencia vigente se conserva en
[`reports/validation/cfpb_quality_gates.md`](../../reports/validation/cfpb_quality_gates.md)
y
[`reports/validation/claimvox_local_feedback_e2e.md`](../../reports/validation/claimvox_local_feedback_e2e.md).
