# CAND-001: Clasificación y enrutamiento de reclamaciones financieras

| Campo | Valor |
|---|---|
| Estado | Seleccionada por el equipo; validación de datos obligatoria |
| Fecha de evaluación | 2026-07-22 |
| Proponente | Miguel |
| Spec | [`000-problem-discovery`](../../../specs/000-problem-discovery/spec.md) |
| Dataset candidato | Consumer Complaint Database del CFPB |

## Resumen

Construir un asistente B2B que reciba la narrativa escrita de una reclamación financiera, prediga la familia de producto a la que pertenece y proponga una cola de tramitación. La clasificación apoyará al personal de operaciones; no resolverá la reclamación ni tomará decisiones financieras sobre la persona.

## Problema, usuario y decisión

- Problema: la clasificación manual de reclamaciones puede consumir tiempo, producir criterios inconsistentes y dificultar la detección temprana de cambios en el volumen y lenguaje.
- Usuario propuesto: personal de operaciones o atención al cliente responsable de clasificar reclamaciones. Es una hipótesis pendiente de validación con un usuario o responsable de negocio.
- Decisión: seleccionar la familia de producto y la cola operativa que debe revisar el caso.
- Alternativa actual asumida: lectura y asignación manual mediante reglas o conocimiento del equipo.
- Momento de inferencia: después de recibir la narrativa y antes de asignarla a una cola.

El dataset contiene la familia `product` elegida por quien presentó la reclamación, no el departamento interno que finalmente la tramitó. Por tanto, el modelo predecirá producto; una regla de negocio configurable deberá transformar el producto en una cola.

## Entrada y salida propuestas

### Entrada inicial

- Texto de la reclamación en inglés.
- Sin identificadores, empresa, producto, incidencia o información posterior a la clasificación.

### Salida inicial

- Familia de producto predicha.
- Confianza y alternativas principales.
- Estado `requiere revisión` cuando la confianza no alcance el umbral que se defina experimentalmente.
- Cola recomendada mediante una regla separada del modelo.

## Dataset y procedencia

- Nombre: Consumer Complaint Database.
- Responsable: Consumer Financial Protection Bureau de Estados Unidos.
- Página oficial: <https://www.consumerfinance.gov/data-research/consumer-complaints/>.
- API oficial: <https://cfpb.github.io/ccdb5-api/documentation/>.
- Referencia de campos: <https://cfpb.github.io/api/ccdb/fields.html>.
- Taxonomía vigente desde el 24 de agosto de 2023: <https://files.consumerfinance.gov/f/documents/cfpb_consumer_complaint_form_product_issue_options_August_2023_FINAL.pdf>.
- Descarga CSV oficial: <https://files.consumerfinance.gov/ccdb/complaints.csv.zip>.
- Fecha de consulta: 2026-07-22.

El CFPB indica que los datos publicados pueden descargarse como CSV o JSON, consultarse mediante API y se actualizan generalmente a diario. También advierte que las reclamaciones no constituyen una muestra estadística representativa de todas las experiencias de consumidores.

Una comunicación oficial del CFPB del 24 de junio de 2026 añade una limitación relevante: las reclamaciones de crédito o informes de consumidores superaron los cinco millones en 2025 y la propia entidad afirma que, sin corregir los problemas descritos, los datos no reflejan de forma fiable las condiciones reales del mercado. Esta evidencia refuerza el valor operativo del problema, pero también obliga a medir el desbalanceo, los cambios de procedencia y los posibles usos abusivos del sistema.

Las narrativas se publican cuando la persona consiente compartirlas y después de que el CFPB aplique medidas para retirar información personal. El estándar reconoce que permanece un riesgo residual de que algún dato no sea eliminado.

La documentación de la API declara licencia CC0 para la API. La compatibilidad exacta de la reutilización de narrativas con una futura explotación comercial deberá confirmarse antes de presentar el producto como comercializable.

## Inspección preliminar reproducible

La cabecera HTTP de la descarga completa se consultó sin descargar el archivo:

```bash
curl -I https://files.consumerfinance.gov/ccdb/complaints.csv.zip
```

