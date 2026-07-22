# Aplicación

La capa de interacción se desarrolla como React PWA contra el contrato de inferencia versionado. La implementación actual utiliza respuestas sintéticas y no está conectada a un modelo entrenado.

La interfaz muestra una clase multiclase, alternativas y revisión humana. El feedback, historial y routing automático quedan fuera de la primera versión hasta que dispongan de una spec y políticas propias.

```text
interface/  React PWA, cliente de inferencia sustituible y mock explícito
api/        adaptador HTTP futuro; todavía no implementado
```

La aplicación no accederá directamente a archivos de entrenamiento ni contendrá lógica de selección del modelo.

La guía de desarrollo y los límites del mock están en [`interface/README.md`](interface/README.md).
