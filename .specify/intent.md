# Intención del proyecto

| Campo | Valor |
|---|---|
| Estado | Vigente |
| Fase | Entrega local verificada y evolución gobernada |
| Alcance | Global del proyecto |
| Responsable | Equipo |
| Última revisión | 2026-07-31 |

## Función de este documento

Este documento define por qué existe el proyecto, qué resultados debe proteger y qué principios deben gobernar las decisiones. Es el contrato de mayor nivel del repositorio.

No sustituye a una spec funcional. El intent cambia únicamente cuando cambia el propósito global; las decisiones de producto y las funcionalidades se definen después mediante specs, planes, tareas y registros de decisión.

## Declaración de intención

> Identificar un problema real en el que una predicción multiclase mejore una decisión concreta y construir una solución de machine learning reproducible, útil, segura, comprensible y desplegable, respaldada por evidencia técnica y documentación apta para negocio.

## Propósito

El proyecto grupal busca demostrar la capacidad de transformar un problema real en un producto de clasificación supervisada multiclase. La solución deberá recibir datos de entrada, devolver una única clase entre tres o más alternativas y explicar su comportamiento con métricas, análisis de errores y evidencia reproducible.

El equipo protegerá primero una entrega esencial completa. Las capacidades avanzadas y expertas se incorporarán de forma incremental cuando el núcleo sea estable y aporten valor verificable.

## Restricciones confirmadas

### Producto y machine learning

- El problema deberá corresponder a clasificación supervisada multiclase con un mínimo de tres clases mutuamente excluyentes.
- La predicción deberá apoyar una decisión comprensible para un usuario o actor identificado.
- La solución deberá incluir una aplicación que reciba entradas y devuelva una predicción.
- La evaluación deberá incluir métricas globales y por clase, matriz de confusión, importancia de variables y análisis de errores cuando sean aplicables.
- La diferencia acordada entre rendimiento de entrenamiento y validación deberá mantenerse por debajo del 5 %. La fórmula y métrica concretas se fijarán en la spec de evaluación.
- El proceso de datos, entrenamiento y evaluación deberá ser reproducible.

### Entrega y operación

- El repositorio, el historial Git y las Pull Requests forman parte de la entrega.
- Deben existir un informe técnico, una presentación para negocio y una presentación técnica.
- El trabajo debe mantenerse trazable mediante specs, tareas, decisiones, dailies y una herramienta compartida de organización.
- La aplicación se desplegará; Docker, CI/CD, seguridad y operación deben considerarse desde el diseño y activarse de forma incremental.
- La documentación deberá aportar fuentes verificables y curadas para NotebookLM sin duplicar fuentes de verdad.

## Decisiones deliberadamente abiertas

Las decisiones abiertas no deben inferirse ni cerrarse sin evidencia y acuerdo
del equipo. Las decisiones respaldadas por contratos y pruebas se mantienen
como tales.

| Decisión | Estado | Evidencia necesaria |
|---|---|---|
| Problema e idea de negocio | Decidido | Clasificación y apoyo al enrutamiento de reclamaciones financieras CFPB |
| Usuario o actor principal | Hipótesis activa | Personal de operaciones o atención; falta contrastar el flujo real |
| Dataset | Decidido con condiciones | Consumer Complaint Database; uso local, minimización y ausencia de narrativas en Git |
| Target y significado de las clases | Decidido | Once familias en `config/cfpb_target_contract.json` |
| Coste relativo de los errores | Pendiente | Impacto por clase y contexto de uso |
| Métrica principal | Decidida para evaluación | Macro F1, métricas por clase, accuracy y gap train-validation |
| Modelo o familia de modelos | Baseline operativo; selección pendiente | Logistic Regression local; ensembles comparados sin Champion |
| Framework de aplicación | Decidido | React PWA válida para productivizar el modelo; evolución nativa sujeta a evidencia |
| Persistencia y base de datos | Parcial | SQLite verificada; PostgreSQL integrado, pendiente de prueba dinámica y migraciones |
| Proveedor y arquitectura cloud | Parcial | Workflow EC2 integrado; faltan entorno verificable, observabilidad y rollback |
| Identidad visual definitiva | Pendiente | Audiencia, contexto y sistema de diseño |

