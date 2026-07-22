# Tareas: Experiencia de clasificación de reclamaciones

- Spec: [`spec.md`](spec.md)
- Plan: [`plan.md`](plan.md)

## T-001 Definir flujo y límites del producto

- Estado: `[x]`
- Responsable: `Producto / UX`
- Requisitos cubiertos: `R-001, R-002, R-006 a R-010, R-012`
- Evidencia obtenida: spec y arquitectura de información con estados y fuera de alcance explícitos.

## T-002 Versionar el contrato de inferencia simulado

- Estado: `[x]`
- Responsable: `Aplicación / plataforma`
- Dependencias: `T-001`
- Requisitos cubiertos: `R-003 a R-005, R-007, R-009, R-011, R-012`
- Evidencia obtenida: `docs/api/openapi.json` y tests contra las once clases.

## T-003 Completar límites iniciales de seguridad

- Estado: `[x]`
- Responsable: `Seguridad / aplicación`
- Dependencias: `T-001, T-002`
- Requisitos cubiertos: `R-002, R-006 a R-009, R-011`
- Evidencia obtenida: modelo de amenazas actualizado y extensiones de tratamiento en OpenAPI.

## T-004 Validar el contrato documental

- Estado: `[x]`
- Responsable: `QA`
- Dependencias: `T-002, T-003`
- Requisitos cubiertos: `AC-004, AC-005, AC-007`
- Evidencia obtenida: tests automatizados de esquema, clases, privacidad, revisión y rutas.

## T-005 Contrastar el flujo con negocio

- Estado: `[!]`
- Responsable: `Producto / equipo`
- Dependencias: `T-001`
- Requisitos cubiertos: `Q-001, Q-005, Q-006`
- Bloqueante: falta una persona usuaria o responsable de negocio con quien contrastar el flujo.
- Evidencia obtenida: pendiente.

## T-006 Implementar la React PWA con mock

- Estado: `[x]`
- Responsable: `Frontend / UX`
- Dependencias: `T-001 a T-004`
- Requisitos cubiertos: `AC-001 a AC-004, AC-006`
- Trabajo: crear shell PWA, formulario, cliente mock, resultado y estados accesibles.
- Evidencia obtenida: React PWA, cliente mock sustituible, 5 tests de interacción, lint accesible, build con service worker y [informe de validación](../../reports/validation/complaint_routing_pwa.md).

## T-007 Integrar el servicio real

- Estado: `[!]`
- Responsable: `Aplicación / ML`
- Dependencias: `T-006`, `001/T-004 a T-006`
- Bloqueante: EDA, modelo aprobado, idioma, límites y política de revisión.
- Evidencia obtenida: pendiente.

## T-008 Endurecer y revisar la entrega frontend

- Estado: `[~]`
- Responsable: `Abel / Frontend / UX`
- Dependencias: `T-006`
- Requisitos cubiertos: `R-010, R-013, R-014, AC-006, AC-008, AC-009`
- Trabajo:
  - revisar la implementación existente en `app/interface/` sin recrearla en `/frontend`;
  - comprobar teclado, foco y estados con tecnología asistiva disponible;
  - revisar móvil, tablet y escritorio y conservar capturas con contenido sintético;
  - completar iconos e instalabilidad PWA;
  - ejecutar Lighthouse registrando versión, entorno y resultados;
  - medir cobertura antes de proponer un umbral obligatorio;
  - activar Dependabot para npm y actualizar las evidencias afectadas.
- Verificación: `npm run typecheck`, `npm run lint`, `npm test`, `npm run build`, revisión manual y actualización del informe de validación.
- Evidencia obtenida: Dependabot npm incorporado durante la reconciliación; revisión manual, capturas, iconos, Lighthouse y cobertura pendientes.

## Checklist de cierre

- [x] Contrato y estados iniciales están definidos.
- [x] Las clases y límites de privacidad están verificados.
- [ ] El flujo ha sido validado con negocio.
- [x] La PWA consume el contrato mediante mock.
- [ ] La integración real cumple las decisiones de datos y modelo.
- [ ] Existen evidencias de accesibilidad y responsive.
- [ ] `T-008` dispone de evidencias de instalabilidad, dependencias, capturas y calidad frontend.
