# Brief para cliente — Estado del proyecto a 22 de julio de 2026

## Tipo

Presentación de negocio con respaldo técnico posterior.

## Audiencia

Cliente potencial, responsable de operaciones, atención al cliente o dirección de una organización que recibe reclamaciones financieras.

## Objetivo

Explicar con lenguaje normal qué problema queremos resolver, cómo sería la experiencia, qué valor se pretende validar, cómo protegemos la decisión humana y qué falta antes de disponer de un producto real.

## Regla narrativa principal

No comenzar con dataset, clasificación multiclase, React, PWA, API, SDD, arneses, CI/CD, modelos o MLOps.

Comenzar con esta secuencia:

```text
reto operativo
    ↓
persona afectada
    ↓
experiencia propuesta
    ↓
valor que queremos validar
    ↓
confianza, privacidad y control humano
    ↓
evidencia y estado real
    ↓
próximos pasos
```

## Mensaje principal

Queremos ayudar a que una organización comprenda y clasifique reclamaciones escritas de forma más consistente, manteniendo siempre la revisión y la decisión final en una persona.

## Narrativa sugerida

1. Una reclamación escrita debe entenderse antes de poder actuar sobre ella.
2. Cuando el volumen aumenta, la primera clasificación consume tiempo y puede variar entre personas.
3. Proponemos una herramienta que sugiera una familia de producto, muestre alternativas y reconozca cuándo necesita revisión.
4. La persona usuaria conserva la decisión; la herramienta no resuelve ni enruta automáticamente el caso.
5. El valor esperado es reducir esfuerzo y mejorar consistencia, pero todavía debe medirse con usuarios y casos reales autorizados.
6. El proyecto ya ha comprobado la viabilidad preliminar de los datos y dispone de un prototipo con respuestas simuladas para revisar la experiencia.
7. Antes de ofrecer una capacidad real quedan por cerrar el análisis de datos, privacidad, idioma, modelo, servicio y validación de negocio.

## Hechos obligatorios

- Dirección elegida por unanimidad por José, Abel, Víctor y Miguel.
- Fuente pública estudiada: Consumer Complaint Database del CFPB.
- Ventana preliminar: 2.306.723 reclamaciones con narrativa y once familias canónicas tras normalizaciones y una exclusión ambigua.
- Clase mayoritaria: 72,45 %, por lo que el equilibrio y el rendimiento por clase serán importantes.
- Existe una PWA contra mock en la PR #14; no existe modelo ni backend conectado.
- 30 tests Python/contrato y 5 tests frontend pasan localmente, junto con lint y build; CI de la PR estaba superada antes de esta actualización documental y deberá ejecutarse de nuevo al publicarla.
- Víctor analiza el CSV, Abel revisa frontend, José prepara backend sin implementar inferencia y Miguel coordina arquitectura.

## Afirmaciones prohibidas

- No afirmar que existe clasificación real, precisión, ahorro, cliente, despliegue o impacto medido.
- No llamar producto terminado al prototipo.
- No presentar el 72,45 % como rendimiento del modelo; es la proporción de la clase mayoritaria.
- No afirmar que las narrativas son completamente anónimas o que la privacidad está cerrada.
- No presentar autenticación, dashboard, voz, feedback, Docker o MLOps como implementados.

## Estructura sugerida

1. El reto de entender y dirigir reclamaciones.
2. La persona que toma la primera decisión.
3. La experiencia propuesta.
4. El valor que queremos validar.
5. Control humano, confianza y privacidad.
6. Evidencia disponible y prototipo.
7. Trabajo en curso y responsabilidades.
8. Próximos pasos y condiciones para una prueba real.
9. Anexo técnico opcional.

## Recursos visuales prioritarios

- Flujo simple desde reclamación hasta revisión humana.
- Capturas reales de la PWA cuando Abel complete `003/T-008`.
- Distribución de clases generada desde el EDA revisado.
- Diagrama actual frente a próximo paso, sin mostrar capacidades futuras como existentes.

## Fuentes principales

- `docs/notebooklm/business_narrative.md`.
- `docs/notebooklm/project_facts.md`.
- `docs/notebooklm/technical_status.md`.
- `docs/project_management/dailies/2026-07-22.md`.
- `reports/validation/cfpb_viability.md`.
- `reports/validation/complaint_routing_pwa.md`.
