## 1. Política versionada

- [x] 1.1 [Datos/ML] Crear una configuración versionada de política que fije las huellas de fuente y contrato, el alcance en inglés, los grupos de duplicados, el objetivo temporal 70/15/15, `macro F1`, `class_weight="balanced"` y los límites de privacidad. Verificar que no contiene narrativas, identificadores ni rutas locales.
- [x] 1.2 [Datos/ML] Añadir pruebas sintéticas para que una fuente o contrato con huella distinta detenga la preparación antes de generar particiones.
- [x] 1.3 [Datos/ML] Registrar en `specs/001-cfpb-target-contract/` la decisión aprobada para `T-006`, sin marcarla completada hasta que exista evidencia de idioma y partición local.

## 2. Preparación de idioma y grupos

- [x] 2.1 [Datos/ML] Seleccionar e implementar un detector de idioma determinista, versionado y reproducible para aceptar solo inglés en el baseline inicial, sin registrar textos en errores, informes ni pruebas.
- [x] 2.2 [Datos/ML] Generar localmente un manifiesto agregado de idioma con recuentos de inclusión y exclusión por clase; mantener los artefactos con narrativas en rutas ignoradas por Git.
- [x] 2.3 [Datos/ML] Añadir pruebas sintéticas que demuestren la exclusión de idioma no inglés o no clasificable y que los grupos duplicados no conflictivos se conservan completos.

## 3. Partición temporal sin leakage

- [x] 3.1 [Datos/ML] Implementar la partición temporal por grupo usando la fecha máxima de cada huella, con objetivo 70/15/15 para train, validation y test.
- [x] 3.2 [Datos/ML] Validar localmente que ninguna huella cruza particiones, que el orden temporal se conserva y que cada clase tiene el soporte mínimo aprobado; detener el flujo y documentar el bloqueo si no se cumple.
- [x] 3.3 [Datos/ML] Generar una evidencia agregada versionable con huellas, límites de fecha, tamaños efectivos, distribución de clases y exclusiones, sin narrativas ni identificadores.
- [x] 3.4 [Datos/ML] Añadir pruebas sintéticas para orden temporal, aislamiento de grupos, reproducibilidad y protección del test.

## 4. Preparación del baseline y cierre documental

- [x] 4.1 [Datos/ML] Crear el contrato de ejecución del baseline para `class_weight="balanced"`, macro F1 como métrica primaria y control train-validation menor de 0.05, sin entrenar ningún modelo en este cambio.
- [x] 4.2 [Documentación] Actualizar README, CHANGELOG, fuentes de NotebookLM y la daily solo con decisiones y evidencias realmente obtenidas; diferenciar política aprobada, preparación implementada y entrenamiento pendiente.
- [x] 4.3 [Verificación] Ejecutar los tests sintéticos de la política, `python scripts/quality/check_repository.py`, `git diff --check` y `npm exec -- openspec validate decide-cfpb-training-policy --type change --strict`; registrar resultados reales.
- [x] 4.4 [Jira/PR] Tras revisión humana, actualizar `PG-2` con el enlace de evidencia y el estado real de `T-006`; abrir una Pull Request hacia `dev` sin marcar `ESS-02`, `PG-2` ni `PG-3` como terminados sin toda su evidencia. Evidencia: PR `#27` fusionada y `PG-2` actualizada a `Listo`; `ESS-02` permanece en curso y `PG-3` pendiente de baseline.
