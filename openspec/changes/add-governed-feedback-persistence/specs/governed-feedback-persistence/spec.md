## ADDED Requirements

### Requirement: Registro local minimizado de feedback

El sistema SHALL proporcionar una persistencia local de feedback humano que
registre únicamente identificadores técnicos, versiones, clases canónicas,
decisión, finalidad y marcas temporales de retención. El sistema SHALL NOT
persistir narrativas, audio, transcripciones, identidad, información de cuenta,
direcciones, IP, cabeceras ni texto libre.

#### Scenario: Feedback sintético conforme

- **WHEN** una revisión sintética contiene solo los campos permitidos y una
  clase canónica
- **THEN** el sistema la registra bajo el esquema versionado sin incluir
  contenido de la reclamación ni identidad personal

#### Scenario: Campo sensible o clase no canónica

- **WHEN** una revisión contiene un campo prohibido o una clase fuera del
  contrato
- **THEN** el sistema la rechaza con un error seguro y no persiste el registro

### Requirement: Almacén local controlado y reproducible

El sistema SHALL resolver el almacén bajo una raíz local configurada y
controlada, aplicar un esquema versionado con migraciones idempotentes y
rechazar rutas que escapen de esa raíz. El sistema SHALL NOT requerir red,
servicios cloud ni una base compartida para las pruebas locales.

#### Scenario: Inicialización repetible

- **WHEN** el almacén temporal se inicializa dos veces con la misma versión de
  esquema
- **THEN** el sistema conserva un esquema válido sin duplicar migraciones ni
  modificar archivos fuera de la raíz controlada

#### Scenario: Ruta externa

- **WHEN** se solicita una ruta de almacén fuera de la raíz configurada
- **THEN** el sistema la rechaza antes de crear o modificar un archivo

### Requirement: Retención y resumen agregados

El sistema SHALL asignar una retención finita a cada feedback, permitir la
purga idempotente de registros vencidos y devolver por defecto solo resúmenes
agregados por versión, clase y decisión. El sistema SHALL NOT usar el registro
para seleccionar, promover o reentrenar automáticamente un modelo.

#### Scenario: Purga de feedback vencido

- **WHEN** se ejecuta la purga sobre registros sintéticos vencidos y vigentes
- **THEN** elimina solo los vencidos y devuelve un contador agregado sin
  exponer registros individuales

#### Scenario: Consulta de seguimiento

- **WHEN** una persona solicita el resumen local de feedback
- **THEN** recibe solo contadores agregados y no recibe narrativas,
  identificadores individuales ni datos de identidad

### Requirement: Frontera con predicción y revisión humana

La ruta de predicción SHALL permanecer independiente de la persistencia de
feedback y la recomendación SHALL seguir requiriendo revisión humana. El
sistema SHALL registrar feedback únicamente mediante una operación explícita
posterior a la revisión.

#### Scenario: Predicción sin feedback

- **WHEN** ClaimVox procesa una predicción sin una decisión humana posterior
- **THEN** el sistema devuelve la respuesta contractual sin crear un registro
  de feedback
