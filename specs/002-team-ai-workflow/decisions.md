# Decisiones: Flujo de trabajo del equipo con IA

## ADR-001 Adoptar un flujo independiente de la herramienta de IA

- Fecha: `2026-07-22`
- Estado: `accepted`
- Relacionada con: `R-001, R-003 a R-008`

### Decisión

El repositorio, las specs, las tareas, los tests y las Pull Requests serán el contexto común. No se elegirá una IA obligatoria. Las herramientas con acceso al repositorio leerán `AGENTS.md`; las demás recibirán un paquete generado y acotado.

### Consecuencias

- El equipo puede cambiar de herramienta sin cambiar el método.
- Las conversaciones no sustituyen las decisiones versionadas.
- La persona que firma la PR mantiene la responsabilidad sobre el resultado.

## ADR-002 Utilizar React PWA como dirección frontend inicial

- Fecha: `2026-07-22`
- Estado: `accepted`
- Relacionada con: `R-002, R-009, AC-006`

### Decisión

La aplicación se desarrollará inicialmente con React y capacidades PWA. El objetivo aproximado es resolver en web instalable el 80 % del alcance antes de evaluar si requisitos reales justifican una evolución nativa.

### Consecuencias

- React PWA deja de ser una pregunta abierta.
- El framework de backend, la arquitectura de inferencia y la tecnología nativa continúan pendientes.
- La decisión no implica que la aplicación, PWA o experiencia nativa estén implementadas.
