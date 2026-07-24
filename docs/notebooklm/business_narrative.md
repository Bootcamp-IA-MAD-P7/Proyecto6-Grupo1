# Narrativa de negocio

> Narrativa basada en evidencia vigente. Existe un prototipo de interfaz para
> revisar el recorrido, pero no un producto operativo ni resultados de modelo.

## Situación actual

Las organizaciones que reciben reclamaciones financieras necesitan interpretar textos libres y asignarlos a la categoría y al circuito adecuados. El volumen, el vocabulario y la distribución de esas reclamaciones pueden cambiar con el tiempo.

## Problema

La lectura y clasificación manual puede consumir tiempo y producir asignaciones inconsistentes. El proyecto estudiará si una predicción multiclase puede apoyar esa primera clasificación sin sustituir la revisión humana.

## Usuario afectado

El usuario propuesto es personal de operaciones o atención al cliente responsable de clasificar reclamaciones. El flujo concreto todavía debe contrastarse.

## Propuesta de valor

Ofrecer una primera categoría de producto, alternativas y un nivel de confianza para que la persona usuaria confirme o corrija el destino. La herramienta no resolverá la reclamación ni tomará decisiones financieras, legales o de elegibilidad.

## Cómo ayuda la predicción multiclase

Cada narrativa se asignaría a una única familia de producto entre tres o más categorías significativas. Una regla separada y configurable traduciría esa categoría a una cola operativa.

## Flujo de uso

1. La persona introduce o revisa una narrativa sin identificadores innecesarios.
2. El sistema propone una familia de producto, confianza y alternativas.
3. Una confianza insuficiente activa revisión manual.
4. La persona confirma o corrige la categoría.
5. El feedback puede utilizarse de forma gobernada para medir y mejorar versiones futuras.

## Impacto esperado y límites

El impacto esperado es reducir esfuerzo de clasificación y hacer más consistente el enrutamiento inicial. Todavía no se ha medido. Los datos públicos del CFPB no representan todo el mercado, pueden contener información personal residual y presentan riesgo de desbalanceo y cambio temporal.

## Mensaje de cierre

El equipo ha elegido esta dirección por unanimidad y ya puede demostrar el
recorrido mediante una interfaz con respuestas sintéticas. El siguiente paso
sigue siendo completar la evidencia de datos y construir el modelo; no se
afirmará que existe predicción real hasta disponer de resultados reproducibles
y una integración verificada.
