# Arquitectura de información

> Estado: flujo local implementado y revisable; validación con usuarios B2B
> todavía pendiente.

## Usuario propuesto

Personal de operaciones o atención que recibe una reclamación escrita y necesita identificar la familia financiera que debe revisarla. La aplicación apoya la decisión y no sustituye su criterio.

## Tareas principales

1. Comprender finalidad y límites del asistente.
2. Introducir una narrativa sin información personal innecesaria.
3. Revisar el texto antes de enviarlo.
4. Solicitar una clasificación al servicio local.
5. Interpretar clase, alternativas y necesidad de revisión.
6. Registrar feedback minimizado o iniciar una nueva clasificación.
7. En revisión administrativa local, consultar health y el desglose agregado
   del feedback sin acceder a registros individuales.

El feedback local minimizado aparece únicamente después de una predicción local
válida. El Dashboard muestra solo versión de modelo, clase sugerida, decisión y
conteo agregado. Historial individual y mapping a colas siguen fuera de la
experiencia.

## Inventario de contenidos

- Propósito y aviso de privacidad.
- Campo de narrativa y ayuda contextual.
- Acción de clasificación.
- Estado de carga o conectividad.
- Familia predicha.
- Alternativas disponibles.
- Confianza calibrada cuando exista.
- Motivos de revisión.
- Versiones de modelo y taxonomía.
- Limitaciones y siguiente acción.

## Mapa de experiencia

La PWA resuelve el recorrido en un único espacio de trabajo responsive con
cuatro estados visibles:

```text
Describe: narrativa, privacidad y ayuda
        ↓
Review: resumen y confirmación
        ↓
Guidance: carga / error o clasificación real
        ↓
Next step: feedback o nueva clasificación
```

La clasificación vive en `/classify`. La navegación por rol y la sesión actual
son de demostración; no acreditan autenticación ni permisos.

## Estados

| Estado | Información y acción esperada |
|---|---|
| Inicial | Propósito, límites, aviso y formulario vacío |
| Entrada inválida | Motivo junto al campo y foco gestionado |
| Enviando | Progreso anunciado y doble envío bloqueado |
| Resultado | Clase, alternativas, trazabilidad y siguiente acción |
| Revisión | Motivos claros sin depender solo de color |
| Offline | Explica que el shell está disponible pero la predicción requiere servicio |
| Servicio no disponible | Mensaje seguro, reintento y conservación local no persistente del texto mientras la vista siga abierta |
| Límite de frecuencia | Espera o reintento sin detalles internos |

## Responsive y accesibilidad

- Una columna legible en móvil y expansión controlada en escritorio.
- Orden de foco coherente y foco visible.
- Etiqueta persistente para el campo; el placeholder no actúa como etiqueta.
- Cambios de estado anunciados a tecnologías de asistencia.
- Errores asociados al campo y resumen cuando sea necesario.
- Ningún significado depende únicamente de color, icono o animación.
- Respeto a preferencias de movimiento reducido.

## Permisos y privacidad

El JWT de demostración se configura por entorno y protege el recorrido, pero no
constituye identidad ni autorización productiva. La narrativa no se guarda, no
aparece en la URL y no se devuelve en la respuesta. La política aprobada permite
metadatos cerrados de feedback con retención local; no se muestra historial
individual ni se presenta esa persistencia como operación compartida.

## Criterios de validación con usuarios

- La persona entiende que recibe una recomendación y no una decisión automática.
- Puede completar el flujo sin conocer terminología de machine learning.
- Comprende qué significa `requiere revisión` aunque no exista porcentaje.
- Sabe qué información no debe introducir.
- Puede recuperarse de errores, offline e indisponibilidad.
- La familia predicha aporta valor antes de definir una cola operativa.