Resultado observado el 22 de julio de 2026:

```text
HTTP/1.1 200 OK
Last-Modified: Tue, 21 Jul 2026 09:31:56 GMT
Content-Length: 1422352348
```

La descarga comprimida completa ocupa aproximadamente 1,42 GB. No se incorporará al repositorio ni se utilizará completa para el primer baseline sin justificarlo.

La primera consulta automática al endpoint de búsqueda fue rechazada desde el entorno local por la protección perimetral del sitio. Esto no invalida el acceso público documentado, pero obliga a verificar el método reproducible de extracción antes de cerrar la puerta de datos.

## Contrato de datos propuesto

La inspección inicial se limitará a:

```text
date_received >= 2023-08-24
has_narrative = yes
entrada = complaint_what_happened
target = product
idioma inicial = inglés
```

Columnas que no se utilizarán como entrada del modelo:

```text
product
sub_product
issue
sub_issue
company
company_response
company_public_response
tags
timely
date_sent_to_company
```

`product` será exclusivamente el target. `sub_product`, `issue` y `sub_issue` revelarían directa o indirectamente la categorización. `company` permitiría aprender atajos asociados a la cartera de cada empresa en vez del contenido de la reclamación.

## Clases candidatas

La taxonomía oficial desde agosto de 2023 incluye estas familias principales:

1. Checking or savings account.
2. Credit card.
3. Credit reporting or other personal consumer reports.
4. Debt collection.
5. Debt or credit management.
6. Money transfer, virtual currency or money service.
7. Mortgage.
8. Payday loan, title loan, personal loan or advance loan.
9. Prepaid card.
10. Student loan.
11. Vehicle loan or lease.

La lista definitiva dependerá de la distribución de narrativas. No se eliminarán ni agruparán clases únicamente para mejorar las métricas; cualquier cambio deberá conservar significado de negocio y quedar registrado.

## Puertas críticas

| Puerta | Estado | Evidencia o condición pendiente |
|---|---|---|
| G-01 Problema y usuario | Cumple | Problema, usuario operativo y decisión identificados; el flujo exacto deberá contrastarse durante la spec funcional. |
| G-02 Multiclase real | Condicional | Existen más de tres productos; falta comprobar soporte por clase con la taxonomía estable. |
| G-03 Datos reproducibles | Condicional | Fuente y descargas oficiales verificadas; falta cerrar extracción filtrada y licencia de uso comercial. |
| G-04 Inferencia válida | Condicional | Contrato narrative-only propuesto; deberá comprobarse leakage y disponibilidad real. |
| G-05 Riesgo asumible | Condicional | Datos publicados y tratados, pero existe riesgo residual de información personal. |
| G-06 Entrega viable | Condicional | Viable con subconjunto reproducible y baseline lineal; pendiente medir volumen y tiempos. |

Ninguna puerta se considera incumplida. El equipo eligió esta dirección por unanimidad, pero la implementación funcional no comenzará hasta que el spike de datos resuelva las condiciones de G-02 a G-06 o registre una revisión expresa de la decisión.

## Puntuación técnica preliminar

| Criterio | Peso | Puntuación | Resultado | Justificación resumida |
|---|---:|---:|---:|---|
| Valor del problema | 15 % | 4/5 | 12 | Volumen y necesidad operativa respaldados por fuentes oficiales; el flujo concreto sigue pendiente de contraste. |
| Usuario y decisión | 10 % | 4/5 | 8 | Usuario y decisión comprensibles; mapping a cola aún hipotético. |
| Disponibilidad, licencia y reproducibilidad | 15 % | 4/5 | 12 | Fuente oficial y API; extracción filtrada y uso comercial pendientes. |
| Calidad y suficiencia de datos | 10 % | 3/5 | 6 | Alto volumen, con sesgo de publicación, desbalanceo y taxonomía histórica. |
| Encaje multiclase y evaluabilidad | 10 % | 4/5 | 8 | Múltiples clases oficiales; falta comprobar distribución estable. |
| Viabilidad de entrega | 15 % | 3/5 | 9 | Baseline asequible si se limita el volumen; dataset completo no es apropiado para el primer ciclo. |
| UX y demostración | 10 % | 4/5 | 8 | Entrada textual, alternativas, confianza y feedback son comprensibles. |
| Evolución hasta nivel experto | 10 % | 5/5 | 10 | Permite challenger, transformer, feedback, A/B y drift lingüístico. |
| Riesgo y uso responsable | 5 % | 2/5 | 2 | Texto financiero y riesgo residual de información personal. |
| **Total** | **100 %** |  | **75/100** | **Recomendada con validaciones obligatorias** |

