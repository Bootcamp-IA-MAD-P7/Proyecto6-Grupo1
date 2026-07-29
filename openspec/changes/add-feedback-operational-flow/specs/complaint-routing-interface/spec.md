## MODIFIED Requirements

### Requirement: Revisión humana y siguiente acción

La interfaz MUST presentar la recomendación como apoyo, comunicar
`review_required` y permitir a la persona revisar el resultado o iniciar una
nueva clasificación sin convertir la recomendación en una decisión automática.
Cuando el servicio local de feedback esté configurado, la interfaz SHALL ofrecer
una acción posterior y explícita de vocabulario cerrado para registrar la
revisión, sin enviar la narrativa, texto libre, identidad ni probabilidades
completas. Si el registro no está disponible o falla, SHALL comunicarlo de forma
segura sin alterar el resultado de predicción.

#### Scenario: Revisión requerida

- **GIVEN** una respuesta con `review_required` igual a `true`
- **WHEN** se muestra el resultado
- **THEN** la necesidad y sus motivos serán comprensibles sin depender solo del color

#### Scenario: Registro explícito de feedback local

- **GIVEN** una respuesta local válida y un servicio de feedback configurado
- **WHEN** la persona elige una decisión permitida y, cuando corresponda, una
  clase canónica revisada
- **THEN** la interfaz envía exclusivamente los metadatos aprobados después de
  la predicción y confirma o informa el error sin modificar la recomendación

#### Scenario: Nueva clasificación

- **GIVEN** que la persona ha terminado de revisar un resultado
- **WHEN** inicia una nueva clasificación
- **THEN** la vista volverá al formulario sin conservar la narrativa anterior en almacenamiento persistente
