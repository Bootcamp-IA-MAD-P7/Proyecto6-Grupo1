# Plan técnico: Arnés agéntico de trabajo

- Spec: [`spec.md`](spec.md)
- Estado: `draft`

## Estado actual comprobado

El proyecto ya dispone de:

- reglas comunes en `AGENTS.md`;
- intención, specs, planes, tareas y decisiones versionadas;
- un generador seguro de handoff en `scripts/documentation/build_ai_handoff.py`;
- quality checks, tests, CI y plantilla de Pull Request;
- dailies, informes y documentación para conservar estado y evidencias.

Falta una entrada sencilla que conecte estas capacidades con roles y procedimientos reutilizables. La spec `002-team-ai-workflow` permanece como base cerrada; esta spec añade la capa operativa sin reabrirla ni duplicarla.

## Solución propuesta

Crear una capa mínima dentro de `ai-specs/`:

```text
ai-specs/
├── agents/       # Qué responsabilidad y límites tiene cada rol
└── skills/       # Cómo iniciar, verificar, revisar y preparar una PR
```

Una entrada de línea de comandos compondrá esas definiciones con el generador existente. La salida seguirá siendo un único Markdown efímero en `exports/`.

```text
rol + spec + tarea
        |
        v
validación de referencias y estado
        |
        v
AGENTS + rol + procedimiento + bundle de la spec
        |
        v
Markdown para cualquier IA
        |
        v
checks + revisión humana + PR
```

## Componentes y flujo

1. `agents`: arquitectura, datos, backend y frontend, con responsabilidades y límites.
2. `skills`: iniciar tarea, verificar tarea, revisar cambio y preparar PR.
3. `harness`: entrada única que valida y compone fuentes existentes.
4. `tests`: contratos de nombres, referencias, estados y seguridad.
5. `quickstart`: instrucciones humanas con ejemplos copiables.
6. `pilot`: generación y revisión del paquete de `001/T-004`.

## Datos, contratos y compatibilidad

- `AGENTS.md`, `specs/` y los contratos versionados siguen siendo las fuentes de verdad.
- `ai-specs/` solo explica cómo actuar; no redefine producto, datos ni arquitectura.
- `build_ai_handoff.py` se reutilizará directamente o mediante una capa compatible.
- Las salidas permanecerán ignoradas por Git.
- El arnés no leerá datasets, notebooks, modelos ni narrativas.
- Los comandos se diseñarán para PowerShell, Git Bash y GitHub Actions.

## Archivos o áreas previstas

- `ai-specs/README.md`
- `ai-specs/agents/*.md`
- `ai-specs/skills/*/SKILL.md`
- `scripts/harness.py` o una extensión compatible del generador actual
- `scripts/documentation/build_ai_handoff.py`, solo si la composición lo exige
- `tests/unit/`
- `.github/workflows/repository-quality.yml`
- `docs/project_management/harness_quickstart.md`
- documentación viva afectada

## Estrategia de pruebas

- Unitarias: validar roles, skills, spec, tarea, estados y rutas permitidas.
- Integración: generar el paquete completo para `001/T-004`.
- Contrato: comprobar secciones obligatorias y ausencia de fuentes prohibidas.
- End-to-end o smoke: seguir el manual hasta obtener un paquete y una propuesta de PR sin publicar cambios.
- Validación manual: una persona del equipo explica la tarea usando solo el Markdown generado.

## Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Duplicar specs o reglas | Confusión y contradicciones | Componer siempre desde fuentes actuales |
| Exceso de carpetas | Mayor coste de mantenimiento | Mantener solo cuatro roles y cuatro procedimientos iniciales |
| Automatización prematura | Flujo difícil de cambiar | Pilotar antes de integrar en CI |
| Falsa autonomía | Cambios sin control humano | Limitar el arnés a contexto, checks y preparación |
| Fuga de información | Riesgo de privacidad | Lista cerrada de fuentes documentales versionadas |
| Dependencia de Specboot | Bloqueo tecnológico | Adaptar conceptos, no instalarlo todavía |

## Entrega y reversión

La implementación se realizará en cambios pequeños dentro de esta rama. El primer punto de control será únicamente documental. La capa podrá retirarse eliminando `ai-specs/` y su entrada de composición, sin migrar specs, código de producto, datos ni historial.

No se instalarán dependencias ni se modificarán la PWA experimental, el EDA o los contratos de producto durante esta spec.

## Decisiones pendientes

- [ ] Elegir la forma final del comando tras probar dos ejemplos locales.
- [ ] Decidir si la validación entra en `repository-quality` después del piloto.
- [ ] Evaluar compatibilidad con Specboot u OpenSpec solo al cerrar esta primera versión.
