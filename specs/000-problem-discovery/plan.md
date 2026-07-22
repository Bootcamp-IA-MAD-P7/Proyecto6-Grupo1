# Plan: Selección del problema de negocio

- Spec: `specs/000-problem-discovery/spec.md`
- Estado: `active`

## Estado actual comprobado

- El proyecto se encuentra en descubrimiento.
- Existe un intent global aprobado que prohíbe inventar problema, dataset o tecnología.
- `CAND-001` ha sido elegida por unanimidad como dirección condicionada; dataset, target y clases siguen sujetos al spike de viabilidad.
- Existe una plantilla inicial de evaluación en `docs/product/idea_evaluation_template.md`.
- El repositorio dispone de dailies, decisiones, fuentes de NotebookLM, Pull Requests y controles de calidad.
- No existe código funcional, EDA ni entrenamiento que condicione la decisión.
- La versión `1.0` de las reglas de evaluación fue aprobada el 22 de julio de 2026 por mayoría absoluta del equipo activo.

## Solución propuesta

Ejecutar un proceso de descubrimiento gobernado por puertas de decisión y una matriz común:

```text
reglas acordadas
       ↓
propuestas comparables
       ↓
valor y decisión de usuario
       ↓
encaje multiclase y datos
       ↓
riesgos y demostrabilidad
       ↓
comparación y sensibilidad
       ↓
decisión registrada o no selección
       ↓
nueva spec funcional
```

La matriz ayuda a ordenar evidencia, pero la selección se registra como una decisión explícita. Las puertas críticas de licencia, multiclase, leakage, privacidad y acceso pueden descartar una alternativa con independencia de su puntuación total.

## Componentes y flujo

### 1. Gobierno de la evaluación

- Resolver Q-001 a Q-004.
- Versionar escala, pesos, mínimos y mecanismo de aprobación.
- Mantener la misma versión durante una ronda; cualquier cambio obliga a recalcular todos los candidatos afectados.

### 2. Registro de candidatos

Cada propuesta tendrá un identificador estable y una ficha homogénea. No se puntuarán ideas que carezcan de problema, usuario, decisión o hipótesis multiclase.

### 3. Puerta de valor

Comprobar necesidad, actor, decisión, frecuencia de uso, impacto esperado y alternativa actual sin el modelo.

### 4. Puerta de datos y ML

Comprobar fuente, licencia, acceso, target potencial, clases, volumen, calidad preliminar, disponibilidad temporal de variables, leakage y viabilidad de evaluación.

### 5. Puerta de responsabilidad

Comprobar privacidad, sensibilidad, sesgo, impacto del error, posibilidad de supervisión humana y usos no deseados.

### 6. Viabilidad de producto y entrega

Valorar claridad de inputs y outputs, UX demostrable, despliegue, feedback, observabilidad y camino incremental hasta los niveles avanzados.

### 7. Decisión y traspaso

Comparar, revisar sensibilidad, registrar elección o no selección y abrir una nueva spec funcional únicamente después de la aprobación.

## Datos, contratos y compatibilidad

Cada candidato deberá poder representarse con estos campos mínimos:

| Campo | Obligatorio | Descripción |
|---|---|---|
| ID | Sí | Identificador estable de la propuesta |
| Problema | Sí | Situación concreta que se desea mejorar |
| Usuario o actor | Sí | Persona o rol que utilizaría el resultado |
| Decisión | Sí | Acción que cambia gracias a la predicción |
| Target potencial | Sí | Resultado categórico que se predeciría |
| Clases | Sí | Tres o más categorías y su significado |
| Momento de inferencia | Sí | Cuándo se realiza la predicción |
| Dataset y fuente | Sí | Origen y localización verificables |
| Licencia y acceso | Sí | Condiciones de uso y reproducibilidad |
| Variables disponibles | Sí | Información existente en inferencia |
| Riesgos | Sí | Leakage, privacidad, sesgo, daño y uso indebido |
| Evidencias | Sí | Enlaces, consultas o inspecciones realizadas |
| Supuestos | Sí | Afirmaciones todavía no validadas |
| Estado | Sí | Propuesta, incompleta, viable, bloqueada, descartada o seleccionada |

