## 1. Preparación segura del constructor

- [x] 1.1 [Datos / ML] Confirmar que la fuente CFPB autorizada existe solo en `data/raw/`, está ignorada por Git y no se utilizará en fixtures, informes, logs, capturas ni prompts externos. Evidencia: `complaints.csv.zip` y el CSV extraído están bajo `data/raw/`; `git check-ignore` confirma fuente, etapa y corpus local ignorados. Las pruebas usan únicamente texto sintético y el manifiesto no incluye narrativas ni identificadores.
- [x] 1.2 [Datos / ML] Inventariar el comportamiento de `scripts/data/convert_cfpb_to_parquet.py` frente a `config/cfpb_target_contract.json` y definir los cambios mínimos para evolucionarlo sin duplicar pipeline. Evidencia: el conversor existente se ha extendido con rutas explícitas, contrato, manifest y control de conflictos; las pruebas están en `tests/unit/test_cfpb_training_dataset.py` y usan solo CSVs sintéticos temporales.
- [x] 1.3 [Datos / ML] Crear fixtures CSV estrictamente sintéticas y el esqueleto de pruebas unitarias e integración del constructor. Evidencia: `tests/unit/test_cfpb_training_dataset.py`; `python -m unittest tests.unit.test_cfpb_training_dataset -v` superado con seis pruebas sintéticas.

## 2. Construcción contractual del corpus local

- [x] 2.1 [Datos / ML] Adaptar el constructor para aceptar rutas explícitas de entrada y salida, cargar el contrato vigente y producir un corpus local en `data/processed/`. Evidencia: `build_training_dataset` recibe `input_path`, `output_path`, `manifest_path` y `contract_path`; las pruebas generan Parquet temporal y `data/.gitignore` protege el destino real.
- [x] 2.2 [Datos / ML] Aplicar de forma verificable la ventana temporal, los campos obligatorios, el mapping de aliases, la exclusión de la etiqueta ambigua y el fallo explícito ante etiquetas desconocidas. Evidencia: pruebas sintéticas de caso válido, alias, fecha/campo no elegible, exclusión ambigua y error de etiqueta desconocida.
- [x] 2.3 [Datos / ML] Limitar el corpus resultante a las columnas autorizadas para pasos posteriores y eliminar identificadores de reclamación no necesarios del artefacto procesado. Evidencia: prueba de `OUTPUT_COLUMNS`; el Parquet no contiene `Complaint ID` ni `Product` de origen.

## 3. Duplicados, privacidad y repetibilidad

- [x] 3.1 [Datos / ML] Calcular la huella de narrativa definida por el contrato y excluir grupos con targets canónicos contradictorios. Evidencia: prueba sintética de dos targets sobre la misma narrativa normalizada y conteos agregados de exclusión.
- [x] 3.2 [Datos / ML] Conservar la huella para grupos no conflictivos sin colapsarlos ni ponderarlos. Evidencia: prueba que conserva dos filas del mismo target y la misma huella; la política intra-grupo sigue abierta en el contrato.
- [x] 3.3 [Datos / ML] Generar un manifiesto agregado de fuente, contrato, población, exclusiones, clases, duplicados y conflictos, sin narrativas ni identificadores de reclamación. Evidencia: prueba de manifiesto JSON y `reports/validation/cfpb_training_dataset_manifest.json` generado sobre la fuente local; ninguno contiene narrativas ni identificadores de filas.
- [x] 3.4 [Datos / ML] Verificar que dos ejecuciones sobre la misma fuente sintética y el mismo contrato producen los mismos recuentos de control. Evidencia: prueba de repetibilidad sobre la misma fuente sintética.

## 4. Validación y trazabilidad

- [x] 4.1 [Datos / ML] Ejecutar las pruebas del constructor y registrar los resultados reales. Verificación: `python -m unittest tests.unit.test_cfpb_training_dataset -v` superado: 6 pruebas, 0 fallos.
- [x] 4.2 [Datos / ML] Ejecutar las comprobaciones transversales. Verificación: `python scripts/quality/check_repository.py`, `git diff --check` y `npm exec -- openspec validate build-cfpb-training-dataset --type change --strict` superados el 27 de julio de 2026.
- [x] 4.3 [Datos / ML] Actualizar `specs/001-cfpb-target-contract/tasks.md` para reflejar la evidencia real de `T-005`, sin cerrar `T-006` dentro de este cambio ni presentar el corpus como listo para entrenar. Evidencia: `T-005` recoge constructor, tests, informe y artefactos locales; `T-006` se cerró posteriormente mediante el cambio independiente `decide-cfpb-training-policy`.
- [x] 4.4 [Miguel / coordinación] Actualizar únicamente la documentación cuyo significado cambie, las fuentes de NotebookLM y el estado de Jira `PG-2` con enlaces a evidencias reales. Evidencia: README, changelog, daily, fuentes de NotebookLM, informe y tarea heredada actualizados; `PG-2` quedó en `Listo` tras la fusión de la PR `#27`.
- [x] 4.5 [Miguel / coordinación] Preparar la Pull Request hacia `dev` con la plantilla completada, las limitaciones explícitas y los comandos de verificación; no fusionar sin revisión humana. Evidencia: PR `#27` fusionada mediante revisión humana; conserva explícitamente que no existe modelo ni inferencia real.
