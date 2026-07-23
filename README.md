# Proyecto de Clasificación Multiclase

Repositorio del Proyecto 6 del Grupo 1.

<p align="center">
  <img alt="Estado: descubrimiento" src="https://img.shields.io/badge/estado-descubrimiento-315C66">
  <img alt="Rama de integración: dev" src="https://img.shields.io/badge/integración-dev-4C6B50">
  <img alt="Calidad: SPEC y CI" src="https://img.shields.io/badge/calidad-SPEC%20%2B%20CI-7A5C3E">
</p>

## Estado actual

El proyecto se encuentra en fase de descubrimiento y validación de datos.

El equipo ha elegido por unanimidad la clasificación y el enrutamiento de reclamaciones financieras mediante narrativas públicas del CFPB. La decisión es condicional: antes de implementar deben validarse la extracción, las clases, el desbalanceo, la calidad y la privacidad.

El spike preliminar ha verificado 2.306.723 narrativas, catorce etiquetas observadas y un desbalanceo severo. La API y el contrato narrative-only son reproducibles. La spec [`001-cfpb-target-contract`](specs/001-cfpb-target-contract/spec.md) fija once clases canónicas y las reglas compartidas para el EDA; idioma y privacidad siguen abiertos antes de entrenar.

La spec [`003-complaint-routing-experience`](specs/003-complaint-routing-experience/spec.md) define el flujo React PWA y un OpenAPI para trabajar con mocks. Son contratos verificables, no una aplicación ni un servicio implementados.

La spec [`004-agentic-harness`](specs/004-agentic-harness/spec.md) proporciona una primera versión operativa del arnés de trabajo: cada integrante puede generar desde `dev` un contexto limitado por rol, spec y tarea para utilizarlo con la IA que prefiera. La herramienta está automatizada y verificada; su adopción continúa en evaluación mediante el piloto con Víctor.

Todavía no se han decidido de forma definitiva:

- la política de idioma y el tratamiento final de duplicados;
- la estrategia de partición y desbalanceo basada en el EDA;
- la métrica principal;
- el framework de backend y el contrato de inferencia;
- la arquitectura de despliegue.

La estructura inicial prepara el repositorio para evolucionar desde el nivel esencial hasta el nivel experto del briefing, sin presentar ninguna capacidad como implementada antes de tiempo.

## Objetivo académico

Construir una solución de clasificación supervisada multiclase con un mínimo de tres clases, análisis exploratorio, evaluación por clase, aplicación de inferencia y control de overfitting inferior al 5 %.

El alcance aspiracional incluye modelos ensemble, validación cruzada, optimización, feedback, recolección de datos, Docker, base de datos, despliegue, tests, redes neuronales y un ciclo MLOps con A/B testing, Data Drift y promoción controlada de modelos.

## Evolución prevista

```mermaid
flowchart LR
    D[Descubrimiento] --> E[Nivel esencial]
    E --> M[Nivel medio]
    M --> A[Nivel avanzado]
    A --> X[Nivel experto]

    classDef discovery fill:#E8F0F2,stroke:#315C66,color:#1F3439
    classDef essential fill:#E8F1E9,stroke:#4C6B50,color:#253A28
    classDef medium fill:#F3EEDF,stroke:#8A7441,color:#443819
    classDef advanced fill:#F3E7DD,stroke:#9A603A,color:#4A2D1C
    classDef expert fill:#ECE7F2,stroke:#67547A,color:#33283D

    class D discovery
    class E essential
    class M medium
    class A advanced
    class X expert
```

| Nivel | Resultado protegido | Estado |
|---|---|---|
| Descubrimiento | Idea, usuario, datos y viabilidad | Idea elegida; datos en validación |
| Esencial | Solución multiclase completa y demostrable | En curso: EDA activo |
| Medio | Champion, feedback y recolección | No iniciado |
| Avanzado | Contenedores, persistencia, cloud y tests | No iniciado |
| Experto | Challenger, A/B, drift y promoción gobernada | No iniciado |

## Estructura

