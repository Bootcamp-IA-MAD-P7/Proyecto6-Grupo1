## Context

El README contiene hechos correctos y enlaces útiles, pero mezcla la lectura de
una persona evaluadora con detalles de gobierno, estructura interna e historial
de trabajo. El nivel esencial está verificado para ejecución local y existe un
tag de corte, por lo que el documento puede priorizar una demostración breve y
la evidencia sin presentar el sistema como desplegado.

## Goals / Non-Goals

**Goals:**

- Reducir el tiempo necesario para localizar el valor, el recorrido local y la
  evidencia del MVP.
- Mantener métricas, límites, fuentes y enlaces alineados con los documentos
  canónicos.
- Separar la lectura ejecutiva de la guía de contribución y del gobierno del
  arnés mediante enlaces progresivos.

**Non-Goals:**

- No rediseñar ClaimVox ni cambiar código, API, modelo, datos o arquitectura.
- No sustituir informes, especificaciones, dailies ni la guía del arnés.
- No crear una presentación dentro del README ni modificar estados de Jira.

## Decisions

1. **Lectura progresiva en lugar de más contenido.** El README abrirá con valor,
   prueba local y evidencia; enlazará a documentos especializados para detalle.
   Alternativa descartada: duplicar informes y métricas, porque incrementaría
   contradicciones.
2. **Tablas breves con fuentes enlazadas.** Toda cifra, estado o afirmación de
   entrega apuntará a su informe o criterio canónico. Alternativa descartada:
   usar badges como única evidencia.
3. **Arquitectura actual y evolución separadas.** La representación actual
   mostrará PWA, API y modelo locales; una sección posterior describirá los
   límites y el roadmap sin anticipar despliegue, base de datos o MLOps.
4. **Narrativa de cliente primero.** La terminología de Harness Engineering se
   mantiene accesible mediante una sección breve y enlaces a su guía.

## Risks / Trade-offs

- [README demasiado largo] → usar secciones plegables conceptualmente mediante
  enlaces, tablas y detalles de segundo nivel.
- [Divergencia de métricas] → usar `delivery_levels.md` e informes de evaluación
  como fuente y comprobar enlaces antes de solicitar PR.
- [Sobrepromesa de producto] → repetir de forma visible que el alcance es local,
  revisable y no desplegado.

## Migration Plan

El cambio es editorial y reversible mediante la reversión de un único commit.
No hay migración de datos, compatibilidad de API ni cambio de configuración.

## Open Questions

Ninguna. El lenguaje visual del README conservará los recursos existentes y no
introducirá identidad distinta de ClaimVox.