Esta puntuación es una preevaluación documental, no la mediana de cuatro hojas individuales. La revisión de `C-01` de 3 a 4 se apoya en nueva evidencia oficial sobre el volumen, la revisión manual y la necesidad de mejorar la utilidad operativa del sistema; no procede únicamente de la votación. La puntuación no elimina ninguna puerta condicional.

## Aplicación y evolución

### Nivel esencial

- formulario de texto;
- baseline TF-IDF con modelo lineal;
- clasificación multiclase y probabilidades calibradas cuando sea posible;
- métricas globales y por clase;
- revisión manual para baja confianza.

### Evolución prevista

- feedback de corrección y persistencia gobernada;
- challenger ensemble o red neuronal;
- comparación con un transformer;
- monitorización de vocabulario, longitud y distribución de clases;
- A/B testing controlado;
- promoción de modelos mediante criterios predefinidos.

Esta evolución describe potencial, no funcionalidad implementada.

## Riesgos y mitigaciones iniciales

| Riesgo | Mitigación propuesta |
|---|---|
| Información personal residual | No versionar narrativas, minimizar logs, aplicar redacción adicional y limitar retención. |
| Sesgo de publicación voluntaria | Documentar que las narrativas públicas no representan todas las reclamaciones. |
| Uso abusivo y cambios de procedencia | Analizar periodos, procedencia disponible, duplicados y cambios bruscos; no interpretar el volumen como incidencia real de mercado. |
| Cambio de taxonomía | Limitar el primer estudio a la taxonomía vigente desde 2023 y versionar el mapping. |
| Desbalanceo | Medir soporte, utilizar macro F1 y recall por clase, y comparar pesos de clase. |
| Leakage | Utilizar la narrativa como única entrada inicial y auditar términos y metadatos. |
| Sobreconfianza | Calibrar probabilidades y ofrecer revisión manual o abstención. |
| Uso indebido | Prohibir decisiones financieras, legales o de elegibilidad basadas en la predicción. |
| Drift lingüístico | Monitorizar vocabulario, longitud, confianza y distribución por periodo. |

## Validaciones pendientes

- Obtener el recuento de narrativas por clase desde el 24 de agosto de 2023.
- Comprobar textos ausentes, longitud, duplicados, redacciones e idioma.
- Definir un método reproducible de descarga o consulta filtrada.
- Confirmar las condiciones aplicables a una explotación comercial.
- Validar el usuario B2B y el mapping entre producto y cola.
- Estimar recursos y tiempo de baseline con una muestra representativa.
- Definir responsables y fecha límite del spike de viabilidad antes de la implementación funcional.

## Evidencias

- [Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/).
- [API oficial](https://cfpb.github.io/ccdb5-api/documentation/).
- [Referencia de campos](https://cfpb.github.io/api/ccdb/fields.html).
- [Opciones de producto e incidencia desde agosto de 2023](https://files.consumerfinance.gov/f/documents/cfpb_consumer_complaint_form_product_issue_options_August_2023_FINAL.pdf).
- [Estándar de retirada de información personal](https://files.consumerfinance.gov/f/documents/201503_cfpb_Narrative-Scrubbing-Standard.pdf).
- [Correcciones y limitaciones comunicadas por el CFPB en junio de 2026](https://www.consumerfinance.gov/about-us/newsroom/the-cfpb-is-correcting-flaws-to-restore-integrity-and-utility-to-the-consumer-complaint-system/).