```text
.
├── .specify/              # Intención, método y plantillas para trabajar con specs
├── specs/                 # Una carpeta por funcionalidad o cambio relevante
├── app/                   # Capa de entrega: interfaz y, si aplica, API
├── config/                # Configuración versionada no sensible
├── data/                  # Datos por etapa del procesamiento
├── docs/                  # Arquitectura, decisiones y gestión del proyecto
├── infra/                 # Docker y despliegue en la nube
├── models/                # Artefactos y metadatos de modelos
├── notebooks/             # Exploración y experimentos narrativos
├── reports/               # Métricas, figuras y evidencias de validación
├── scripts/               # Automatizaciones reproducibles
├── src/                   # Código reutilizable de datos, ML y MLOps
└── tests/                 # Pruebas por nivel
```

La responsabilidad de cada carpeta se detalla en [docs/architecture/repository_structure.md](docs/architecture/repository_structure.md).

## Pilares de calidad

| Pilar | Aplicación desde el inicio |
|---|---|
| Producto y UX | Investigación, flujos, accesibilidad y sistema visual antes de las pantallas. |
| Datos y ML | Contratos, reproducibilidad, evaluación por clase y test final protegido. |
| Plataforma | Docker y CI/CD diseñados desde la fundación, activados por etapas. |
| Seguridad | Secretos, datos, dependencias y permisos con mínimo privilegio. |
| Documentación | README, diagramas, evidencias, dailies y fuentes curadas para NotebookLM. |
| Gobierno | Specs, ADR, PR, tags, releases y quality gates trazables. |

## Forma de trabajo

Los cambios relevantes seguirán este flujo:

```text
intent -> spec -> plan -> tareas -> implementación -> verificación -> cierre
```

La [intención del proyecto](.specify/intent.md) fija el propósito y los límites globales. La guía está en [.specify/README.md](.specify/README.md) y las normas de colaboración en [CONTRIBUTING.md](CONTRIBUTING.md).

### Incorporación rápida al equipo

1. Seguir la [guía autoservicio para trabajar con IA](docs/project_management/harness_quickstart.md).
2. Leer [`AGENTS.md`](AGENTS.md): resume decisiones y límites vigentes.
3. Consultar la asignación en [`team.md`](docs/project_management/team.md).
4. Localizar la spec y tarea desde [`specs/`](specs/README.md).
5. Utilizar Jira para el estado diario y una Pull Request para integrar evidencias.

Cada integrante genera desde su propio clon un contexto acotado mediante `scripts/harness.py`. Las IA con acceso al repositorio leen el paquete local; para una herramienta externa se sube únicamente ese Markdown. Nunca se comparten datos brutos ni narrativas CFPB.

## Ramas

- `dev`: rama de integración y rama predeterminada durante el desarrollo.
- `main`: se reservará para versiones estables cuando exista una primera entrega verificable.
- Ramas de trabajo: se crearán desde `dev` y volverán mediante Pull Request.

## Objetivos de madurez

- [Mapa de niveles y evidencias](docs/project_management/delivery_levels.md)
- [Principios de calidad del proyecto](docs/project_management/project_principles.md)
- [Gobierno Git y releases](docs/project_management/git_governance.md)
- [Estrategia CI/CD](docs/project_management/ci_cd_strategy.md)

## Documentación viva

La documentación se considera parte del producto. Debe alimentar el trabajo diario, las revisiones, las presentaciones y las fuentes curadas para NotebookLM.

- [Sistema de fuentes para NotebookLM](docs/notebooklm/README.md)
- [Dailies del equipo](docs/project_management/dailies/README.md)
- [Estándar visual de documentación](docs/design/documentation_visual_standard.md)
- [Blueprint arquitectónico](docs/architecture/system_blueprint.md)
- [Baseline de seguridad](docs/security/security_baseline.md)
- [Estrategia de pruebas](docs/quality/test_strategy.md)

## Próximo hito

El trabajo activo se concentra en dos objetivos:

- Datos/ML: recibir el EDA de Víctor e incorporarlo a [`001-cfpb-target-contract`](specs/001-cfpb-target-contract/spec.md) para cerrar idioma, duplicados, partición, desbalanceo y privacidad antes de entrenar.
- Arquitectura y método: pilotar con Víctor desde `dev` la spec [`004-agentic-harness`](specs/004-agentic-harness/spec.md) y utilizar su feedback para cerrar la primera versión.

La React PWA permanece como propuesta experimental en una Pull Request separada y no forma parte del estado integrado en `dev`. Antes de retomarla deberá actualizarse desde `dev` y revisarse con Abel.
