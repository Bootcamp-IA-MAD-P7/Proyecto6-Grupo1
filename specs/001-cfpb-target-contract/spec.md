# SPEC: Contrato de target CFPB

- ID: `001`
- Estado: `in_progress`
- Responsables: `Víctor / análisis del CSV y EDA`; `Miguel / contrato y arquitectura`
- Fecha: `2026-07-22`

## Contexto y problema

El spike CFPB confirmó que el dataset es viable, pero observó catorce etiquetas de `product`: once vigentes, dos históricas equivalentes y una histórica ambigua. También detectó desbalanceo, narrativas repetidas y riesgo residual de información personal.

<<<<<<< HEAD
Víctor está realizando el análisis del CSV y el EDA. Necesita reglas compartidas que eviten comparar resultados construidos con clases, filtros o columnas incompatibles, sin convertir esta spec en un notebook ni repetir su análisis. Miguel mantiene el contrato y revisa su coherencia con arquitectura, privacidad y experiencia de producto.
=======
Víctor tiene asignado el EDA y debe trabajar con reglas compartidas que eviten resultados construidos con clases, filtros o columnas incompatibles, sin convertir esta spec en un notebook ni repetir su análisis.
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83

## Usuario y necesidad

- El equipo de EDA necesita saber qué población describir, qué target estudiar y qué evidencias devolver.
- El equipo de ML necesita un contrato reproducible antes de construir particiones o entrenar.
- El equipo de producto necesita que la salida conserve once familias financieras comprensibles.

## Objetivo observable

Disponer de un contrato versionado y verificable que transforme las etiquetas observadas en once clases canónicas, limite la entrada a la narrativa y defina las reglas mínimas de elegibilidad, duplicados, partición y privacidad.

## Alcance

### Incluido

- Taxonomía canónica y mapping exacto de etiquetas históricas.
- Exclusión justificada de la etiqueta histórica ambigua.
- Columnas permitidas y prohibidas para modelado.
- Reglas para evitar fuga entre particiones por narrativas duplicadas.
- Límites de privacidad y persistencia aplicables al EDA.
- Evidencias que el EDA debe aportar para cerrar idioma, duplicados y soporte temporal.

### Fuera de alcance

- Realizar o reemplazar el EDA del equipo.
- Seleccionar modelos, métricas finales, balanceo o hiperparámetros.
- Descargar o versionar narrativas.
- Implementar la aplicación, API, Docker o despliegue.
- Decidir todavía el mapping entre producto y cola operativa.

## Contrato funcional

### Población inicial

```text
2023-08-24 <= date_received < 2026-07-23
complaint_what_happened no vacío
product no vacío
```

La ventana permanece congelada durante el primer ciclo para hacer comparables los resultados.

### Entrada y target

- Única entrada candidata al modelo: `complaint_what_happened`.
- Target de origen: `product`.
- Target derivado: `product_canonical`.
- Las columnas que revelan la clasificación, la empresa o una respuesta posterior están prohibidas como features.

### Normalización

1. Las once etiquetas vigentes se conservan sin cambios.
2. `Credit reporting, credit repair services, or other personal consumer reports` se normaliza a `Credit reporting or other personal consumer reports`.
3. `Payday loan, title loan, or personal loan` se normaliza a `Payday loan, title loan, personal loan, or advance loan`.
4. `Credit card or prepaid card` se excluye del corpus de modelado porque el nombre no permite asignar con seguridad una de las dos clases vigentes. Sus 111 registros permanecen visibles en el EDA de población y en el recuento de exclusiones.
5. Cualquier etiqueta desconocida bloquea la construcción del corpus hasta revisar el contrato; no se asigna automáticamente a `other`.

### Duplicados

- El EDA debe informar IDs repetidos, textos exactamente repetidos y textos repetidos con targets distintos.
- Una huella de narrativa normalizada será la clave de grupo para impedir que textos equivalentes aparezcan en particiones distintas.
- Los grupos con targets contradictorios se excluyen del modelado y se cuantifican.
- La decisión de conservar una observación por grupo o ponderar grupos se tomará después del EDA; no modifica la regla contra leakage.

### Privacidad e idioma

- Las narrativas pueden procesarse localmente, pero no se incorporan a Git, informes, capturas, logs ni fuentes de NotebookLM.
- Los ejemplos publicados deben ser sintéticos o redactados.
- El EDA debe medir idioma con método y versión reproducibles. El idioma no se usa todavía como filtro silencioso.
- No se autoriza entrenamiento hasta aprobar la política de idioma y completar la revisión de privacidad de `000-problem-discovery`.

## Requisitos

- R-001: El contrato debe producir exactamente once etiquetas canónicas conocidas.
- R-002: Toda etiqueta histórica debe mapearse o excluirse mediante una regla exacta y trazable.
- R-003: Solo `complaint_what_happened` puede considerarse entrada del modelo inicial.
- R-004: Ninguna narrativa o fragmento real puede persistirse en Git o documentación.
- R-005: Los duplicados de narrativa no pueden cruzar particiones de entrenamiento, validación o test.
- R-006: El EDA debe separar población de origen, población elegible, exclusiones y corpus resultante.
- R-007: El EDA debe devolver distribución por clase y tiempo, ausencias, duplicados, conflictos de target, longitud e idioma.
- R-008: Una etiqueta no contemplada debe provocar un fallo explícito.
- R-009: Las decisiones de balanceo y métrica se tomarán con la evidencia del EDA, no dentro de esta spec.

## Criterios de aceptación

- AC-001: Dadas las catorce etiquetas observadas, cuando se aplique el mapping, entonces el resultado contiene once clases canónicas y una exclusión ambigua cuantificada.
- AC-002: Dada una columna prohibida, cuando se valide como feature, entonces el contrato la rechaza.
- AC-003: Dadas narrativas iguales, cuando se preparen particiones, entonces comparten clave de grupo y no pueden repartirse entre particiones.
- AC-004: Dada una etiqueta desconocida, cuando se construya el target, entonces el proceso falla y solicita revisión.
- AC-005: Dado un informe o artefacto versionado, cuando se revise, entonces no contiene narrativas reales.
- AC-006: Dado el EDA paralelo, cuando finalice, entonces entrega las evidencias de R-007 sin necesidad de modificar esta spec salvo que contradiga el contrato.

## Preguntas abiertas no bloqueantes para el EDA

- [ ] Q-001: ¿Qué detector y umbral de idioma ofrecen un resultado reproducible y proporcionado?
- [ ] Q-002: ¿Conviene colapsar duplicados o ponderarlos después de agrupar las particiones?
- [ ] Q-003: ¿Qué ventana temporal debe reservarse como test final tras estudiar la cobertura y el drift?
- [ ] Q-004: ¿Qué clases necesitan pesos, muestreo u otra mitigación de desbalanceo?

## Evidencia de cierre esperada

- `config/cfpb_target_contract.json` validado automáticamente.
- Informe EDA con el checklist de R-007 y sin narrativas persistidas.
- Política de idioma y privacidad aprobada.
- Implementación reproducible del target y de la clave de grupo.
- Tests de mapping, etiquetas desconocidas, leakage y ausencia de texto en artefactos.