Que una decisión esté pendiente es un estado válido. No representa una carencia que deba rellenarse con supuestos.

## Por qué trabajamos con specs

La metodología basada en specs funciona como contrato común del equipo:

```text
intent -> spec -> plan -> tasks -> implementation -> verification -> closure
```

- El intent fija propósito, límites y principios globales.
- La spec define el problema, usuario, alcance y criterios de aceptación.
- El plan describe la solución técnica, contratos, riesgos y verificación.
- Las tareas convierten el plan en trabajo pequeño y trazable.
- La evidencia determina si una tarea o fase puede cerrarse.

Si una implementación contradice una spec o este intent, se corrige la implementación o se actualiza primero el contrato mediante una decisión explícita y revisable.

## Nivel esencial protegido

El nivel esencial está verificado mediante evidencia de:

- problema, usuario y decisión de negocio definidos;
- dataset seleccionado, licenciado y documentado;
- target y clases con significado inequívoco;
- análisis exploratorio orientado a clasificación;
- separación de datos y preprocesamiento reproducibles;
- baseline funcional y comparación honesta;
- métricas globales y por clase;
- overfitting controlado según la definición acordada;
- aplicación capaz de recibir entradas y devolver una predicción;
- informe técnico, README y demostración coherentes con el estado real.

Ninguna capacidad experta debe desestabilizar esta entrega esencial.

## Evolución media, avanzada y experta

Con el núcleo esencial verificado, el equipo incorpora de forma incremental:

- modelos ensemble y optimización reproducible;
- validación cruzada estratificada;
- feedback local gobernado ya verificado y recolección futura de nuevos datos;
- persistencia SQLite local verificada; Docker/Compose, PostgreSQL y un workflow
  EC2 están integrados pero pendientes de verificación reproducible de entrega;
- quality gates locales ya verificados; pruebas operativas pendientes;
- red neuronal como experimento o componente justificado;
- sistema Champion/Challenger;
- A/B testing;
- monitorización de data drift con alertas;
- promoción controlada de modelos cuando un challenger supere criterios predefinidos.

Una capacidad avanzada solo se presentará como implementada cuando exista código, verificación y evidencia. Si no mejora el sistema, se conservará como experimento documentado.

## Estrategia de entrega

| Etapa | Pregunta de salida |
|---|---|
| Descubrimiento | Verificado: problema y dataset adecuados para multiclase |
| Esencial | Verificado: solución local reproducible de extremo a extremo |
| Medio | ¿La evaluación, optimización y recogida de feedback son robustas? |
| Avanzado | ¿La solución puede probarse, contenerizarse, persistirse y desplegarse? |
| Experto | ¿El ciclo de modelos puede compararse, observarse y gobernarse con seguridad? |

No se avanzará de etapa por acumulación de componentes, sino por evidencia de que la etapa anterior está protegida.

## Principios de trabajo

### Producto y UX

- Comprender al usuario y su decisión antes de diseñar pantallas.
- Hacer visible la incertidumbre del modelo y evitar promesas que la evidencia no sostenga.
- Diseñar para accesibilidad, claridad, estados de error y uso responsive.
- Evitar iconografía genérica asociada a inteligencia artificial.

### Datos y ML

- Prevenir leakage y evaluar si las variables existirán en el momento real de inferencia.
- Proteger el conjunto de test y separar experimentación de evaluación final.
- Analizar desequilibrio, rendimiento por clase y coste de errores.
- Registrar datasets, transformaciones, semillas, parámetros, métricas y artefactos.
- Comparar contra un baseline antes de optimizar.

