# Decisiones: Arnés agéntico de trabajo

## ADR-001 Adoptar los principios de Harness Engineering de forma incremental

- Fecha: `2026-07-23`
- Estado: `accepted`
- Relacionada con: `R-001, R-002, R-006, R-011`

### Contexto

El proyecto ya tiene una base SDD propia y funcional. Instalar directamente otra estructura podría duplicar specs, instrucciones y comandos antes de demostrar qué necesita realmente el equipo.

### Opciones consideradas

1. Instalar Specboot u OpenSpec y migrar el repositorio.
2. Adaptar primero los principios de instrucciones, herramientas, entorno, estado y retroalimentación.
3. Mantener el flujo actual sin una capa agéntica.

### Decisión

Se adopta la opción 2. Se construirá una capa mínima sobre la estructura existente y se evaluará una integración externa después del piloto.

### Consecuencias

- Beneficios: menor riesgo, aprendizaje gradual y reutilización de lo que ya funciona.
- Costes o límites: no estarán disponibles inicialmente todos los comandos de Specboot.
- Trabajo posterior: comparar la primera versión con Specboot y OpenSpec usando evidencia del equipo.

### Evidencia

La spec `002-team-ai-workflow` ya proporciona reglas, generación segura y un flujo independiente del proveedor.

## ADR-002 Mantener una única jerarquía de specs

- Fecha: `2026-07-23`
- Estado: `accepted`
- Relacionada con: `R-001, R-003, R-004`

### Contexto

La información de producto y trabajo ya reside en `.specify/` y `specs/`. Una segunda jerarquía convertiría el arnés en otra fuente de verdad.

### Opciones consideradas

1. Copiar las specs dentro de `ai-specs/`.
2. Sustituir `specs/` por una estructura nueva.
3. Hacer que la capa agéntica referencie las specs actuales.

### Decisión

Se adopta la opción 3. `ai-specs/` contendrá únicamente roles y procedimientos; nunca copiará contratos de producto ni estados de tareas.

### Consecuencias

- Beneficios: menor duplicación y trazabilidad clara.
- Costes o límites: la composición debe validar enlaces entre varias fuentes.
- Trabajo posterior: crear tests que detecten referencias inexistentes.

### Evidencia

`AGENTS.md` ya establece el flujo `spec -> plan -> tasks -> implementation -> verification -> closure`.

## ADR-003 Mantener la revisión y publicación bajo control humano

- Fecha: `2026-07-23`
- Estado: `accepted`
- Relacionada con: `R-005, R-009, R-011`

### Contexto

El objetivo es mejorar contexto y retroalimentación, no delegar decisiones irreversibles ni el gobierno del repositorio.

### Opciones consideradas

1. Automatizar cambios, commits, publicación y merge.
2. Automatizar contexto y verificaciones, dejando diff, commit, PR y merge bajo confirmación humana.

### Decisión

Se adopta la opción 2. La persona responsable revisará los cambios, las evidencias y la Pull Request antes de cualquier publicación.

### Consecuencias

- Beneficios: seguridad, aprendizaje del equipo y responsabilidad clara.
- Costes o límites: el ciclo conserva pasos manuales deliberados.
- Trabajo posterior: evaluar automatizaciones adicionales solo cuando existan controles y una necesidad demostrada.

### Evidencia

El ruleset de `dev` y la guía de contribución ya exigen Pull Request y quality gates.

## ADR-004 Componer el arnés sobre el generador existente

- Fecha: `2026-07-23`
- Estado: `accepted`
- Relacionada con: `R-002 a R-010 | AC-001 a AC-006 | T-004`

### Contexto

`build_ai_handoff.py` ya valida specs, tareas, seguimiento Git, formatos y áreas prohibidas. Reimplementar esas protecciones en otra herramienta crearía dos comportamientos difíciles de mantener.

### Opciones consideradas

1. Sustituir el generador por una herramienta nueva.
2. Copiar su lógica dentro de un comando del arnés.
3. Crear una entrada pequeña que lo componga con rol, procedimiento y validación de estado.

### Decisión

Se adopta la opción 3. `scripts/harness.py` utiliza una acción posicional y opciones explícitas para rol, spec y tarea. El generador original conserva su uso anterior y recibe parámetros opcionales para título, instrucciones y nombre seguro de salida.

### Consecuencias

- Beneficios: una única política de seguridad, compatibilidad con el flujo anterior y uso equivalente en PowerShell y Git Bash.
- Costes o límites: los dos scripts quedan relacionados y deben probarse juntos.
- Trabajo posterior: integrar la suite conjunta en CI después del piloto.

### Evidencia

El comando real de inicio generó un paquete para `001/T-004`; los tests cubren roles y acciones inválidos, tareas bloqueadas, estados incompatibles y compatibilidad del generador original.

## ADR-005 Crear la estructura de forma incremental

- Fecha: `2026-07-23`
- Estado: `accepted`
- Relacionada con: `R-001, R-005, R-011, T-005, T-006`

### Contexto

El repositorio contenía 46 archivos `.gitkeep`; 42 de esos marcadores ya no aportaban contenido y anticipaban aplicación, modelos, MLOps, infraestructura, recursos o pruebas futuras. Esa estructura aumentaba el ruido para personas y agentes y podía confundirse con capacidades implementadas.

### Opciones consideradas

1. Mantener todo el árbol previsto hasta nivel experto.
2. Eliminar también los contratos y mapas de arquitectura futuros.
3. Conservar los README y mapas de responsabilidad, pero crear subcarpetas únicamente con su primer archivo real.

### Decisión

Se adopta la opción 3. Se conservan las cuatro etapas locales de `data/` porque forman parte del EDA activo. Las demás subcarpetas aparecerán en la Pull Request que incorpore su primera implementación, configuración, prueba o evidencia.

### Consecuencias

- Beneficios: menos ruido, navegación más clara y menor riesgo de presentar intención como capacidad.
- Costes o límites: cada nueva capacidad deberá crear explícitamente su ruta inicial.
- Trabajo posterior: revisar el mapa de estructura cuando se incorporen modelo, PWA, infraestructura o MLOps reales.

### Evidencia

La corrección elimina 42 archivos `.gitkeep` y conserva únicamente las cuatro etapas locales de datos utilizadas por el trabajo activo.
