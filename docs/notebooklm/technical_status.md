# Estado técnico consolidado

## Estado general

- Fase: descubrimiento.
- Idea de negocio: clasificación y enrutamiento de reclamaciones financieras, elegida por unanimidad con condiciones.
- Dataset: Consumer Complaint Database del CFPB como candidata; spike de viabilidad pendiente.
- Código funcional: no iniciado.
- Despliegue: no iniciado.

## Capacidades verificadas

- Rama `dev` creada y configurada como rama predeterminada.
- Estructura inicial integrada en `dev` mediante Pull Request y squash merge.
- Intent global del proyecto integrado y vigente.
- Spec `000-problem-discovery` activa para gobernar la evaluación y el cierre de las puertas de datos.
- Reglas de evaluación `1.0` aprobadas por mayoría absoluta del equipo activo, con puertas críticas, matriz y gobierno de la selección.
- Dos candidatas evaluadas con la matriz `1.0`: reclamaciones CFPB y clasificación visual de residuos con RealWaste.
- `CAND-001` elegida por José, Abel, Víctor y Miguel con cuatro votos favorables, cero contrarios y cero abstenciones.
- La decisión autoriza el spike de viabilidad, pero no todavía el EDA completo, entrenamiento o implementación funcional.
- Arnés CFPB reproducible implementado con configuración versionada, probe API, muestra temporal en memoria, informes agregados y siete tests unitarios.
- Probe verificado: 2.306.723 narrativas, catorce etiquetas observadas, licencia CC0 informada por la API y clase mayoritaria del 72,45 %.
- G-03, G-04 y G-06 superadas para descubrimiento; G-02 y G-05 continúan condicionadas por mapping y privacidad.
- Workflow `repository-quality` ejecutado correctamente en Pull Request.
- Ruleset `Protect dev` activo con PR y check de calidad obligatorios, historial lineal y bloqueo de force push y borrado.
- Aprobaciones humanas no requeridas temporalmente.

## Capacidades previstas, no implementadas

- Pipeline de datos y entrenamiento.
- Aplicación multiclase.
- Persistencia y feedback.
- Docker y despliegue.
- CI/CD completo.
- Red neuronal, A/B testing, drift y promoción.

## Riesgos actuales

- Tratar una selección condicionada como si el dataset ya estuviera validado.
- Confundir estructura preparada con funcionalidad implementada.
- Los roles del equipo activo todavía no están asignados.
- La candidata CFPB necesita aprobar la normalización de tres etiquetas históricas o ambiguas y ampliar la validación de privacidad.
- El fuerte crecimiento de reclamaciones de informes de crédito puede producir desbalanceo extremo y cambios de procedencia que limiten la representatividad.
- La muestra temporal detecta drift de etiquetas y duplicación: el extremo de 2023 concentra la etiqueta histórica y muchos más duplicados que el extremo de 2026.
- La publicación reciente de narrativas presenta retraso y la API tiene comportamiento dependiente del cliente y paginación no trivial.
