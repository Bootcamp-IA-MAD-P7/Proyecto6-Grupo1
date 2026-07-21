# Principios de calidad del proyecto

Estos principios convierten la experiencia de proyectos anteriores en criterios permanentes de trabajo.

## 1. Calidad casi comercial

El proyecto se abordará como un producto que podría enseñarse, probarse y evolucionarse con un cliente. El alcance académico no justifica una arquitectura improvisada ni documentación inconsistente.

## 2. Documentación como parte del producto

README, diagramas, tablas, métricas, decisiones y guías operativas evolucionarán junto al código. La documentación debe ser visual, verificable y reutilizable en presentaciones.

## 3. NotebookLM se alimenta con fuentes curadas

No se volcará el repositorio completo. Se mantendrán fuentes estables, actualizaciones diarias y briefs de presentación con hechos verificables.

## 4. CI/CD desde el inicio

Las primeras automatizaciones comprobarán la salud del repositorio y la documentación. Los quality gates de datos, modelo, aplicación, contenedores y despliegue se activarán conforme exista código real.

## 5. Diseño y UX desde la arquitectura

La interfaz no será una decoración final. Flujos, estados, accesibilidad, sistema visual y contenido se definirán antes de implementar pantallas.

## 6. Seguridad y encapsulamiento por defecto

Los secretos, datos, artefactos, dominio, casos de uso, infraestructura e interfaces tendrán límites claros. Las dependencias externas no deben penetrar innecesariamente en el núcleo del sistema.

## 7. Git como sistema de gobierno

Ramas, Pull Requests, tags, releases, issues, decisiones y automatizaciones proporcionarán trazabilidad. No se usarán únicamente como almacenamiento de código.

## 8. Evidencia antes que afirmaciones

Una capacidad solo se presenta como implementada cuando existe código, prueba, métrica o validación reproducible que la respalda.

## 9. Nivel experto sin sacrificar estabilidad

MLOps, redes neuronales y promoción de modelos se construirán sobre un núcleo esencial estable. Data Drift será una señal de revisión; nunca una justificación aislada para sustituir el modelo.

## 10. Presentación alineada con la realidad

README, NotebookLM, presentaciones y demo deben utilizar los mismos hechos, métricas, versiones y limitaciones.
