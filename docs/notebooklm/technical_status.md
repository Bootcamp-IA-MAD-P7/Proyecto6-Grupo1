# Estado técnico consolidado

## Estado general

- Fase: descubrimiento.
- Idea de negocio: clasificación y enrutamiento de reclamaciones financieras, elegida por unanimidad con condiciones.
- Dataset: Consumer Complaint Database del CFPB viable con condiciones; target y reglas de EDA versionados.
- Código funcional: React PWA funcional contra mock; pipeline ML y servicio real no iniciados.
- Despliegue: no iniciado.

## Capacidades verificadas

- Rama `dev` creada y configurada como rama predeterminada.
- Estructura inicial integrada en `dev` mediante Pull Request y squash merge.
- Intent global del proyecto integrado y vigente.
- Spec `000-problem-discovery` activa para gobernar la evaluación y el cierre de las puertas de datos.
- Reglas de evaluación `1.0` aprobadas por mayoría absoluta del equipo activo, con puertas críticas, matriz y gobierno de la selección.
- Dos candidatas evaluadas con la matriz `1.0`: reclamaciones CFPB y clasificación visual de residuos con RealWaste.
- `CAND-001` elegida por José, Abel, Víctor y Miguel con cuatro votos favorables, cero contrarios y cero abstenciones.
- El spike está completado y la spec `001` autoriza el EDA bajo contrato; todavía no autoriza entrenamiento o implementación funcional.
- Arnés CFPB reproducible implementado con configuración versionada, probe API, muestra temporal en memoria, informes agregados y siete tests unitarios.
- Probe verificado: 2.306.723 narrativas, catorce etiquetas observadas, licencia CC0 informada por la API y clase mayoritaria del 72,45 %.
- G-02, G-03, G-04 y G-06 superadas para EDA; G-05 continúa condicionada por la revisión de privacidad.
- Spec `001-cfpb-target-contract` activa con once clases canónicas, dos aliases, una exclusión ambigua y siete tests de contrato.
- El EDA continúa en paralelo y debe aportar evidencia agregada sobre clases, tiempo, ausencias, duplicados, longitud e idioma.
- React PWA implementada con React, TypeScript y Vite contra un cliente mock sustituible; backend, inferencia real y evolución nativa siguen pendientes.
- Spec `003-complaint-routing-experience` en curso con arquitectura de información, OpenAPI contract-only, siete tests de contrato y cinco tests de interacción frontend.
- La propuesta frontend previa de Abel se ha reconciliado con la spec `003`: los requisitos compatibles de calidad pasan a `T-008`, mientras auth, administración, entrenamiento y voz permanecen como propuestas no aprobadas.
- Abel tiene asignada operativamente la revisión de `003/T-008` y la PR #14; los roles permanentes del equipo siguen pendientes de acuerdo.
- El build genera manifest y service worker; el shell estático puede funcionar offline, pero `/api/` no tiene fallback ni caché runtime.
- La interfaz identifica el modo simulado, no muestra confianza inventada, exige revisión humana y no conserva ni devuelve la narrativa.
- Flujo humano-IA independiente de proveedor implementado y verificado, con generación acotada de contexto por spec y tarea.
- Workflow `repository-quality` ejecutado correctamente en Pull Request.
- Ruleset `Protect dev` activo con PR y check de calidad obligatorios, historial lineal y bloqueo de force push y borrado.
- Aprobaciones humanas no requeridas temporalmente.

## Capacidades previstas, no implementadas

- Pipeline de datos y entrenamiento.
- Integración de la React PWA con un servicio y modelo reales.
- Persistencia y feedback.
- Docker y despliegue.
- CI/CD completo.
- Red neuronal, A/B testing, drift y promoción.

## Riesgos actuales

- Tratar la viabilidad condicionada como si idioma, privacidad y partición ya estuvieran cerrados.
- Confundir estructura preparada con funcionalidad implementada.
- Confundir la PWA mock con una predicción real o un producto validado por negocio.
- Los roles permanentes del equipo activo todavía no están asignados; existe una asignación operativa frontend para la PR #14.
- La normalización de target está versionada; idioma, deduplicación final, partición, desbalanceo y privacidad siguen pendientes de la evidencia del EDA.
- El fuerte crecimiento de reclamaciones de informes de crédito puede producir desbalanceo extremo y cambios de procedencia que limiten la representatividad.
- La muestra temporal detecta drift de etiquetas y duplicación: el extremo de 2023 concentra la etiqueta histórica y muchos más duplicados que el extremo de 2026.
- La publicación reciente de narrativas presenta retraso y la API tiene comportamiento dependiente del cliente y paginación no trivial.