### Ingeniería y operación

- Mantener dominio, aplicación, infraestructura e interfaz desacoplados.
- Configurar por entorno y no incluir secretos en el repositorio.
- Automatizar comprobaciones proporcionales al riesgo.
- Diseñar despliegue, observabilidad y reversión antes de declarar producción.
- Mantener cambios pequeños, commits descriptivos y Pull Requests trazables.

### Seguridad y responsabilidad

- Aplicar mínimo privilegio y defensa en profundidad.
- Clasificar datos sensibles y reducir su recopilación al mínimo necesario.
- Documentar riesgos de sesgo, privacidad, abuso y decisiones automatizadas.
- Mantener supervisión humana cuando el impacto del error lo requiera.

### Documentación y comunicación

- Tratar la documentación como parte del producto.
- Mantener una única fuente de verdad para cada hecho.
- Respaldar afirmaciones con métricas, capturas, informes, tests o decisiones versionadas.
- Mantener dailies, README, changelog, specs y fuentes de NotebookLM alineados con el estado real.

## Fronteras vigentes

Mientras no exista evidencia adicional, no se debe:

- sustituir macro F1 y métricas por clase por una única cifra agregada;
- elegir un Champion sin CV completa convergida y decisión versionada;
- entrenar con una partición, idioma o política de duplicados no aprobados;
- construir una interfaz que presente confianza o automatización no respaldadas por un contrato;
- confundir una definición PostgreSQL o un workflow EC2 con base compartida o
  despliegue verificados sin build, pruebas, smoke y rollback;
- presentar el JWT de demostración como identidad o autorización productiva;
- presentar capacidades previstas como implementadas;
- presentar feedback local como corpus o reentrenamiento automático.

## Equipo y colaboración

El equipo activo está formado por José, Abel, Víctor y Miguel. Josué comunicó su baja del Bootcamp el 22 de julio de 2026 y dejó de formar parte del equipo.

Las responsabilidades principales están asignadas: Miguel coordina arquitectura y arnés; José, backend; Abel, frontend/UX; Víctor, datos y EDA. Los roles de respaldo y la cobertura estable de producto, MLOps y QA continúan pendientes y no deben asignarse por suposición.

Las decisiones relevantes deben quedar registradas. Las conversaciones ayudan a explorar; el repositorio conserva el acuerdo verificable.

## Estado deseado al finalizar

Al final del proyecto, una persona autorizada deberá poder:

- comprender el problema y el valor de la predicción;
- instalar y ejecutar la solución;
- proporcionar datos válidos y obtener una predicción multiclase;
- reproducir o auditar el entrenamiento y la evaluación;
- consultar métricas, errores, limitaciones y versión del modelo;
- comprobar tests, seguridad básica y evidencias de calidad;
- desplegar o demostrar la aplicación mediante un proceso documentado;
- distinguir con claridad capacidades implementadas, experimentales y pendientes;
- utilizar la documentación para una presentación técnica y otra orientada a negocio.

## Audiencia

Este documento está dirigido a:

- José, Abel, Víctor y Miguel;
- docentes y personas evaluadoras;
- colaboradores técnicos o de producto;
- agentes de IA que trabajen sobre el repositorio;
- cualquier persona que necesite comprender el propósito antes de proponer o implementar una solución.

## Gobierno del intent

- Toda modificación requiere una Pull Request hacia `dev`.
- Los cambios deben explicar qué principio o restricción se modifica y por qué.
- Las decisiones concretas se mantienen en sus specs; este intent solo resume las que cambian los límites globales del proyecto.
- Si cambia el propósito global, las condiciones de entrega o la estrategia de madurez, este documento deberá revisarse junto con README, changelog y fuentes de NotebookLM.

La regla principal es simple: primero validar el problema y proteger una entrega esencial completa; después añadir complejidad que aporte valor demostrable.
