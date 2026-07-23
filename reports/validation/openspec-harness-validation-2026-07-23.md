# Validación de OpenSpec + Harness Engineering — 2026-07-23

## Resultado

`PASS` local. La validación remota de GitHub Actions se registrará en la Pull Request antes del merge.

## Alcance comprobado

- dependencia local y lockfile;
- configuración y primer cambio OpenSpec;
- adaptadores oficiales para cinco herramientas;
- integración entre OpenSpec y `scripts/harness.py`;
- compatibilidad limitada con tareas numeradas;
- calidad automática;
- documentación, estructura, privacidad y reversión;
- README y recursos visuales;
- paquete curado para NotebookLM.

## Evidencia funcional

El cambio `adopt-openspec-harness` se creó con OpenSpec real. El arnés:

1. comprueba Node.js y la dependencia local;
2. ejecuta `openspec doctor`;
3. valida todos los artefactos en modo estricto;
4. consume `status` e `instructions apply` en JSON;
5. bloquea planificación incompleta o tareas pendientes;
6. genera un Markdown únicamente desde fuentes documentales versionadas.

El comando real:

```bash
python scripts/harness.py start \
  --role architect \
  --change adopt-openspec-harness
```

generó localmente:

```text
exports/ai-handoffs/harness-start-architect-openspec-adopt-openspec-harness.md
```

La salida está excluida de Git.

El cambio se validó y archivó como `2026-07-23-adopt-openspec-harness`; el archivo creó la capacidad vigente `openspec/specs/openspec-governance/spec.md` con diez requisitos y diez escenarios.

## Comprobaciones

```text
python scripts/harness.py doctor
PASS Node.js 24.18.0
PASS OpenSpec 1.6.0
PASS OpenSpec project root
PASS OpenSpec strict validation

npm run openspec:validate
1 passed, 0 failed

npm audit --audit-level=high
0 vulnerabilities

python -m unittest discover -s tests/unit -p "test_*.py" -v
39 tests passed

python -m unittest discover -s tests/contract -p "test_*.py" -v
7 tests passed

python scripts/quality/check_repository.py
passed

git diff --cached --check
no output
```

Los SVG del README se analizaron como XML válido y se renderizaron en Chrome para comprobar recortes, jerarquía, legibilidad y coherencia de estados.

## Revisión adversarial

| Riesgo buscado | Resultado |
|---|---|
| OpenSpec solo nominal | No: dependencia, CLI, configuración, cambio, validación y archivo están integrados |
| Dos fuentes de verdad permanentes | Mitigado: `specs/` queda congelado para cambios nuevos |
| Dependencia global por persona | No: `npm ci` instala la versión exacta |
| Herramienta de IA obligatoria | No: cinco adaptadores y CLI universal |
| Estado reconstruido por el arnés | No: consume JSON del OpenSpec local |
| Ruta externa o datos sensibles | Bloqueados y cubiertos por tests |
| Telemetría en arnés o CI | Desactivada mediante `OPENSPEC_TELEMETRY=0` |
| PR con tareas pendientes | Bloqueada por `prepare-pr` |
| Documentación que exagera producto | README distingue contratos, previsto e implementado |
| Presentación iniciada por jerga técnica | El paquete NotebookLM comienza por narrativa y hechos de negocio |

## Límites

- La implantación del método no demuestra modelo, aplicación, backend, despliegue o MLOps.
- Los adaptadores oficiales facilitan el uso, pero cada integrante sigue revisando el resultado de su herramienta.
- Víctor y Abel conservan un modo heredado para no rehacer trabajo; cualquier decisión nueva se adapta mediante OpenSpec.
- Jira queda para un cambio posterior porque aún no se ha definido proyecto, clave ni política de sincronización.

## Reversión

La PR puede revertirse sin perder datos, código de producto ni expedientes anteriores. La reversión elimina:

- dependencia y lockfile de OpenSpec;
- `openspec/`;
- adaptadores oficiales;
- modo OpenSpec del arnés;
- puertas OpenSpec de CI.

El flujo numerado anterior permanece recuperable en el commit previo.
