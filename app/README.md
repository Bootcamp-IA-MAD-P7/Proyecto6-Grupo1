# Aplicación

La dirección aprobada para la capa de interacción es una React PWA. En `dev` todavía no existe una aplicación integrada: solo están versionados el flujo de experiencia y el contrato OpenAPI para trabajar con respuestas simuladas.

Existe una propuesta experimental en la PR `#14`, pendiente de actualización y revisión con Abel. No debe tratarse como producto implementado ni como inferencia real.

```text
interface/  React PWA cuando la propuesta sea revisada e integrada
api/        adaptador HTTP futuro; todavía no implementado
```

La aplicación no accederá directamente a archivos de entrenamiento ni contendrá lógica de selección del modelo.
