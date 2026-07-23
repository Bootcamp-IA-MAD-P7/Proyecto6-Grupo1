# Expediente 004: primera iteración del arnés

- ID: `004`
- Estado: `superseded`
- Responsable: `Miguel / arquitectura`
- Fecha de sustitución: `2026-07-23`
- Sustituido por: `openspec/specs/openspec-governance/spec.md`

## Propósito histórico

Este expediente definió la primera capa autoservicio: roles, procedimientos y un comando para proporcionar a distintas IA el mismo contexto, los mismos límites y el mismo ciclo de revisión.

La iteración demostró que era viable:

- componer instrucciones desde fuentes versionadas;
- limitar el trabajo por rol y tarea;
- impedir paquetes para tareas bloqueadas;
- excluir datos, secretos y narrativas;
- mantener commit, push, PR y merge bajo control humano;
- utilizar el mismo flujo con distintas herramientas.

## Motivo de la sustitución

La primera versión no proporcionaba por sí sola un motor estándar para propuestas, requisitos, diseño, tareas, validación y archivo. El checkpoint profesional exige OpenSpec real, instalado y reproducible.

Desde esta sustitución:

- OpenSpec gobierna todo cambio nuevo;
- `scripts/harness.py` consulta el estado e instrucciones de OpenSpec;
- `ai-specs/` conserva solo roles y procedimientos;
- este expediente y las demás carpetas numeradas permanecen únicamente para compatibilidad.

## Requisitos históricos conservados

- El flujo debe ser independiente del proveedor de IA.
- El contexto debe incluir intención, briefing, contratos, rol y comprobaciones.
- Una entrada inválida o bloqueada debe fallar sin salida parcial.
- No deben incorporarse datos brutos, narrativas CFPB, secretos, modelos ni logs.
- La persona responsable conserva revisión, decisiones y publicación.
- El proceso debe funcionar en Windows y GitHub Actions.

## Criterio vigente

La capacidad definitiva se considera implantada únicamente si:

1. la dependencia local de OpenSpec está fijada;
2. existen adaptadores oficiales para las herramientas acordadas;
3. el arnés consume la salida real de OpenSpec;
4. OpenSpec y las suites del repositorio se validan en CI;
5. el equipo dispone de un manual autoservicio;
6. un cambio real se valida y archiva.

La evidencia normativa vigente se encuentra en `openspec/specs/openspec-governance/spec.md` después del archivo del cambio de adopción.
