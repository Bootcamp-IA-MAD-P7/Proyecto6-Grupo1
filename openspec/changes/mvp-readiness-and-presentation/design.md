## Context

ClaimVox dispone de un baseline multiclase reproducible, una API FastAPI local y una PWA React que puede usar esa API bajo configuración explícita. El nivel esencial está verificado para ejecución local, pero no hay despliegue, autenticación, base de datos, persistencia de feedback, monitorización operativa ni modelo Champion. El repositorio ya evita registrar cuerpos de petición y no incluye narrativas CFPB reales; esa protección no se debe debilitar al hacer más visible el comportamiento técnico.

La documentación principal es amplia, aunque necesita una lectura más directa para una persona evaluadora, y la entrega no tiene aún un tag Git que señale el corte de MVP. Los criterios posteriores del briefing requieren un mapa Jira único que conserve dependencias y evidencia mínima sin prometer su ejecución.

## Goals / Non-Goals

**Goals:**

- Convertir el README en punto de entrada profesional para demo, arquitectura, evidencia, seguridad, escalabilidad y límites.
- Añadir observabilidad técnica local que permita diagnosticar salud, latencia, resultado técnico y versión del modelo sin almacenar contenido ni identidad.
- Reducir riesgos evidentes de la API local mediante límite de tamaño, cabeceras de respuesta y frecuencia configurable con pruebas.
- Revisar límites de módulos y dependencias para aplicar mejoras pequeñas y medibles sin reescribir PWA, backend ni pipeline ML.
- Definir el corte `v0.1.0-essential-mvp`, el mapa Jira posterior y una narrativa NotebookLM que sea comprensible antes de explicar la tecnología.

**Non-Goals:**

- No crear autenticación, perfiles de usuario, base de datos, analítica de marketing, despliegue, Docker, cloud, MLOps ni un Champion.
- No guardar narrativas, audio, transcripciones, direcciones IP, correos, identificadores de dispositivo ni predicciones individuales.
- No realizar cambios de diseño visual que sustituyan las decisiones de Abel.
- No convertir las tareas futuras de Jira en criterios verificados ni alterar métricas o datos existentes.

## Decisions

### Observabilidad de mínimo dato y sin identidad

La API emitirá eventos estructurados solo a su salida técnica local. Cada evento podrá contener tipo de evento, timestamp, duración redondeada, código HTTP, modo del predictor, versión del modelo y si se exige revisión humana. No tendrá body, narrativa, alternativas, confianza individual, IP, usuario ni hash de identidad. La aplicación no persistirá esos eventos; la retención depende del destino de logs del entorno y se documentará como local o efímera.

Registrar cuerpo y predicción para depurar queda descartado por privacidad. Crear ya una tabla de usuarios o feedback también queda fuera: exige propósito, permisos, retención, borrado y seguridad que pertenecen a un cambio posterior. Integrar una plataforma externa añade transferencia de datos y credenciales sin necesidad para el MVP.

### Protección proporcional para una API solo local

Se aprueba un máximo contractual de **5.000 caracteres** por narrativa y un
máximo predeterminado de **20 solicitudes de predicción por minuto por cliente
local temporal**. Ambos valores se exponen como configuración local: el límite
de caracteres solo puede reducirse respecto al máximo contractual y el de
frecuencia se puede ajustar para pruebas. La clave de frecuencia vive solo en
memoria durante la ejecución; no se registra, persiste ni se usa para perfilar
personas.

El servicio aplicará ese límite explícito, rate limiting en memoria configurable
y cabeceras de seguridad adecuadas para respuestas API. No se añadirá HSTS ni
una política de despliegue HTTPS al servidor local. El limitador será best-effort
para desarrollo local, no un control distribuido de producción; se documentará
ese límite.

No se usarán Redis, base de datos, CORS abierto ni credenciales para implementar estos controles.

### Mejora de código basada en frontera y evidencia

La auditoría revisará rutas, servicio de predicción, adaptadores de predictor, configuración y cliente HTTP de la PWA. Solo se extraerán componentes o funciones cuando reduzcan acoplamiento, duplicación o coste verificable. Cada refactor conservará OpenAPI, once clases, estados seguros y pruebas existentes.

### README como puerta de entrada; fuentes especializadas como evidencia

El README resumirá sin duplicar problema, demo local, arquitectura, evidencia, seguridad, escalabilidad, repositorio y límites. Los informes, specs y guías seguirán siendo las fuentes de detalle. NotebookLM utilizará una narrativa de cliente que empiece por el problema y la revisión humana, y usará métricas y arquitectura solo después de explicar valor y límites.

### Release tag solo después de evidencia y revisión

`v0.1.0-essential-mvp` será un tag anotado creado sobre un commit de `dev` después de fusionar esta entrega y revisar que el nivel esencial sigue 10/10. El tag no certifica despliegue ni producción; identifica un corte reproducible de MVP local. La creación del tag no será automática.

## Risks / Trade-offs

- [Logs locales copiados fuera del equipo] → eventos sin contenido ni identidad y revisión del destino antes de desplegar.
- [Rate limiting insuficiente en varias instancias] → declararlo in-memory y local; exigir un diseño distribuido antes de exponer la API.
- [README demasiado extenso] → priorizar resumen y enlaces, sin repetir informes.
- [Refactor introduce regresiones] → cambios pequeños, tests contractuales y build antes de integrar.
- [Tag entendido como versión productiva] → nombre y documentación explícitos: `essential-mvp`, ejecución local y revisión humana.
- [Backlog Jira se convierta en promesa] → cada ticket llevará evidencia mínima y dependencia, no una afirmación de implementación.

## Migration Plan

1. Inventariar documentación, configuración y puntos de logging actuales.
2. Definir y probar los controles locales antes de activarlos por defecto.
3. Actualizar README, fuentes NotebookLM y documentación de seguridad con evidencias reales.
4. Crear o actualizar el mapa Jira y enlazar el cambio OpenSpec correspondiente.
5. Preparar PR, ejecutar quality gates y revisión humana.
6. Tras merge, crear el tag anotado desde `dev` y verificar su trazabilidad.

Reversión: revertir el commit de cada control o documento; no hay migración de datos ni estado persistente que recuperar.

## Open Questions

- Si la demo requiere una pantalla visible de estado técnico o basta con documentación y respuestas seguras.
- Qué responsable y cadencia tendrá la revisión de métricas una vez exista feedback con una política de privacidad aprobada.
- Qué claves Jira se crearán para el backlog posterior; este cambio no inventará claves inexistentes.
