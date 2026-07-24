# Validación de Jira, OpenSpec y el arnés

## Identificación

- Fecha: 2026-07-23.
- Cambio OpenSpec: `integrate-jira-workflow`, archivado como
  `openspec/changes/archive/2026-07-23-integrate-jira-workflow/`.
- Rama: `chore/integrate-jira-workflow`.
- Jira: proyecto `PG`.
- Alcance: seguimiento operativo del nivel esencial y transporte seguro de la
  referencia Jira en el arnés.

## Resultado

La integración fue revisada por Miguel y archivada correctamente. Jira conserva responsable,
estado y bloqueos; OpenSpec conserva requisitos y decisiones; GitHub conserva la
implementación y la evidencia. No se han incorporado credenciales ni narrativas
CFPB.

## Backlog comprobado

| Clave | Tipo | Padre | Estado verificado | Asignación verificada |
|---|---|---|---|---|
| `PG-1` | Epic | — | Por hacer | Sin asignar |
| `PG-2` | Historia | `PG-1` | En curso | Víctor González Trapero |
| `PG-3` | Tarea | `PG-1` | Por hacer | Sin asignar |
| `PG-4` | Historia | `PG-1` | En curso | Abel Cañas |
| `PG-5` | Tarea | `PG-1` | Por hacer | Sin asignar |
| `PG-6` | Historia | `PG-1` | Por hacer | Sin asignar |
| `PG-7` | Tarea | `PG-1` | Por hacer | Sin asignar |

No se ha asignado la cuenta de José ni responsables no confirmados.

## Dependencias comprobadas

```text
PG-2 blocks PG-3
PG-2 blocks PG-5
PG-3 blocks PG-5
PG-3 blocks PG-6
PG-3 blocks PG-7
PG-4 blocks PG-6
PG-5 blocks PG-6
PG-6 blocks PG-7
```

La primera escritura de las relaciones utilizó la orientación inversa de la API.
La lectura de control permitió detectarlo antes del cierre. Se retiraron los ocho
enlaces y se recrearon; la lista anterior procede de la lectura final de Jira.

## Arnés comprobado

- `--jira PG-N` acepta referencias válidas y rechaza formatos inválidos.
- `--jira-exception` solo acepta `bootstrap`, `emergency` o `automation`.
- Un cambio OpenSpec sin Jira ni excepción se bloquea.
- `001/T-004`, `003/T-006` y `003/T-007` se relacionan automáticamente con
  `PG-2`, `PG-4` y `PG-5`.
- Una clave manual que contradice el mapping heredado se rechaza.
- Los paquetes incluyen la referencia de seguimiento y no requieren conexión,
  token ni secreto de Atlassian.

Paquetes locales utilizados:

```text
exports/ai-handoffs/harness-start-architect-openspec-integrate-jira-workflow.md
exports/ai-handoffs/harness-start-data-analyst-001-cfpb-target-contract-T-004.md
```

`exports/` permanece fuera de Git.

## Comprobaciones

```text
npm audit --audit-level=high
found 0 vulnerabilities

python scripts/harness.py doctor
PASS Node.js 24.18.0
PASS OpenSpec 1.6.0
PASS OpenSpec project root
PASS OpenSpec strict validation (3 items)

npm run openspec:validate
3 passed, 0 failed

python -m unittest discover -s tests/unit -p "test_*.py" -v
48 tests passed

python -m unittest discover -s tests/contract -p "test_*.py" -v
7 tests passed

python -m compileall -q scripts tests
No output — passed.

python scripts/quality/check_repository.py
Repository quality checks passed.

git diff --cached --check
No output — passed.
```

## Límites

- El ticket no acredita una capacidad de producto implementada.
- No existe todavía modelo, inferencia real, aplicación integrada o despliegue.
- La ejecución y el feedback del piloto de Víctor sobre `PG-2` siguen pendientes.
- La integración no sincroniza estados automáticamente ni guarda credenciales.
- El push, la Pull Request y el merge siguen requiriendo autorización y revisión
  humana; el archivo OpenSpec fue autorizado y completado antes del commit.