No se versionarán datasets pesados, credenciales ni muestras sensibles. Los resultados cuantitativos deberán registrar cómo se obtuvieron.

## Archivos o áreas previstas

- `specs/000-problem-discovery/`: contrato, plan, tareas y decisiones.
- `docs/product/idea_evaluation_template.md`: matriz que deberá versionarse antes de puntuar.
- `docs/product/`: futuras fichas y evidencias de candidatos.
- `docs/notebooklm/project_facts.md`: solo recibirá hechos posteriores a una decisión aceptada.
- `docs/notebooklm/technical_status.md`: estado del proceso de descubrimiento.
- `docs/project_management/dailies/`: actividad, bloqueantes y acuerdos del equipo.
- `README.md` y `CHANGELOG.md`: estado e hitos relevantes.

## Estrategia de pruebas

- Unitarias: no aplican al redactar la spec; cualquier script futuro de puntuación deberá probar escala, pesos y cálculo.
- Integración: comprobar que spec, decisiones, matriz, daily y paquete de NotebookLM conservan enlaces válidos.
- Contrato: verificar que cada candidato contiene todos los campos mínimos y utiliza la versión vigente de la matriz.
- End-to-end o smoke: recorrer la ronda completa y comprobar que produce fichas, comparación, decisión condicionada y validaciones pendientes explícitas.
- Validación manual: revisión cruzada de licencias, leakage, riesgos, puntuaciones y razonamiento de decisión.
- Repositorio: ejecutar `python scripts/quality/check_repository.py` y `git diff --check` en cada PR.

## Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Elegir por atractivo del dataset | Producto sin decisión útil | Evaluar primero problema, usuario y decisión |
| Crear clases artificiales | Modelo multiclase sin significado | Exigir semántica y exclusividad de clases |
| Data leakage | Métricas irreales | Revisar momento de inferencia y disponibilidad temporal |
| Licencia o acceso insuficientes | Imposibilidad de reproducir o comercializar | Tratar licencia y acceso como puerta crítica |
| Puntuaciones subjetivas | Falsa precisión | Enlazar evidencia, revisar sensibilidad y añadir razonamiento |
| Sesgo de confirmación | Alternativas evaluadas de forma desigual | Congelar criterios antes de puntuar y hacer revisión cruzada |
| Datos sensibles | Riesgo legal o reputacional | Minimización, no versionar muestras y revisión específica |
| Alcance experto prematuro | Retraso del nivel esencial | Evaluar potencial sin implementar capacidades todavía |
| Bloqueo por desacuerdo | Decisión no trazable | Acordar mecanismo de aprobación y desempate antes de comparar |

## Entrega y reversión

La spec pasó a `active` al resolverse Q-001 a Q-004 y versionarse la matriz. Se cerrará cuando la candidata seleccionada supere sus puertas críticas, la documentación quede sincronizada y exista una spec funcional independiente.

La ejecución concluye con una decisión registrada o una no selección explícita. Revertir una elección no elimina evidencias: se añade una nueva decisión que sustituye a la anterior y explica la nueva información.

## Decisiones pendientes

- [x] Aprobar la escala, pesos y mínimos de la matriz.
- [x] Aprobar la evidencia mínima de viabilidad de datos.
- [x] Aprobar el mecanismo de aprobación y desempate.
- [x] Confirmar Jira como herramienta compartida de organización; enlace pendiente de creación.
- [x] Aprobar la ronda formada por `CAND-001` y `CAND-002`.
- [x] Elegir `CAND-001` por unanimidad como dirección condicionada.
- [ ] Resolver las puertas de viabilidad de datos antes de iniciar implementación funcional.
