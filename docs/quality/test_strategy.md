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
