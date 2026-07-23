## Context

El proyecto `PG` existe en Jira Cloud y está vacío. El repositorio ya dispone de OpenSpec, tareas heredadas, roles, Pull Requests protegidas y un arnés local. Crear tickets sin una frontera explícita duplicaría requisitos y obligaría a mantener dos versiones del mismo alcance.

La integración debe funcionar con cualquier IA y desde cualquier clon. Por seguridad, el repositorio no almacenará tokens de Atlassian ni dependerá de una conexión Jira para ejecutar tests o CI.

## Goals / Non-Goals

**Goals:**

- hacer visible quién trabaja, el estado y los bloqueos;
- enlazar cada unidad de entrega con su cambio OpenSpec, rama y PR;
- permitir que el arnés valide y transporte una clave Jira;
- crear un backlog inicial pequeño y útil;
- evitar duplicidad entre Jira, OpenSpec, dailies y GitHub.

**Non-Goals:**

- replicar cada requisito o checkbox en Jira;
- sincronizar estados automáticamente mediante credenciales;
- crear todo el nivel medio, avanzado y experto antes de refinarlos;
- asignar personas que todavía no tengan cuenta o acceso confirmado;
- presentar un ticket como evidencia de implementación.

## Decisions

### Frontera entre sistemas

| Sistema | Responsabilidad |
|---|---|
| Jira | responsable, estado operativo, prioridad y bloqueo |
| OpenSpec | propuesta, requisitos, diseño, tareas y decisiones |
| GitHub | ramas, commits, pruebas, revisión y evidencia |
| Daily | coordinación diaria y comunicación del equipo |

Jira enlaza a la fuente versionada; no copia documentos completos.

### Jerarquía inicial

- Un Epic representa un resultado amplio y defendible.
- Una Historia representa valor o capacidad visible.
- Una Tarea representa trabajo técnico o documental.
- Las subtareas solo se crean cuando facilitan coordinación real.

El primer Epic será el nivel esencial. No se crearán todavía Epics vacíos para niveles futuros.

### Backlog inicial aprobado

| Clave | Tipo | Resultado | Fuente versionada | Dependencias |
|---|---|---|---|---|
| `PG-1` | Epic | Alcanzar el nivel esencial | `docs/project_management/delivery_levels.md` | — |
| `PG-2` | Historia | Completar EDA y decisiones de datos | `001/T-004` | — |
| `PG-3` | Tarea | Entrenar y evaluar el baseline | Cambio OpenSpec por crear | `PG-2` |
| `PG-4` | Historia | Construir la React PWA | `003/T-006` | Puede usar mocks |
| `PG-5` | Tarea | Implementar el backend de inferencia | `003/T-007` | `PG-2`, `PG-3` |
| `PG-6` | Historia | Integrar predicción y revisión humana | Cambio OpenSpec por crear | `PG-3`, `PG-4`, `PG-5` |
| `PG-7` | Tarea | Consolidar métricas e informe técnico | Cambio OpenSpec por crear | `PG-3`, `PG-6` |

El equipo activo aprobó el desglose antes de escribir en Jira. Las incidencias se
crearon inicialmente sin asignación técnica. Jira confirma después a Víctor en
`PG-2` y Abel en `PG-4`; José y el resto de responsables siguen sin confirmarse.

### Piloto delimitado

El primer uso real será `PG-2` / `001/T-004`: Víctor generará su contexto con el
modo heredado, que incorpora `PG-2` automáticamente, y comunicará fricciones o
decisiones nuevas antes de integrar el EDA. La preparación técnica del piloto
queda verificada en este cambio; la ejecución y el feedback de Víctor permanecen
pendientes y no bloquean la implantación del mecanismo.

### Secuencia sin circularidad

1. Crear y revisar la propuesta OpenSpec.
2. Presentar el desglose Jira y obtener aprobación.
3. Crear Epic e historias.
4. Añadir la clave Jira al cambio y comenzar implementación.

El cambio de bootstrap `integrate-jira-workflow` queda documentado como excepción porque crea el propio mecanismo de tracking.

### Convenciones

- Cambio OpenSpec: nombre estable en kebab-case.
- Jira: `PG-N`.
- Rama nueva: `tipo/PG-N-descripcion-corta`.
- PR: campo Jira obligatorio o excepción explicada.
- El arnés aceptará `--jira PG-N`, validará el formato e incluirá la referencia en el paquete.

Las tareas heredadas de Víctor y Abel recibirán historias Jira sin cambiar sus IDs de compatibilidad.

### Seguridad

- Sin tokens, cookies, credenciales o datos Jira en Git.
- Sin narrativas CFPB en Jira.
- Descripciones limitadas a contexto, requisitos resumidos, aceptación y enlaces.
- La automatización conectada se usa bajo autorización humana; el CLI local solo valida referencias.

## Risks / Trade-offs

- Doble mantenimiento de estados. → Jira es operativo; las evidencias y requisitos no se copian.
- Miembros sin acceso a Jira. → Crear tickets sin asignación técnica hasta confirmar cuentas.
- Ramas existentes sin clave Jira. → Compatibilidad documentada para trabajo ya iniciado.
- Exceso de tickets. → Primer backlog limitado a un Epic y seis elementos de entrega.
- Estado Jira desactualizado. → Daily y revisión de PR incluyen una comprobación breve de coherencia.

## Migration Plan

1. Versionar contrato, pruebas y manual.
2. Presentar y aprobar el backlog inicial.
3. Crear Epic e historias en `PG`.
4. Incorporar claves a documentación y arnés.
5. Pilotar con una tarea real.
6. Archivar el cambio y publicar mediante PR.

Rollback: retirar la validación de claves y conservar los tickets como histórico; no afecta al producto ni a los datos.

## Open Questions

- Cuentas Jira de José, Abel y Víctor.
- Si el equipo utilizará estimaciones o sprints; no son necesarios para el primer backlog.
