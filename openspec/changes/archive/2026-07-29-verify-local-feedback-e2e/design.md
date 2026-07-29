## Context

ClaimVox ya puede consumir una predicción local configurada y el flujo de
feedback conserva únicamente metadatos aprobados en almacenamiento local. La
evidencia actual comprueba contratos y unidades aisladas, pero no demuestra el
recorrido completo desde una respuesta local válida hasta un resumen agregado.

## Goals / Non-Goals

**Goals:**

- Ejecutar una comprobación local reproducible de predicción real, feedback
  explícito y resumen agregado sin incorporar la narrativa al feedback.
- Verificar que la respuesta de feedback se limita a metadatos autorizados,
  que el resumen no expone registros individuales y que la predicción no se
  altera.
- Producir evidencia agregada suficiente para decidir el estado de `MED-04`.

**Non-Goals:**

- No crear autenticación, autorización, base compartida, analítica de usuarios,
  Docker, despliegue, MLOps, corpus de entrenamiento ni reentrenamiento.
- No verificar `MED-05`, seleccionar un Champion ni modificar el modelo servido.
- No versionar artefactos locales, registros de feedback, UUID, narrativas,
  datos CFPB, credenciales ni capturas con contenido introducido.

## Decisions

### Recorrido local con entradas sintéticas

La verificación SHALL usar una narrativa sintética y una API FastAPI local que
cargue el artefacto reproducible ya disponible en el equipo. Primero se obtiene
una predicción real; después se construye el feedback exclusivamente con
metadatos permitidos de esa respuesta y vocabularios cerrados. Esto demuestra la
integración sin usar ni guardar una narrativa CFPB real.

### Evidencia agregada y sin persistencia versionada

El informe versionado registrará solo modo local, contrato, resultado de las
operaciones, versión de modelo/taxonomía disponible, grupos del resumen y los
límites comprobados. La raíz local de feedback, registros, UUID y cualquier
contenido enviado permanecen fuera de Git. Esta decisión prioriza privacidad y
reproducibilidad frente a una auditoría de registros individuales.

### Criterio de decisión para MED-04

`MED-04` podrá pasar a `Verificado` únicamente si predicción local real,
creación de feedback permitida y resumen exclusivamente agregado se completan
en la misma ejecución local, sin cambiar la predicción. El resultado no prueba
autenticación, operación compartida ni métricas de producción; esos límites se
mantendrán explícitos.

## Risks / Trade-offs

- [No hay artefacto local reproducible disponible] → la verificación queda
  bloqueada y `MED-04` continúa en curso; no se sustituye por mock.
- [El feedback contiene información no permitida] → se detiene la prueba, no se
  versionan registros y se corrige primero el contrato o la implementación.
- [Un registro local previo contamina el resumen] → usar una raíz local limpia o
  documentar solo la comprobación de grupos sin datos individuales.
- [El entorno local no representa producción] → el informe declara de forma
  explícita ausencia de autenticación, servicio compartido, despliegue y MLOps.

## Migration Plan

1. Confirmar la configuración local de API, artefacto y raíz controlada.
2. Ejecutar el recorrido con entrada sintética y registrar únicamente resultados
   agregados.
3. Si se supera, actualizar los documentos canónicos que cambien de significado;
   si falla, conservar `MED-04` en curso y registrar el bloqueo.
4. No hay migración ni rollback compartidos: los registros locales de la prueba
   expiran según la política y pueden purgarse con el repositorio local.

## Open Questions

- Ninguna para la verificación local; la autenticación, una base compartida y la
  instrumentación de producción son cambios posteriores y separados.
