---
name: review-change
description: "Revisar un diff frente al cambio OpenSpec, contratos y reglas del proyecto."
---

# Revisar un cambio

La revisión es de solo lectura.

1. Confirmar base, alcance y cambio OpenSpec; usar el expediente numerado solo si es trabajo heredado.
2. Leer requisitos, diseño, decisiones, tareas y evidencias.
3. Revisar primero funcionalidad, privacidad, seguridad, contratos, datos y tests.
4. Revisar después mantenibilidad, duplicidad, UX y documentación.
5. Comprobar que ningún mock, contrato o carpeta se presenta como capacidad real.
6. Ordenar hallazgos como `blocking`, `high`, `medium` o `low`.
7. Indicar archivo, ubicación, impacto y corrección esperada.
8. Si no hay hallazgos, explicar alcance revisado y riesgo residual.

No modificar archivos, confundir preferencias con defectos, aprobar alcance no acordado ni inventar fallos.

## Resultado

```text
Alcance revisado:
Hallazgos:
Comprobaciones consideradas:
Preguntas o bloqueantes:
Riesgo residual:
Conclusión:
```
