## Context

ClaimVox integra en `dev` un baseline multiclase reproducible, inferencia
FastAPI local, PWA conectada, feedback local minimizado y tres quality gates.
La documentación activa no se actualizó de manera uniforme después de las
últimas integraciones: algunas fuentes siguen negando persistencia local, el
resumen global avanzado contradice su propia tabla y el gráfico activo
representa un corte anterior.

La auditoría debe respetar cuatro fronteras:

- `docs/project_management/delivery_levels.md` es la fuente canónica del estado
  de los 25 criterios.
- Los JSON e informes bajo `reports/validation/` son evidencia, no sustitutos
  del estado canónico.
- Los cambios OpenSpec archivados, dailies e informes fechados son históricos y
  no se reescriben para aparentar actualidad.
- Las ramas no fusionadas y los archivos locales no versionados no forman parte
  de `dev` ni pueden convertirse en evidencia documental.

## Goals / Non-Goals

**Goals:**

- Contrastar afirmaciones activas contra código, contratos, pruebas y evidencia
  versionada.
- Corregir defectos claros, reproducibles y acotados.
- Presentar el proyecto con lenguaje técnico profesional y trazabilidad directa.
- Automatizar la detección de divergencias entre el gráfico activo, el README y
  el estado canónico.
- Dejar explícito qué funciona localmente y qué requiere trabajo posterior.

**Non-Goals:**

- Ejecutar entrenamiento completo, notebooks pesados o datasets CFPB.
- Seleccionar un Champion o convertir resultados exploratorios en entrega.
- Implementar Docker, base compartida, autenticación, cloud o MLOps.
- Reescribir fuentes históricas o incorporar cambios desde ramas no fusionadas.
- Crear, mover o publicar tags, commits, Pull Requests o releases.

## Decisions

### 1. Verdad por capas, no una única narración duplicada

El estado se mantiene en `delivery_levels.md`; README resume y enlaza; los
informes conservan evidencia; OpenSpec define requisitos; NotebookLM separa
hechos, estado técnico y narrativa. Se evita copiar tablas completas fuera de
su fuente canónica.

Alternativa descartada: mantener el mismo estado en todos los documentos. La
duplicación fue la causa principal de divergencia.

### 2. Conteos derivados de identificadores canónicos

La puerta de calidad analizará las filas `ESS`, `MED`, `ADV` y `EXP` de
`delivery_levels.md`, comprobará unicidad y recuento total, y validará los
conteos declarados en el gráfico activo. El recurso visual tendrá fecha de
corte `2026-07-30`.

Alternativa descartada: validar solo la existencia del SVG. Un activo válido
puede seguir mostrando cifras obsoletas.

### 3. Capacidad local y capacidad operativa se expresan por separado

La documentación dirá que existe persistencia SQLite local gobernada y feedback
local extremo a extremo, pero no autenticación, base compartida, operación
multiusuario, despliegue ni reentrenamiento automático.

Alternativa descartada: usar «persistencia» sin calificativo. Esa redacción
confunde una capacidad local probada con `ADV-02`.

### 4. Métricas solo desde evidencia versionada

Las cifras del baseline se tomarán de
`reports/validation/cfpb_baseline_metrics.json`; MED-01 de su informe
versionado; el resto de estados de sus evidencias enlazadas. Ningún archivo
local no versionado ni rama experimental se citará como resultado integrado.

### 5. Daily factual por áreas

La daily del corte recogerá únicamente cambios verificables en Git y resultados
ejecutados. Separará coordinación, frontend, backend, datos/ML y QA sin inventar
autoría individual cuando no pueda probarse.

## Risks / Trade-offs

- [La revisión amplia puede convertir documentación histórica en actual] →
  limitar ediciones a fuentes activas y añadir referencias al estado canónico.
- [Un parser Markdown simple puede ser frágil] → usar IDs y estados con formato
  estable, pruebas focalizadas y errores descriptivos.
- [La etiqueta 15/25 puede interpretarse como nivel medio terminado] → mostrar
  también 3 en curso y 7 no iniciados, con desglose por nivel.
- [La persistencia local puede confundirse con una base integrada] → repetir el
  límite local/SQLite y mantener `ADV-02` en `No iniciado`.
- [El README puede crecer demasiado] → priorizar mapa de evidencias y enlaces,
  trasladando detalle operativo a guías específicas.

## Migration Plan

1. Inventariar afirmaciones activas y evidencia versionada.
2. Corregir la comprobación automática y generar el gráfico vigente.
3. Reconciliar fuentes activas, README y daily.
4. Ejecutar pruebas focalizadas, quality gates y validación estricta OpenSpec.
5. Revisar el diff y solicitar revisión humana antes de cualquier commit o PR.

Rollback: revertir los archivos de este cambio. No hay migración de datos,
contratos, modelos ni servicios.

## Security, Testing and Documentation Impact

- No se leerán ni versionarán narrativas CFPB, datos brutos, modelos o secretos.
- Se comprobarán enlaces locales, SVG, conteos, OpenSpec y suites proporcionales
  de backend, frontend y quality gates.
- Se actualizarán únicamente fuentes activas cuyo significado haya cambiado.
- Los límites de privacidad y revisión humana permanecerán visibles.

## Open Questions

- La creación de una etiqueta posterior queda sujeta a revisión humana. No debe
  usar un nombre que sugiera nivel medio completo, Champion o despliegue.
