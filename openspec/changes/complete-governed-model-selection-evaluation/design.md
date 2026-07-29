## Context

PG-11 ya dispone de una política, un ejecutor aislado, tuning gobernado y un
piloto de 20.000 filas. El piloto confirmó viabilidad, pero sus tres folds y
cinco trials no constituyen la ejecución aprobada para `MED-02` o `MED-03`.
La política vigente fija `StratifiedGroupKFold`, `narrative_hash`, cinco folds,
semilla `42`, macro F1 y hasta 30 trials por candidato. La partición `train`
es la única entrada de selección; `validation` se reserva para una confirmación
única posterior y `test` permanece protegido.

## Goals / Non-Goals

**Goals:**

- Ejecutar una evaluación reproducible sobre el alcance completo autorizado de
  `train.parquet`, conservando grupos, once clases y semillas versionadas.
- Realizar CV agrupada y estratificada, tuning acotado dentro de los folds y una
  confirmación única sobre `validation` solo después de la recomendación.
- Generar evidencia agregada de folds, variabilidad, gap, coste, limitaciones
  por clase y decisión humana para evaluar `MED-02` y `MED-03`.

**Non-Goals:**

- No usar `test` para ajuste, selección, diagnóstico ni promoción.
- No declarar un Champion, modificar ClaimVox, desplegar, crear un artefacto
  compartido ni sustituir el baseline local en la aplicación.
- No reducir la ejecución de entrega a un piloto, ni versionar datos,
  narrativas, binarios, credenciales o logs sensibles.

## Decisions

### Alcance de datos y prevención de fuga

La ejecución SHALL consumir la totalidad de la partición local `train.parquet`
aprobada y conservará `narrative_hash` como grupo. Se usará
`StratifiedGroupKFold` con cinco folds y semilla `42`, tal como fija la
política. Se rechazarán rutas de corpus completo, `validation` y `test` como
entrada de selección.

Se descarta `StratifiedKFold` sin grupos porque podría separar narrativas con el
mismo hash entre folds. También se descarta reutilizar el piloto, ya que no
alcanza el presupuesto ni el número de folds aprobados.

### Secuencia de decisión sin test protegido

La búsqueda Optuna evaluará candidatos solo dentro de los folds de `train`, con
macro F1 como objetivo primario. El informe recogerá macro F1 de train y del
fold retenido, media, desviación, coste y métricas agregadas por clase. La
recomendación aplicará el gap estricto menor que `0.05` y los desempates
versionados.

Tras una revisión humana de la recomendación —o de la ausencia de selección—,
un único candidato puede confirmarse una sola vez contra `validation`. Esa
confirmación no permite volver a ajustar parámetros. `test` no se carga en
ninguna fase de este cambio.

### Presupuesto y ejecución controlada

El presupuesto de entrega será el vigente: cinco folds y hasta 30 trials por
candidato. Antes de ejecutar se registrará el entorno, la huella de la
partición, versiones y coste previsto. La ejecución requerirá aprobación humana
explícita de tiempo y cómputo; si se interrumpe o no alcanza el presupuesto, se
publicará como evidencia incompleta y no cambiará `MED-02` ni `MED-03`.

Se descarta ampliar silenciosamente la infraestructura o paralelizar sin una
decisión específica. El entorno puede ser local o Colab autorizado, pero sus
resultados deben producir el mismo formato agregado y no subir datos a Git.

### Evidencia y quality gates

El resultado se validará contra el esquema de informe de selección y las
puertas de métricas vigentes. Git conservará configuración, código, pruebas y
reportes agregados; los modelos y datos permanecen locales. Los quality gates
deben rechazar ausencia de clases, leakage, campos incompletos, gap igual o
superior a `0.05` y cualquier indicio de uso del test para seleccionar.

## Risks / Trade-offs

- [Coste alto de cinco folds y 30 trials] → aprobación humana previa, registro
  de presupuesto y resultado explícitamente incompleto si no finaliza.
- [Inestabilidad de clases minoritarias] → resultados por fold y por clase,
  desviación como criterio de decisión y revisión humana.
- [Fuga por agrupación mal aplicada] → entrada limitada a `train`,
  `narrative_hash` obligatorio y pruebas que rechazan rutas o grupos no válidos.
- [Sobreinterpretar una mejor métrica] → no Champion, confirmación única en
  validation y test protegido fuera de alcance.

## Migration Plan

1. Implementar y probar el perfil completo sin ejecutar datos reales.
2. Solicitar aprobación humana del presupuesto y ejecutar fuera de Git.
3. Versionar únicamente evidencia agregada y decidir si satisface los criterios.
4. Si falla una puerta o el presupuesto no se completa, conservar el baseline y
   registrar que no hay selección aprobada; no hay migración de servicio ni
   rollback de datos porque no se modifican.

## Open Questions

- La aprobación humana de tiempo y cómputo sigue pendiente antes de ejecutar el
  presupuesto completo.
- Si ningún candidato satisface el gap o las limitaciones por clase, la decisión
  será no seleccionar y los criterios se actualizarán solo según la evidencia
  realmente obtenida.
