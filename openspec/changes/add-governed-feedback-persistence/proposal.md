# Propuesta: persistencia gobernada de feedback

## Contexto

ClaimVox dispone de inferencia local bajo configuración explícita y conserva la
revisión humana como requisito. Actualmente no existe persistencia: una decisión
de revisión no puede asociarse de forma trazable a una versión de modelo ni
utilizarse como evidencia para mejorar el flujo. `PG-14` define la base local y
gobernada que necesitarán la recogida de feedback (`PG-13`) y una futura
recolección para reentrenamiento.

La persistencia no debe convertirse en un registro de reclamaciones. El contrato
de predicción ya prohíbe conservar la narrativa en salidas, logs y ficheros, y
este cambio mantiene esa restricción.

## Objetivo

Definir e implementar una persistencia local mínima, validada y reproducible
para decisiones humanas de revisión, con finalidad, retención y trazabilidad
explícitas, sin almacenar narrativas CFPB ni identidad personal.

El registro candidato podrá contener únicamente:

- un identificador técnico no personal de la decisión;
- el identificador de predicción y las versiones de modelo y taxonomía ya
  presentes en la respuesta contractual;
- clase sugerida, clase confirmada o corrección humana dentro de las once
  clases canónicas;
- decisión de revisión, marca temporal y finalidad declarada;
- metadatos de retención y procedencia necesarios para auditoría local.

## Alcance propuesto

- Diseñar un esquema local versionado y una interfaz de persistencia separada
  de la ruta de predicción.
- Exigir validación de clases, versiones, marcas temporales y campos permitidos
  antes de escribir o recuperar un registro.
- Aplicar mínimo privilegio al acceso local y una política explícita de
  retención, borrado y exportación agregada.
- Generar pruebas sintéticas de creación, rechazo de campos sensibles,
  trazabilidad, retención y acceso controlado.
- Preparar evidencia agregada para `MED-04` y `MED-05`, sin declararlos
  verificados hasta que sus flujos completos y políticas dependientes existan.

## Fuera de alcance

- Almacenar narrativas, audio, transcripciones, direcciones, cuentas, nombres
  u otro dato personal.
- Autenticación, autorización multiusuario, cuentas reales o permisos de
  producción.
- Base de datos compartida o gestionada, despliegue, secretos, observabilidad
  operativa, MLOps o reentrenamiento automático.
- Modificar la predicción, sus métricas, la selección de modelo, frontend o
  contratos públicos existentes sin una decisión posterior aprobada.
- Declarar `ADV-02`, `MED-04` o `MED-05` verificados solo por crear esta
  propuesta.

## Decisiones que se concretarán en el diseño

- Motor local, ruta controlada y ciclo de vida del almacén.
- Esquema de registro, claves, índices, migraciones y mecanismo de mínimo
  privilegio compatible con el entorno local.
- Retención por defecto, borrado, exportación agregada y límites de volumen.
- Punto de integración futuro con el servicio y la interfaz sin incluir la
  narrativa ni modificar la decisión de revisión humana.
- Evidencia mínima para pasar de persistencia local implementada a feedback y
  recolección gobernados.

## Trazabilidad y éxito

- Jira: `PG-14`.
- Dependencias: contrato de predicción vigente y límites de privacidad de
  ClaimVox.
- Relación de entrega: prepara `MED-04` y `MED-05`; puede contribuir a
  `ADV-02`, pero no lo verifica por sí mismo.
- Éxito: diseño, requisitos y tareas trazables que permitan implementar una
  persistencia local sin introducir narrativas reales, identidad, permisos de
  producción ni capacidades no evidenciadas.
