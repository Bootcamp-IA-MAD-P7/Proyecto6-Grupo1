# Complaint Routing Interface

React PWA en integración para `PG-4`. La clasificación actual utiliza respuestas
sintéticas y no existe todavía conexión con un backend ni con un modelo
entrenado.

## Dictado por voz

El dictado es una ayuda opcional para rellenar el mismo campo de narrativa:

- solo comienza cuando la persona pulsa `Start dictation`;
- solicita permiso de micrófono mediante la Web Speech API del navegador;
- puede depender del navegador o de su proveedor para procesar el audio;
- inserta una transcripción editable que debe revisarse antes de enviarse;
- no bloquea la escritura cuando la función no está disponible o falla;
- esta aplicación no guarda audio ni transcripciones en almacenamiento, caché,
  URL o consola.

La compatibilidad varía entre navegadores. La entrada por teclado permanece
siempre disponible. El idioma utilizado por el reconocimiento se toma del
documento o del navegador como configuración técnica; no representa una política
de idioma aprobada para el producto.

La instalación, los comandos, el modo mock, el contrato, el comportamiento
offline y las capacidades propuestas se completarán durante el cierre de esta
integración en la tarea OpenSpec 10.1.
