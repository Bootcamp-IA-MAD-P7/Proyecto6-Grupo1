## ADDED Requirements

### Requirement: Identidad y madurez del prototipo comunicadas con precisión

La documentación de la capacidad `complaint-routing-interface` MUST usar la
identidad visible integrada de la interfaz y MUST comunicar que sigue siendo un
prototipo React PWA. La identidad visual MUST NOT alterar el contrato de
predicción ni utilizarse para afirmar que existen modelo entrenado, inferencia,
autenticación, administración, entrenamiento, registro de modelos o despliegue
operativos.

#### Scenario: Consulta del manual de frontend

- **WHEN** una persona consulte el README raíz, el manual de la interfaz o las
  fuentes de presentación después de una evolución visual integrada
- **THEN** encontrará la identidad actual, los límites de mock y la referencia
  a la evidencia de integración sin contradicciones entre documentos

#### Scenario: Pantallas propuestas conservadas

- **WHEN** la interfaz incluya rutas o pantallas de autenticación,
  administración, entrenamiento o modelos como propuesta visual
- **THEN** la documentación las mantendrá diferenciadas de las capacidades
  operativas y no las utilizará como evidencia de un nivel de entrega
