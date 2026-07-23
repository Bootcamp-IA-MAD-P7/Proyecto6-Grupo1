# Plan técnico: Contrato de target CFPB

- Spec: [`spec.md`](spec.md)
- Estado: `in_progress`

## Estado actual comprobado

- El spike reproduce 2.306.723 narrativas y catorce etiquetas en la ventana congelada.
- Once etiquetas corresponden a la taxonomía vigente, dos tienen equivalencia semántica directa y una es ambigua.
- La narrativa es la única entrada admitida por `config/cfpb_viability.json`.
- El EDA está asignado a Víctor y permanece fuera de esta implementación.

## Solución propuesta

Versionar primero una política declarativa en `config/cfpb_target_contract.json` y proteger sus invariantes con tests. Después del EDA, implementar un constructor de dataset que consuma esa política, produzca únicamente metadatos agregados y prepare una clave de grupo sin persistir narrativas.

```text
fuente local excluida de Git
        ↓
filtro de elegibilidad
        ↓
normalización del target ──→ exclusiones cuantificadas
        ↓
huella de narrativa y grupos
        ↓
EDA / partición posterior sin leakage
```

## Contrato con el equipo de EDA

El equipo puede explorar distribución, tiempo, ausencias, longitudes, idioma y duplicados. No debe utilizar como features `product`, `sub_product`, `issue`, `sub_issue`, `company` ni campos posteriores. Entregará cifras y gráficos agregados; los notebooks versionados no mostrarán textos reales.

La spec acepta nueva evidencia del EDA. Si esa evidencia contradice una regla, se actualiza primero `spec.md` y se registra la decisión antes de cambiar el pipeline.

## Archivos previstos

- `config/cfpb_target_contract.json`: política ejecutable.
- `tests/unit/test_cfpb_target_contract.py`: invariantes del contrato.
- `scripts/data/`: futura implementación del target y grupos.
- `reports/validation/` o `reports/figures/`: evidencias agregadas del EDA.
- `specs/001-cfpb-target-contract/`: alcance, plan, tareas y decisiones.

## Estrategia de pruebas

- Unitarias: cardinalidad, mappings, exclusiones y separación feature/target.
- Contrato: etiquetas desconocidas fallan; las aliases solo apuntan a clases canónicas.
- Integración posterior: aplicar el contrato a una muestra local sin persistir narrativas.
- Validación manual: revisión cruzada entre cifras del EDA y contrato.

## Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| El EDA usa reglas diferentes | Resultados no comparables | JSON único y checklist en la spec |
| Duplicados cruzan particiones | Métricas infladas | Partición por huella de narrativa |
| Aparece otra etiqueta | Target incorrecto | Fallo explícito, nunca `other` automático |
| Se publica texto sensible | Riesgo de privacidad | Artefactos agregados y ejemplos sintéticos |
| La política se cierra antes del EDA | Decisiones débiles | Mantener idioma, deduplicación final y split como preguntas abiertas |

## Entrega y reversión

El cambio se integra mediante PR hacia `dev`. Revertirlo elimina la spec y el contrato sin alterar datos ni modelos, porque todavía no existe un pipeline dependiente.
