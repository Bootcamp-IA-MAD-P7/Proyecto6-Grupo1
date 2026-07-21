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
- specs activas;
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
2. Actualizar specs, decisiones y evidencias afectadas.
3. Revisar `source_catalog.md`.
4. Actualizar `daily_updates/YYYY-MM-DD.md` con los hechos que merecen llegar a NotebookLM.
5. Generar el paquete con `scripts/documentation/build_notebooklm_pack.py`.
6. Revisar el paquete antes de subirlo.
7. Mantener las presentaciones generadas como borradores hasta contrastar cifras y mensajes.

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
