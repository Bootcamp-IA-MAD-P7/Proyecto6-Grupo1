# Aplicación

<<<<<<< HEAD
La capa de interacción se desarrolla como React PWA contra el contrato de inferencia versionado. La implementación actual utiliza respuestas sintéticas y no está conectada a un modelo entrenado.

La interfaz muestra una clase multiclase, alternativas y revisión humana. El feedback, historial y routing automático quedan fuera de la primera versión hasta que dispongan de una spec y políticas propias.

```text
interface/  React PWA, cliente de inferencia sustituible y mock explícito
=======
La dirección aprobada para la capa de interacción es una React PWA. En `dev` todavía no existe una aplicación integrada: solo están versionados el flujo de experiencia y el contrato OpenAPI para trabajar con respuestas simuladas.

Abel creará el frontend desde cero mediante `003/T-006` y registrará sus decisiones de frontend y UX antes o durante la implementación. El trabajo deberá diferenciar claramente los mocks de la futura inferencia real.

```text
interface/  React PWA cuando exista implementación verificada
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83
api/        adaptador HTTP futuro; todavía no implementado
```

La aplicación no accederá directamente a archivos de entrenamiento ni contendrá lógica de selección del modelo.

La guía de desarrollo y los límites del mock están en [`interface/README.md`](interface/README.md).
