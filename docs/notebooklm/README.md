# Sistema de fuentes para NotebookLM

## Objetivo

Alimentar NotebookLM de forma frecuente con información curada, coherente y verificable para producir presentaciones de alta calidad sin exponerle el ruido completo del repositorio.

## Principio

NotebookLM debe recibir una selección editorial, no un volcado indiscriminado de archivos.

```text
Fuentes estables
     +
Actualización diaria
     +
Evidencia técnica y visual
     +
Brief de presentación
     ↓
Paquete curado para NotebookLM
```

## Capas de fuentes

### 1. Núcleo estable

Documentos que cambian con poca frecuencia:

- visión e intención del producto, cuando se definan;
- arquitectura y estructura;
- principios de diseño y seguridad;
- decisiones aceptadas;
- metodología y niveles de entrega.

### 2. Estado vivo

Documentos actualizados conforme avanza el proyecto:

- README;
- changelog;
- cambios y capacidades OpenSpec;
- expedientes numerados únicamente cuando aporten contexto histórico necesario;
- estado de tareas;
- dailies;
- catálogo de fuentes;
- resumen técnico y narrativa de negocio.

### 3. Evidencia

Material que respalda afirmaciones:

- métricas estructuradas;
- figuras y gráficos;
- capturas reales de la aplicación;
- resultados de tests;
- informes de validación;
- decisiones Champion/Challenger y monitorización.

### 4. Brief de presentación

Define audiencia, duración, narrativa, tono, hechos obligatorios, afirmaciones prohibidas y recursos visuales.

## Flujo diario

1. Completar la daily del equipo.
2. Actualizar OpenSpec, decisiones y evidencias afectadas.
3. Revisar `source_catalog.md`.
4. Actualizar `project_facts.md`, `technical_status.md` y `business_narrative.md` únicamente cuando cambien sus hechos.
5. Generar el paquete con `scripts/documentation/build_notebooklm_pack.py`.
6. Revisar el paquete antes de subirlo.
7. Mantener las presentaciones generadas como borradores hasta contrastar cifras y mensajes.

## Orden para una presentación de cliente

Una presentación orientada a cliente no comienza por specs, Git, nombres de herramientas o arquitectura. El orden editorial recomendado es:

```text
problema y contexto
        ↓
persona afectada y decisión
        ↓
experiencia propuesta
        ↓
valor y confianza
        ↓
evidencia y limitaciones
        ↓
detalle técnico necesario
```

`business_narrative.md`, `project_facts.md` y el brief de la presentación son las fuentes de entrada. `AGENTS.md`, las tareas y los documentos del arnés sirven para control interno y presentación técnica, no para abrir la historia de negocio.

La daily canónica pertenece a `docs/project_management/dailies/`. NotebookLM la consume directamente como fuente versionada; no mantiene una copia ni una adaptación diaria paralela.

## Qué no se debe subir como fuente principal

- repositorio completo;
- código fuente sin explicación;
- datasets crudos;
- logs extensos;
- secretos o configuración privada;
- resultados temporales no validados;
- documentación histórica superada;
- imágenes decorativas sin relación con el producto.

## Calidad visual

Las fuentes visuales deben utilizar gráficos reales, diagramas claros, capturas del producto y una identidad coherente. Se evitarán robots, cerebros digitales, circuitos, chispas o iconografía genérica asociada a IA.

## Salida generada

Los paquetes se generan en:

```text
exports/notebooklm/YYYY-MM-DD-notebooklm-pack.md
```

`exports/` no se versiona. Las fuentes originales sí permanecen trazables en el repositorio.

El archivo generado es un contenedor de revisión, no una autorización para utilizar todas sus fuentes en cualquier presentación. La persona responsable selecciona la audiencia y revisa el orden narrativo antes de subirlo.
