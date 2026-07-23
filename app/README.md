# Aplicación

La dirección aprobada para la capa de interacción es una React PWA. En `dev` todavía no existe una aplicación integrada: solo están versionados el flujo de experiencia y el contrato OpenAPI para trabajar con respuestas simuladas.

Abel creará el frontend desde cero mediante `003/T-006` y registrará sus decisiones de frontend y UX antes o durante la implementación. El trabajo deberá diferenciar claramente los mocks de la futura inferencia real.

```text
interface/  React PWA cuando exista implementación verificada
api/        adaptador HTTP futuro; todavía no implementado
```

La aplicación no accederá directamente a archivos de entrenamiento ni contendrá lógica de selección del modelo.
