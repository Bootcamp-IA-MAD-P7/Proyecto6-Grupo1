## Context

El baseline TF-IDF + LogisticRegression es el único candidato evaluado con el
split temporal completo y un gap train-validation de macro F1 inferior a 0.05.
Las comparativas Random Forest, XGBoost y LightGBM aportan exploración útil en
una muestra de 50K, pero no cumplen todavía el protocolo completo ni permiten
seleccionar un champion. ClaimVox y el servicio FastAPI local ya consumen un
artefacto compatible bajo configuración explícita y mantienen revisión humana.

La entrega esencial requiere completar la evidencia, no introducir una familia
de modelos adicional: matriz de confusión, importancia de variables, análisis de
errores, manifiesto de artefacto y guía reproducible sin datos sensibles.

## Goals / Non-Goals

**Goals:**

- Seleccionar el baseline LogisticRegression como candidato esencial local solo
  si sus evidencias reproducibles y sus tests de contrato siguen siendo válidos.
- Generar análisis completo sobre validation, sin volver a usar el test protegido
  para seleccionar ni ajustar.
- Guardar el artefacto local en `models/`, ignorado por Git, y versionar solo su
  manifiesto, configuración, métricas y figuras agregadas.
- Producir una lectura honesta de errores y limitaciones por clase.
- Consolidar la guía técnica de la entrega esencial.

**Non-Goals:**

- No optimizar hiperparámetros ni repetir la comparación ensemble completa.
- No convertir el baseline en modelo desplegado, champion MLOps o decisión
  automática.
- No incluir filas, narrativas, textos representativos, predicciones por fila ni
  binarios de modelo en Git.
- No modificar el diseño, contratos funcionales ni seguridad de ClaimVox/FastAPI
  salvo documentación de compatibilidad.

## Decisions

### Selección esencial basada en el baseline completo

Se usará la configuración LogisticRegression ya evaluada (`C=0.1`, TF-IDF con
unigramas y bigramas, `class_weight=balanced`, semilla 42) como candidato de
entrega esencial. Es el único modelo con evidencia sobre todas las particiones,
artefacto local y gap validado de 0.0482.

Alternativa descartada por ahora: seleccionar XGBoost por su macro F1 de muestra.
No es comparable aún porque solo cuenta con 50K y no ha superado el protocolo de
gap completo. Permanece como trabajo medio, no como modelo esencial elegido.

### Validation para diagnósticos; test protegido para resultado ya registrado

La matriz de confusión, el análisis de errores y los diagnósticos por clase se
generarán sobre validation completo. El test protegido no se utilizará de nuevo
para elegir, depurar ni ajustar; solo se enlazarán las métricas ya versionadas
en la guía final.

### Explicabilidad compatible con texto lineal

La importancia se calculará como coeficientes TF-IDF por clase del clasificador
lineal. Las figuras se etiquetarán como asociaciones del modelo, no causalidad ni
explicación individual de una reclamación. La evidencia no contendrá texto de
reclamaciones.

### Errores agregados sin narrativas

El análisis utilizará confusiones más frecuentes, soporte, precision, recall y
F1 por clase. No se conservarán ejemplos de texto, identificadores ni salidas
por fila. Las acciones propuestas se limitarán a revisión humana, cobertura de
clases débiles y experimentación posterior.

## Risks / Trade-offs

- [Clases minoritarias con F1 bajo] → mantener sus limitaciones visibles y no
  presentar la recomendación como decisión automática.
- [Uso accidental del test protegido] → las tareas y scripts de diagnóstico
  recibirán solo validation; el informe reutiliza las métricas test ya
  registradas.
- [Artefacto local no disponible en otra máquina] → registrar versión,
  configuración, hash y comando de reconstrucción, sin versionar el binario.
- [Tiempo de reentrenamiento] → la ejecución completa se realiza una vez con
  configuración congelada; los tests usan datos sintéticos.

## Migration Plan

1. Añadir un comando de evaluación final que entrene localmente con la
   configuración congelada y genere únicamente evidencia agregada.
2. Ejecutarlo sobre las particiones locales aprobadas y revisar los resultados.
3. Verificar carga, probabilidades y clases con tests sintéticos.
4. Actualizar la documentación y los niveles de entrega solo si la evidencia
   resultante coincide con los criterios.
5. Si el comando falla o el gap deja de cumplir, no se cambia ningún criterio a
   verificado; se conserva el baseline anterior y se documenta el bloqueo.
