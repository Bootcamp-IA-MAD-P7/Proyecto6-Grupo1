# Aplicación

Aquí se implementará la capa de interacción con el modelo cuando se decidan la idea de negocio y el framework entre las opciones permitidas.

La aplicación deberá consumir el mismo pipeline de inferencia versionado, mostrar una clase multiclase y permitir feedback cuando se alcance el nivel medio.

```text
interface/  experiencia de usuario y presentación
api/        adaptador HTTP, si la arquitectura aprobada lo requiere
```

La aplicación no accederá directamente a archivos de entrenamiento ni contendrá lógica de selección del modelo.
