## Context

`T-005` ha construido un corpus local reproducible y ha confirmado que la instantánea descargada el 27 de julio no coincide con la del EDA anterior. Antes de `PG-3` el equipo necesitaba una política que evitara cambiar la población, el idioma, los duplicados, el split y el desbalanceo entre experimentos. Esa política ya se ha aplicado localmente y ha generado las tres particiones protegidas; no se ha entrenado ningún modelo.

La política se vincula a `PG-2` y a la tarea heredada `001/T-006`. No modifica el contrato de once clases ni crea todavía particiones o modelos.

## Goals / Non-Goals

**Goals:**

- Convertir las cinco decisiones aprobadas en requisitos comprobables.
- Establecer una referencia de fuente y contrato que impida comparar experimentos sobre poblaciones distintas.
- Aplicar y comprobar las condiciones de preparación que usarán los experimentos de baseline.
- Mantener privacidad, trazabilidad y test protegido.

**Non-Goals:**

- Entrenar, seleccionar o evaluar modelos.
- Escoger una arquitectura ML, hacer tuning o usar el test final.
- Cambiar el target, la React PWA, el backend, infraestructura o Jira.
- Publicar corpus, textos CFPB, muestras, logs o capturas de datos reales.

## Decisions

### Fuente y contrato fijados por huella

La referencia inicial será el ZIP local cuya huella consta en `reports/validation/cfpb_training_dataset_manifest.json`, junto al contrato actual. Una huella distinta exige una decisión nueva, no una sustitución silenciosa.

Alternativa considerada: reutilizar las cifras del EDA sin distinguir fuente. Se descarta porque el EDA anterior tiene otra instantánea y contaminaría la reproducibilidad.

### Inglés para el primer baseline

El primer baseline se limita a inglés, en consonancia con el EDA que observó predominio de inglés. Se ha elegido `langdetect 1.0.9` con semilla `0` y un máximo de 500 caracteres; las exclusiones quedan en un manifiesto agregado.

Alternativa considerada: entrenar multilingüe desde el inicio. Se descarta para el baseline porque introduce complejidad de representación y evaluación sin haber demostrado valor adicional.

### Grupos completos y partición temporal

Los conflictos de target se excluyen. Los duplicados no conflictivos se conservan completos y se asignan según su fecha máxima a una sola partición temporal. La preparación buscará 70/15/15 y ajustará límites de fecha solo para mantener clases mínimas, dejando registrado el resultado efectivo.

Alternativa considerada: split aleatorio estratificado por fila. Se descarta porque permitiría leakage de narrativas idénticas y una estimación temporal demasiado optimista.

### Macro F1 y pesos de clase en el baseline

Macro F1 será la métrica de selección inicial para proteger las clases minoritarias. El baseline aplicará pesos balanceados y no re-muestreo; accuracy, métricas por clase y F1 weighted complementan la lectura.

Alternativa considerada: usar accuracy o F1 weighted como métrica primaria. Se descarta porque la clase mayoritaria domina ambas señales en este corpus. El re-muestreo se pospone hasta compararlo de forma reproducible.

### Privacidad y promoción de resultados

Datos y artefactos con narrativas se mantienen locales. Las evidencias compartidas solo contienen huellas, recuentos y configuración. El test se usa una sola vez, tras seleccionar un candidato con validation.

## Risks / Trade-offs

- [El detector de idioma excluye inglés válido] → cuantificar exclusiones y revisar sus distribuciones agregadas antes de fijar el baseline.
- [Un split temporal deja una clase rara con soporte insuficiente] → registrar límites efectivos y detener la preparación para revisión, sin mover filas manualmente.
- [La fuente CFPB se actualiza] → comprobar la huella antes de cada preparación y abrir cambio nuevo si difiere.
- [Macro F1 empeora la lectura de volumen] → acompañarla siempre de accuracy y métricas por clase.
- [Conservar duplicados aumenta peso efectivo de grupos] → mantenerlo explícito y compararlo solo en un cambio posterior.

## Migration Plan

1. Versionar la política aprobada y actualizar la tarea heredada.
2. Implementar el detector, el manifiesto de idioma y el split temporal por grupos en artefactos locales ignorados por Git.
3. Validar los datos locales y la evidencia agregada sin publicar narrativas.
4. Crear un cambio independiente para entrenar y evaluar el baseline.

La reversión consiste en revertir esta decisión antes de crear particiones; no modifica ni elimina la fuente ni el corpus local existentes.

## Open Questions

- Qué detector determinista de idioma ofrece la mejor relación entre reproducibilidad y precisión para textos de reclamación.
- Qué definición de referencia usar para la siguiente actualización pública del CFPB si la huella cambia.

El equipo aprobó el 27 de julio un mínimo de 100 filas por clase tanto en validation como en test. La preparación debe detenerse si no lo alcanza.
