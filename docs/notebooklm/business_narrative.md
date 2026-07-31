# Narrativa de negocio

> Narrativa basada en evidencia vigente. ClaimVox puede demostrar localmente el
> recorrido completo entre interfaz, servicio y baseline, pero no existe un
> producto desplegado ni una decisión automática.

## Situación actual

Las organizaciones que reciben reclamaciones financieras necesitan interpretar textos libres y asignarlos a la categoría y al circuito adecuados. El volumen, el vocabulario y la distribución de esas reclamaciones pueden cambiar con el tiempo.

## Problema

La lectura y clasificación manual puede consumir tiempo y producir asignaciones inconsistentes. El proyecto estudiará si una predicción multiclase puede apoyar esa primera clasificación sin sustituir la revisión humana.

## Usuario afectado

El usuario propuesto es personal de operaciones o atención al cliente responsable de clasificar reclamaciones. El flujo concreto todavía debe contrastarse.

## Propuesta de valor

Ofrecer una primera categoría de producto, alternativas y un nivel de confianza para que la persona usuaria confirme o corrija el destino. La herramienta no resolverá la reclamación ni tomará decisiones financieras, legales o de elegibilidad.

## Cómo ayuda la predicción multiclase

El baseline local ya evaluado propone una única familia de producto entre once categorías canónicas y muestra alternativas para facilitar la revisión. Una regla separada y configurable traduciría esa categoría a una cola operativa; esa regla no toma decisiones autónomas.

## Flujo de uso

1. La persona introduce o revisa una narrativa sin identificadores innecesarios.
2. El sistema propone una familia de producto, confianza y alternativas.
3. Una confianza insuficiente activa revisión manual.
4. La persona confirma o corrige la categoría.
5. La persona puede registrar localmente una confirmación o corrección
   minimizada; su uso futuro para mejorar modelos requiere un corpus y una
   política todavía no implementados.

## Impacto esperado y límites

El impacto esperado es reducir esfuerzo de clasificación y hacer más consistente el enrutamiento inicial. Todavía no se ha medido. Los datos públicos del CFPB no representan todo el mercado, pueden contener información personal residual y presentan riesgo de desbalanceo y cambio temporal.

## Por qué es una base fiable

La demostración no parte de una pantalla aislada: reúne un contrato de once
clases, datos preparados de forma reproducible, evaluación versionada, un
servicio local y una interfaz que conserva la revisión humana. La arquitectura
separa experiencia, servicio y predictor. El feedback se incorporó mediante
contratos y pruebas. Docker, PostgreSQL y un acceso JWT demo están integrados
como siguiente capa técnica, pero necesitan ejecución reproducible y no
demuestran por sí solos una operación cloud.

## Mensaje de cierre

El equipo ha elegido esta dirección por unanimidad y ya puede demostrar
el recorrido entre ClaimVox, un servicio y un baseline reproducible,
manteniendo siempre la revisión humana. El mock sigue disponible para demos sin
servicio. No se afirmará que existe un producto cloud verificado, una decisión
automática ni una operación productiva.
