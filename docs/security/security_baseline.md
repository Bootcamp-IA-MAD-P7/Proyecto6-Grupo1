# Baseline de seguridad

## Repositorio

- Secretos excluidos y detección automática cuando esté disponible.
- Dependencias monitorizadas.
- Pull Requests obligatorios para ramas protegidas.
- Workflows con permisos mínimos y acciones versionadas.
- Releases trazables a commits verificados.

## Aplicación

- Validación estricta de entradas.
- Mensajes de error sin detalles internos.
- Límites de tamaño y frecuencia cuando proceda.
- Autenticación y autorización definidas antes de exponer datos privados.
- Cabeceras, CORS y transporte seguro configurados por entorno.

## Datos

- Clasificación de sensibilidad antes de incorporar el dataset.
- Minimización y finalidad documentadas.
- Separación entre datos originales, procesados y operativos.
- Retención y eliminación definidas si se recoge feedback.
- Datos de tests sintéticos o anonimizados.

## Modelos

- Artefactos con versión, hash y metadatos.
- Carga únicamente desde ubicaciones controladas.
- Contrato de features validado antes de inferencia.
- Promoción condicionada y reversible.
- Registro de versión en cada predicción.

## Infraestructura

- Imágenes mínimas y usuarios no privilegiados.
- Health/readiness sin filtrar secretos.
- Redes y bases de datos con exposición mínima.
- Credenciales temporales para CI/CD cuando sea posible.
- Backups, migraciones y rollback probados.
