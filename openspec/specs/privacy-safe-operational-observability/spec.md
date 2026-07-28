# privacy-safe-operational-observability Specification

## Purpose

Establecer la observabilidad técnica mínima de la ejecución local sin incorporar
identidad, contenido de reclamaciones ni persistencia por defecto.

## Requirements

### Requirement: Eventos técnicos sin contenido ni identidad

El servicio SHALL emitir un evento técnico estructurado al completar una
predicción válida. El evento SHALL limitarse a campos operativos aprobados y
SHALL NOT incluir narrativas, audio, transcripciones, alternativas, confianza
individual, IP, usuario, correo, credenciales ni hashes de identidad.

#### Scenario: Predicción local completada

- **WHEN** el servicio completa una solicitud de predicción válida
- **THEN** el evento técnico contiene solo resultado HTTP, duración, modo del predictor, versión del modelo y estado de revisión humana

### Requirement: Retención y destino explícitos

La aplicación SHALL NOT persistir eventos de observabilidad ni enviarlos a un
tercero por defecto. La documentación SHALL identificar que el destino y la
retención dependen del entorno local y requieren una decisión específica antes de
recopilar feedback o exponer el servicio.

#### Scenario: Ejecución local por defecto

- **WHEN** se inicia el servicio con la configuración del repositorio
- **THEN** los eventos se dirigen solo al canal técnico local configurado y no crean archivos, tablas ni cuentas de usuario
