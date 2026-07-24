# Estrategia CI/CD

## Principio

CI/CD comienza desde la fundación, pero sus puertas crecen con el producto. No se simulan checks de una aplicación todavía inexistente.

## Etapa 0 — Fundación

Activa desde el primer PR:

- integridad de la estructura;
- enlaces Markdown internos;
- nomenclatura de dailies;
- ausencia de archivos sensibles o demasiado grandes;
- `git diff --check`;
- permisos mínimos del workflow.
- instalación reproducible con `npm ci`;
- auditoría de dependencias npm;
- diagnóstico y validación estricta de OpenSpec;
- suites unitarias y de contrato.

Workflow: `.github/workflows/repository-quality.yml`.

## Etapa 1 — Contratos de datos y ML esencial

<<<<<<< HEAD
Estado: parcialmente activa para contratos y tests Python; el pipeline de datos y entrenamiento todavía no existe.
=======
Se añadirá cuando existan paquetes y dependencias de ML:
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83

- instalación reproducible;
- lint y tipos;
- tests de integridad de datos con muestras controladas;
- tests del preprocessing;
- tests de entrenamiento reducido;
- validación del contrato del artefacto;
- umbrales de métricas en fixtures o resultados versionados.

## Etapa 2 — Aplicación

Estado: parcialmente activa para la React PWA mock.

- tests de componentes y estados;
- contrato de inferencia verificado;
- lint y build de interfaz en CI;
- reglas automatizadas de accesibilidad;
- Dependabot para npm;
- integración real, feedback y análisis adicional de dependencias pendientes de specs futuras.

## Etapa 3 — Contenedores y staging

- build de imágenes.
- escaneo de vulnerabilidades.
- ejecución como usuario no privilegiado.
- health/readiness.
- smoke test con servicios reales de staging.
- migraciones verificadas.

## Etapa 4 — Producción

```text
PR -> CI -> dev -> release PR -> main -> build inmutable -> staging -> aprobación -> producción -> smoke -> rollback si falla
```

- Credenciales temporales mediante OIDC cuando el proveedor lo permita.
- GitHub Environments separados.
- Aprobación manual de producción al principio.
- Artefacto idéntico entre staging y producción.
- Despliegue detenido si falla cualquier quality gate.
- Rollback documentado y probado.

## Etapa 5 — MLOps

- validación de datos y esquema;
- comparación Challenger/Champion;
- generación de informes de experimento;
- drift y calidad del servicio;
- evaluación de política de promoción;
- promoción separada del despliegue de aplicación;
- aplicación explícita, auditable y reversible.

## Estrategia de entornos

| Entorno | Propósito | Datos | Despliegue |
|---|---|---|---|
| Local | Desarrollo | Sintéticos o controlados | Manual |
| CI | Verificación efímera | Fixtures | Automático |
| Staging | Validación integrada | No sensibles | Automático desde release candidato |
| Producción | Servicio real | Según política aprobada | Controlado desde `main` |
