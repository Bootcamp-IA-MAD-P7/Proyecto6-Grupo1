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
